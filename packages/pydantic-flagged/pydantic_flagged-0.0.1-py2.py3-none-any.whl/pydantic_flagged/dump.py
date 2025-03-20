from typing import TypedDict, Any, Literal, Unpack, TYPE_CHECKING
from pydantic.main import IncEx


class _BaseDumpKwargs(TypedDict, total=False):
    include: IncEx | None
    exclude: IncEx | None
    context: Any | None
    by_alias: bool
    exclude_unset: bool
    exclude_defaults: bool
    exclude_none: bool
    round_trip: bool
    warnings: bool | Literal["none", "warn", "error"]
    serialize_as_any: bool


class DumpKwargs(_BaseDumpKwargs, total=False):
    mode: Literal["json", "python"] | str


class DumpJsonKwargs(_BaseDumpKwargs, total=False):
    indent: int | None


# For type checker to make sure the kwarg types exactly match the actual kwargs taken
# by BaseModel's dump methods
if TYPE_CHECKING:
    from pydantic import BaseModel

    class _TestTypeChecker(BaseModel):
        def test_model_dump(self, **kwargs: Unpack[DumpKwargs]):
            self.model_dump(**kwargs)

        def test_model_dump_json(self, **kwargs: Unpack[DumpJsonKwargs]):
            self.model_dump_json(**kwargs)
