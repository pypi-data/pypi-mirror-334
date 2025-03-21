import inspect
from copy import copy
from types import FunctionType, MethodType, UnionType
from typing import Generic, TypeVar, cast

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError, QuerySet
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
from fastapi import HTTPException, Request
from fastapi.routing import APIRoute
from pydantic import BaseModel

from fango.filters import generate_filterset_by_pydantic
from fango.generics import BaseModelT, ModelT
from fango.permissions import PermissionDependency
from fango.routing import FangoRouter, action
from fango.schemas import PK, ActionClasses
from fango.utils import copy_instance_method


class AsyncGenericViewSet(Generic[BaseModelT]):
    """
    Async Generic ViewSet implementation.

    """

    _internal: FangoRouter
    pydantic_model: BaseModelT
    payload_pydantic_model: BaseModelT | None = None
    queryset: QuerySet
    http_method_names: set[str]
    lookup_value_converter: str = "int"
    pydantic_model_action_classes: ActionClasses = {}
    dependencies = []
    strict_filter_by: str | None = None
    strict_page_size: int | None = None
    read_only: bool = False

    def __init__(
        self,
        router: FangoRouter,
        basename: str,
        strict_filter_by: str | None = None,
        pydantic_model: BaseModelT | None = None,
    ) -> None:
        self.pydantic_model = self.__get_pydantic_model_or_table_action_class()
        self.filterset_class = generate_filterset_by_pydantic(self.pydantic_model)
        self._basename = basename
        self._router = router

        if strict_filter_by:
            self.strict_filter_by = strict_filter_by

        if pydantic_model:
            self.pydantic_model = pydantic_model

        self.__initialize_http_methods()
        self.__initialize_pydantic_model_classes()
        self.__compile_router()

    def __initialize_http_methods(self) -> None:
        ro_methods = {"HEAD", "TRACE", "OPTIONS", "GET"} | {"PATCH"}
        rw_methods = {"POST", "PUT", "DELETE"}

        if (
            hasattr(self, "queryset")
            and (self.queryset.model._meta.managed or not self.read_only)
            and self.payload_pydantic_model
        ):
            self.http_method_names = ro_methods | rw_methods
        else:
            self.http_method_names = ro_methods

    def __initialize_pydantic_model_classes(self) -> None:
        """
        Method for init pydantic_model_action_classes for all viewset routes.

        """
        action_classes = ActionClasses({x.name: self.pydantic_model for x in self._internal.routes})  # type: ignore
        action_classes.update(self.pydantic_model_action_classes)
        self.pydantic_model_action_classes = action_classes

    def __resolve_dependencies_and_permissions(self, route) -> list:
        """
        Merge route, viewset and @action dependencies and
        resolve permissions priority, then use only max permission.

        """
        dependencies = {*route.dependencies, *self._router.dependencies, *self.dependencies}
        all_applied_permissions = {x for x in dependencies if callable(x) and issubclass(x, PermissionDependency)}

        if permission := {x() for x in dependencies if callable(x) and issubclass(x, PermissionDependency)}:
            permission = max(permission).__class__

        return list(dependencies - all_applied_permissions) + [permission]

    def __compile_router(self) -> None:
        """
        Process @internal and @action router per viewset.

        """

        router = copy(self._internal)

        router.tags = [self._basename]
        router.prefix = f"{self._router.prefix}/{self._basename}"

        for route in router.routes:
            route = cast(APIRoute, route)

            if route.name == "rel" and not self.strict_filter_by:
                continue

            if route.methods & self.http_method_names:
                route = copy(route)
                route.dependencies = self.__resolve_dependencies_and_permissions(route)

                if "%" in route.path:
                    route.path = route.path % self.lookup_value_converter
                    route.path_format = route.path_format % self.lookup_value_converter

                route.endpoint = self.__get_route_native_endpoint(route)
                if route.response_model:
                    self.__fix_generic_response_annotations(route)

                route.path = router.prefix + route.path
                route.tags = router.tags
                self._router.routes.append(route)

        for route in action.routes:
            route = cast(APIRoute, route)

            if method := getattr(self, route.name, None):
                route = copy(route)

                if route.endpoint == method.__func__:
                    route.endpoint = self.__get_route_native_endpoint(route)
                    route.dependencies = self.__resolve_dependencies_and_permissions(route)
                    route.path = router.prefix + route.path
                    route.tags = router.tags
                    self._router.routes.append(route)

    def __get_route_native_endpoint(self, route: APIRoute) -> MethodType:
        """
        Method returns route endpoint method from ViewSet instance.

        Any methods with Generic annotated params will be replaced by
        runtime created method and function with true pydantic model.

        """
        function_signature = inspect.signature(cast(FunctionType, route.endpoint))
        method = getattr(self, route.name)

        for param in function_signature.parameters.values():
            if isinstance(param.annotation, TypeVar):
                parameters = function_signature.parameters.copy()

                parameters[param.name] = function_signature.parameters[param.name].replace(
                    annotation=self.payload_pydantic_model or self.pydantic_model
                )
                method = copy_instance_method(method)
                method.__func__.__signature__ = function_signature.replace(parameters=tuple(parameters.values()))

        return method

    def __fix_generic_response_annotations(self, route: APIRoute) -> None:
        """
        Fix generic annotations like T -> MyModel
        Fix iterable generic response annotations like Page[T] -> Page[MyModel]

        """
        pydantic_model = self.pydantic_model_action_classes[route.name]

        if isinstance(route.response_model, TypeVar):
            route.response_model = pydantic_model

        elif not isinstance(route.response_model, UnionType):
            for klass in inspect.getmro(route.response_model)[1:]:
                if issubclass(klass, Generic) and issubclass(klass, BaseModel):
                    if route.response_model.__pydantic_generic_metadata__.get("args"):
                        route.response_model = klass[pydantic_model]  # type: ignore
                    else:
                        route.response_model = klass
                    break

    def __get_pydantic_model_or_table_action_class(self) -> BaseModelT:
        """
        Method for get pydantic model from pydantic_model attr or action class.

        """
        if (
            not hasattr(self, "pydantic_model")
            and hasattr(self, "pydantic_model_action_classes")
            and "list" in self.pydantic_model_action_classes
        ):
            return self.pydantic_model_action_classes["list"]

        elif hasattr(self, "pydantic_model"):
            return self.pydantic_model

        else:
            raise Exception("Method has no pydantic_model.")

    def get_pydantic_model_class(self, request: Request) -> BaseModelT:
        """
        Method for get concrete pydantic_model for route.

        """
        route_name = request.scope["route"].name

        if model := self.pydantic_model_action_classes.get(route_name):
            return model
        else:
            return self.__get_pydantic_model_or_table_action_class()

    async def get_queryset(self, request: Request) -> QuerySet:
        """
        Method for get queryset defined in ViewSet.

        """
        return self.queryset


