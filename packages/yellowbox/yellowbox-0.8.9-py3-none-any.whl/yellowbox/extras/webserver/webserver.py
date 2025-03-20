from __future__ import annotations

from contextlib import contextmanager
from threading import Lock, Thread
from time import sleep
from typing import ContextManager, Iterator, Mapping, Optional, Union, overload
from warnings import warn

from requests import ConnectionError, RequestException, get
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, WebSocketRoute
from uvicorn import Config, Server

from yellowbox import YellowService
from yellowbox.extras.webserver.class_endpoint import HTTPEndpointTemplate, WSEndpointTemplate
from yellowbox.extras.webserver.endpoints import (
    HTTP_SIDE_EFFECT,
    METHODS,
    WS_SIDE_EFFECT,
    MockHTTPEndpoint,
    MockWSEndpoint,
    http_endpoint,
    ws_endpoint,
)
from yellowbox.retry import RetrySpec
from yellowbox.utils import docker_host_name


class HandlerError(Exception):
    """
    An exception occurred while handling an endpoint in the webserver thread
    """


class WebServer(YellowService):
    """
    An easy-to-modify HTTP and websocket server, wrapping a starlette application
    """

    _PORT_ACCESS_MAX_RETRIES = 100  # the maximum number of attempts to make when accessing a binding port.
    _PORT_ACCESS_INTERVAL = 0.01  # retry interval between attempts when accessing a binding port.
    _SHUTDOWN_SERVE_THREAD_TIMEOUT = 5  # the maximum time to wait for the server thread to stop when shutting down

    _CLASS_ENDPOINT_TEMPLATES: Mapping[str, Union[HTTPEndpointTemplate, WSEndpointTemplate]] = {}

    def __init__(self, name: str, port: int = 0, **kwargs):
        """
        Args:
            name: the name of the service
            port: the port to bind to when serving, default will bind to an available port
            **kwargs: forwarded to the uvicorn configuration.
        """
        self.__name__ = name
        self._app = Starlette(debug=True)
        self._route_lock = Lock()

        # since the main thread won't catch errors in handlers, this class will store any error raised while handling,
        #  and raise them in the main thread as soon as we can
        self.pending_exception: Optional[Exception] = None

        if "log_config" not in kwargs:
            kwargs["log_config"] = None

        kwargs.setdefault("host", "0.0.0.0")

        self._port = port

        config = Config(self._app, **kwargs, port=self._port)
        self._server = Server(config)
        self._serve_thread = Thread(name=f"{name}_thread", target=self._server.run)

    @property
    def port(self) -> int:
        """
        Returns:
            The port the service is bound to, if the service is binding to anything.

        Notes:
            Will only return 0 if the port was not provided during construction and the service thread is not running
            If the service is starting up, this property will block until the port is bound, or raise an error if
            blocked for longer than 1 second.
        """
        if self._port or not self._serve_thread.is_alive():
            return self._port
        for _ in range(self._PORT_ACCESS_MAX_RETRIES):
            servers = getattr(self._server, "servers", None)
            if servers:
                sockets = getattr(servers[0], "sockets", None)
                if sockets:
                    socket = sockets[0]
                    break
            sleep(self._PORT_ACCESS_INTERVAL)
        else:
            raise RuntimeError("timed out when getting binding port")
        self._port = socket.getsockname()[1]
        return self._port

    @overload
    def add_http_endpoint(self, endpoint: MockHTTPEndpoint) -> MockHTTPEndpoint: ...

    @overload
    def add_http_endpoint(
        self,
        methods: METHODS,
        rule_string: str,
        side_effect: HTTP_SIDE_EFFECT,
        *,
        auto_read_body: bool = True,
        forbid_implicit_head_verb: bool = True,
        name: Optional[str] = None,
    ) -> MockHTTPEndpoint: ...

    def add_http_endpoint(self, *args, **kwargs) -> MockHTTPEndpoint:
        """
        Add an http endpoint to the server
        Args:
            *args: either a single mock http endpoint, or parameters forwarded to http_endpoint construct one
            **kwargs: forwarded to http_endpoint to construct an endpoint

        Returns:
            the http endpoint added to the server
        """
        self.raise_from_pending()
        if len(args) == 1 and not kwargs:
            (ep,) = args
        else:
            ep = http_endpoint(*args, **kwargs)
        if ep.owner is not None:
            raise RuntimeError("an endpoint cannot be added twice")
        with self._route_lock:
            self._app.routes.append(ep.route())
        ep.owner = self
        return ep

    def remove_http_endpoint(self, endpoint: MockHTTPEndpoint):
        """
        Remove an http endpoint previously added to the server
        Args:
            endpoint: the endpoint to remove
        """
        self.raise_from_pending()
        if endpoint.owner is not self:
            raise RuntimeError("endpoint is not added to the server")
        with self._route_lock:
            i = next(
                (
                    i
                    for i, route in enumerate(self._app.routes)
                    if isinstance(route, Route) and route.endpoint == endpoint.get
                ),
                None,
            )
            if i is None:
                raise RuntimeError("endpoint is not found in the server")
            self._app.router.routes.pop(i)
            endpoint.owner = None

    @overload
    def patch_http_endpoint(self, endpoint: MockHTTPEndpoint) -> ContextManager[MockHTTPEndpoint]: ...

    @overload
    def patch_http_endpoint(
        self,
        methods: METHODS,
        rule_string: str,
        side_effect: HTTP_SIDE_EFFECT,
        *,
        auto_read_body: bool = True,
        forbid_implicit_head_verb: bool = True,
        name: Optional[str] = None,
    ) -> ContextManager[MockHTTPEndpoint]: ...

    @contextmanager  # type:ignore[misc]
    def patch_http_endpoint(self, *args, **kwargs) -> Iterator[MockHTTPEndpoint]:
        """
        A context manager to add and then remove an http endpoint
        Args:
            *args: forwarded to self.add_http_endpoint
            **kwargs: forwarded to self.add_http_endpoint

        Returns:
            The temporarily added endpoint
        """
        ep = self.add_http_endpoint(*args, **kwargs)
        try:
            yield ep
        finally:
            self.remove_http_endpoint(ep)

    @overload
    def add_ws_endpoint(self, endpoint: MockWSEndpoint) -> MockWSEndpoint: ...

    @overload
    def add_ws_endpoint(
        self,
        rule_string: str,
        side_effect: WS_SIDE_EFFECT,
        *,
        name: Optional[str] = None,
        allow_abrupt_disconnect: bool = True,
    ) -> MockWSEndpoint: ...

    def add_ws_endpoint(self, *args, **kwargs):
        """
        Add a websocket endpoint to the server
        Args:
            *args: either a single mock ws endpoint, or parameters forwarded to ws_endpoint construct one
            **kwargs: forwarded to ws_endpoint to construct an endpoint

        Returns:
            the websocket endpoint added to the server
        """
        self.raise_from_pending()
        if len(args) == 1 and not kwargs:
            (ep,) = args
        else:
            ep = ws_endpoint(*args, **kwargs)

        if ep.owner is not None:
            raise RuntimeError("an endpoint cannot be added twice")

        with self._route_lock:
            self._app.routes.append(WebSocketRoute(ep.rule_string, ep.endpoint, name=ep.__name__))
        ep.owner = self
        return ep

    def remove_ws_endpoint(self, endpoint: MockWSEndpoint):
        """
        Remove a websocket endpoint previously added to the server
        Args:
            endpoint: the endpoint to remove
        """
        self.raise_from_pending()
        if endpoint.owner is not self:
            raise RuntimeError("endpoint is not added to the server")
        with self._route_lock:
            i = next(
                (
                    i
                    for (i, route) in enumerate(self._app.router.routes)
                    if isinstance(route, WebSocketRoute) and route.app == endpoint.endpoint
                ),
                None,
            )
            if i is None:
                raise RuntimeError("endpoint is not found in the server")
            self._app.router.routes.pop(i)
            endpoint.owner = None

    @overload
    def patch_ws_endpoint(self, endpoint: MockWSEndpoint) -> ContextManager[MockWSEndpoint]: ...

    @overload
    def patch_ws_endpoint(
        self,
        rule_string: str,
        side_effect: WS_SIDE_EFFECT,
        *,
        name: Optional[str] = None,
        allow_abrupt_disconnect: bool = True,
    ) -> ContextManager[MockWSEndpoint]: ...

    @contextmanager  # type:ignore[misc]
    def patch_ws_endpoint(self, *args, **kwargs):
        """
        A context manager to add and then remove a ws endpoint
        Args:
            *args: forwarded to self.add_ws_endpoint
            **kwargs: forwarded to self.add_ws_endpoint

        Returns:
            The temporarily added endpoint
        """
        ep = self.add_ws_endpoint(*args, **kwargs)
        try:
            yield ep
        finally:
            self.remove_ws_endpoint(ep)

    def local_url(self, schema: Optional[str] = "http") -> str:
        """
        Get the url to access this server from the local machine
        Args:
            schema: the optional schema of the url, defaults to http
        """
        if schema is None:
            return f"localhost:{self.port}"
        return f"{schema}://localhost:{self.port}"

    def container_url(self, schema="http") -> str:
        """
        Get the url to access this server from a docker container running in the local machine
        Args:
            schema: the optional schema of the url, defaults to http
        """
        if schema is None:
            return f"{docker_host_name}:{self.port}"
        return f"{schema}://{docker_host_name}:{self.port}"

    def start(self, retry_spec: Optional[RetrySpec] = None) -> WebServer:
        if self._serve_thread.is_alive():
            raise RuntimeError("thread cannot be started twice")
        self._serve_thread.start()
        with self.patch_http_endpoint("GET", "/__yellowbox/ping", side_effect=PlainTextResponse("")):
            retry_spec = retry_spec or RetrySpec(interval=0.1, timeout=5)
            retry_spec.retry(
                lambda: get(self.local_url() + "/__yellowbox/ping", timeout=1.0).raise_for_status(),
                (ConnectionError, RequestException),
            )

        # add all the class endpoints
        for name, template in type(self)._CLASS_ENDPOINT_TEMPLATES.items():  # noqa: SLF001
            ep: Union[MockHTTPEndpoint, MockWSEndpoint]
            if isinstance(template, HTTPEndpointTemplate):
                ep = template.construct(self)
                self.add_http_endpoint(ep)
            else:
                assert isinstance(template, WSEndpointTemplate)
                ep = template.construct(self)
                self.add_ws_endpoint(ep)
            setattr(self, name, ep)

        return super().start()

    def stop(self):
        self._server.should_exit = True
        self._serve_thread.join(self._SHUTDOWN_SERVE_THREAD_TIMEOUT)
        if self._serve_thread.is_alive():
            warn(f"server thread did not stop after {self._SHUTDOWN_SERVE_THREAD_TIMEOUT} seconds", stacklevel=2)
        super().stop()
        self.raise_from_pending()

    def is_alive(self) -> bool:
        self.raise_from_pending()
        return self._serve_thread.is_alive()

    def raise_from_pending(self):
        # if there is a pending exception, this will raise it
        if self.pending_exception:
            pending = self.pending_exception
            self.pending_exception = None
            raise HandlerError() from pending

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _cls_endpoints = {}
        for base in cls.__bases__:
            base_http_templates = getattr(base, "_CLASS_ENDPOINT_TEMPLATES", None)
            if base_http_templates:
                overlapping_keys = base_http_templates.keys() & _cls_endpoints.keys()
                if overlapping_keys:
                    raise TypeError(f"overlapping cls endpoints: {overlapping_keys}")
                _cls_endpoints.update(base_http_templates)

        for k, v in vars(cls).items():
            if isinstance(v, (HTTPEndpointTemplate, WSEndpointTemplate)):
                if k in _cls_endpoints:
                    raise TypeError(f"cls endpoint {k} already defined")
                _cls_endpoints[k] = v

        cls._CLASS_ENDPOINT_TEMPLATES = _cls_endpoints
