from collections.abc import Collection
from typing_extensions import Self

from immundata.backend.base import BaseBackend
from immundata.models import Operation


class ImmunData:
    _backend: BaseBackend
    _operations: Collection[Operation]

    def __init__(self, backend: BaseBackend, operations:Collection[Operation]) -> None:
        self._backend = backend
        self._operations = operations

    def _apply_operation(self, op_name: str, *args, **kwargs) -> Self:
        new_operation = Operation(name=op_name, args=args, kwargs=kwargs)
        return self.__class__(self._backend, [*self._operations, new_operation])

    # def collect(self, *args, **kwargs) -> Any:
    #     raise NotImplementedError
    #     # apply all operations and get data to the RAM

    # def compute(self, *args, **kwargs) -> Self:
    #     raise NotImplementedError
    #     # apply all operations and get data back to the source

    def agg(self, *args, **kwargs) -> Self:
        return self._apply_operation("agg", *args, **kwargs)

    def filter(self, *args, **kwargs) -> Self:
        return self._apply_operation("filter", *args, **kwargs)

    def group_by(self, *args, **kwargs) -> Self:
        return self._apply_operation("group_by", *args, **kwargs)

    def select(self, *args, **kwargs) -> Self:
        return self._apply_operation("select", *args, **kwargs)

    def sort(self, *args, **kwargs) -> Self:
        return self._apply_operation("sort", *args, **kwargs)

    def with_columns(self, *args, **kwargs) -> Self:
        return self._apply_operation("with_columns", *args, **kwargs)
