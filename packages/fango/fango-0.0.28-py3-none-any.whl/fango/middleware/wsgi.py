import typing

from starlette.middleware.wsgi import WSGIResponder
from starlette.types import Receive, Scope, Send


class CustomWSGIMiddleware:
    def __init__(self, app: typing.Callable[..., typing.Any]) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "http"
        try:
            responder = WSGIResponder(self.app, scope)
            await responder(receive, send)
        except Exception as task_group:
            for exc in task_group.exceptions:
                raise exc
