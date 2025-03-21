from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from fango.viewsets import AsyncGenericViewSet

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class FangoRouter(APIRouter):
    viewsets = []

    def get(self, *args, **kwargs) -> Callable:
        response_model_exclude_unset = kwargs.pop("response_model_exclude_unset", True)
        return super().get(*args, **kwargs, response_model_exclude_unset=response_model_exclude_unset)

    def register(
        self,
        basename: str,
        viewset: type["AsyncGenericViewSet"],
        strict_filter_by: str | None = None,
        pydantic_model: type[BaseModel] | None = None,
    ) -> None:
        """
        Register viewset.

        """
        vs = viewset(
            self,
            basename,
            strict_filter_by=strict_filter_by,
            pydantic_model=pydantic_model,
        )
        self.viewsets.append(vs)


action = FangoRouter()