class CRUDMixin(Generic[BaseModelT, ModelT]):
    queryset: QuerySet

    async def create_entry(self, request: Request, payload: BaseModelT) -> ModelT:
        """
        Method for create new entry.

        """
        return await self.queryset.model.save_from_schema(payload)

    async def update_entry(self, request: Request, payload: BaseModelT, pk: PK) -> ModelT:
        """
        Method for update entry.

        """
        return await self.queryset.model.save_from_schema(payload, pk)

    async def delete_entry(self, request: Request, pk: PK) -> None:
        """
        Method for delete entry.

        """
        try:
            instance = await self.queryset.aget(pk=pk)
            await instance.adelete()

        except ProtectedError as e:
            label = self.queryset.model._meta.verbose_name
            relations = "; ".join(f"{x._meta.verbose_name} id={x.pk}" for x in e.protected_objects)

            raise HTTPException(
                status_code=400,
                detail=f"Can't delete object {label} id={pk} by protected relations: {relations}",
            )

        except ObjectDoesNotExist:
            label = self.queryset.model._meta.verbose_name

            raise HTTPException(
                status_code=204,  # FIXME: поправить на 404
                detail=_(f"Object {label} id={pk} is not found."),
            )

    async def add_or_remove_rel(self, object_id: PK, field: str, pk: PK) -> None:
        """
        Method for add or remove relation.

        """
        descriptor = getattr(self.queryset.model, field)
        parent = await descriptor.field.model.objects.aget(pk=object_id)

        rel = getattr(parent, descriptor.field.name)
        try:
            if not await rel.filter(pk=pk).aexists():
                await rel.aadd(pk)
            else:
                await rel.aremove(pk)
        except IntegrityError:
            label = self.queryset.model._meta.verbose_name

            raise HTTPException(
                status_code=404,
                detail=_(f"Object {label} id={pk} is not found."),
            )
