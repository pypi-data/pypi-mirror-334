from typing import ClassVar, Any, Unpack, Callable, Literal
from functools import cached_property
from pydantic import (
    BaseModel,
    SerializerFunctionWrapHandler,
    SerializationInfo,
    model_serializer,
)
from pydantic.fields import FieldInfo
from .dump import DumpKwargs, DumpJsonKwargs


class BaseModelFlagged(BaseModel):
    """
    A BaseModel that introduces the concept of "flagged" fields. Fields whose names
    follow a given pattern are considered flagged.

    By default, a flagged field is defined as one whose name ends with an underscore.
    This can be changed by declaring a custom definition on the class.

    DEFAULT BEHAVIOR CHANGES
    ========================
    By default, this base model does not behave any differently from pydantic.BaseModel.

    BEHAVIOR IN SERIALIZATION
    =========================
    During serialization via .model_dump()/.model_dump_json(), flagged fields can be
    handled in specific ways based on a "mode" setting:

    - "exclude": Exclude flagged fields from serialized output.
    - "include": Only include flagged fields, and exclude everything else.

    This mode can be specified at the class level, or at the time of serialization. The
    mode specified during a dump call takes precedence over the class-level setting.

    These configurations also apply when this model is nested inside a parent that's
    being dumped, even if the parent is a different basemodel with no knowledge of
    flagged fields.

    The class-level setting applies only to the current model. It does not affect nested
    child models. On the other hand, when a dump-level setting is passed, it affects all
    nested models of this type.

    DUMP-LEVEL SETTING
    ------------------
    This class's dump methods accept a parameter to control flagged field serialization.
    But, even if you're serializing a parent model of a different type, you can still
    control the behavior of all nested models by passing a `context` dict (a feature
    already built into Pydantic) to the dump method, with a specific key. The name of the
    key recognized by this class can be customized with a class variable, allowing for
    granular control.
    """

    model_flagged_fields_define: ClassVar[
        Callable[[str], bool] | set[str] | list[str] | tuple[str]
    ] = lambda name: name.endswith("_")
    """
    Class config: Defines what it means for a field to be considered flagged. This can
    either be a function that returns whether a name is flagged, or a list/tuple/set of
    field names.
    """

    model_flagged_fields_ser_mode: ClassVar[Literal["exclude", "include"] | None] = None
    """
    Class config: Default mode for handling flagged fields during serialization:

    - "exclude": Exclude flagged fields from serialized output.
    - "include": Only include flagged fields, and exclude everything else.
    - None: default behavior
    
    This applies even when this model is nested inside a parent that's being serialized.
    """

    model_flagged_fields_ser_mode_context_key: ClassVar[str] = "flagged"
    """
    Class config: Name of the key to look for in the `context` dict during
    serialization, to determine how to handle flagged fields. The value of the
    `flagged` parameter in this class's dump methods (if passed) will be set
    under this name in the `context` dict.

    Keep in mind, the `context` dict propagates down through nested models during
    serialization, so a dump-level setting will override class defaults for all nested
    model instances.
    """

    @cached_property
    def model_flagged_fields(self) -> dict[str, FieldInfo]:
        return self.model_get_flagged_fields()

    @classmethod
    def model_get_flagged_fields(cls) -> dict[str, FieldInfo]:
        """
        Not recommended unless you want to get fields from the class directly.
        The instance property is more efficient and concise.
        """
        is_flagged = cls.model_name_is_flagged
        return {k: v for k, v in cls.model_fields.items() if is_flagged(k)}

    @cached_property
    def model_unflagged_fields(self) -> dict[str, FieldInfo]:
        return self.model_get_unflagged_fields()

    @classmethod
    def model_get_unflagged_fields(cls) -> dict[str, FieldInfo]:
        """
        Not recommended unless you want to get fields from the class directly.
        The instance property is more efficient and concise.
        """
        is_flagged = cls.model_name_is_flagged
        return {k: v for k, v in cls.model_fields.items() if not is_flagged(k)}

    @classmethod
    def model_name_is_flagged(cls, name: str) -> bool:
        """
        Returns whether a given field name is considered flagged according to the
        class-level definition.
        """
        define = cls.model_flagged_fields_define
        return define(name) if callable(define) else name in define

    def model_dump(
        self,
        flagged: Literal["exclude", "include"] | None = None,
        **kwargs: Unpack[DumpKwargs],
    ) -> dict[str, Any]:
        """
        Same as BaseModel.model_dump(), but with a `flagged` option to control how
        flagged fields are handled:

        - "exclude": Exclude flagged fields from serialized output.
        - "include": Only include flagged fields, and exclude everything else.
        - None: default behavior

        This is for convenience, and has the same effect as passing a `context` dict.
        """
        return self._dump_helper(super().model_dump, flagged, **kwargs)

    def model_dump_json(
        self,
        flagged: Literal["exclude", "include"] | None = None,
        **kwargs: Unpack[DumpJsonKwargs],
    ) -> str:
        """
        Same as BaseModel.model_dump_json(), but with a `flagged` option to control how
        flagged fields are handled:

        - "exclude": Exclude flagged fields from serialized output.
        - "include": Only include flagged fields, and exclude everything else.
        - None: default behavior

        This is for convenience, and has the same effect as passing a `context` dict.
        """
        return self._dump_helper(super().model_dump_json, flagged, **kwargs)

    def _dump_helper[**P, R](
        self,
        dump_method: Callable[P, R],
        flagged: Literal["exclude", "include"] | None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        """Shared logic for `model_dump()` and `model_dump_json()`"""
        if flagged is None:
            return dump_method(*args, **kwargs)

        key = self.model_flagged_fields_ser_mode_context_key
        if (context := kwargs.get("context")) is None:
            kwargs["context"] = {key: flagged}
            return dump_method(*args, **kwargs)

        if not isinstance(context, dict):
            raise ValueError(
                "Non-dict `context` prohibited when using `flagged` parameter. Either "
                "leave `context` unset, or make sure it's a dict."
            )
        context[key] = flagged
        return dump_method(*args, **kwargs)

    @model_serializer(mode="wrap", when_used="unless-none")
    def _ser_model(
        self, default_logic: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> dict:
        """Called by Pydantic whenever this instance is being serialized."""
        result = default_logic(self)

        # NOTE: Yes, the following code is ugly. It's goal is to be efficient, because
        # Pydantic (being written in Rust) is so fast during serialization that anything
        # we do here could have a noticeable performance impact.

        # Decide how to handle flagged fields. Prioritize dump-level setting if it's
        # found in the `context` dict, otherwise use the class-level setting.
        context, key, default, missing = (
            info.context,
            self.model_flagged_fields_ser_mode_context_key,
            self.model_flagged_fields_ser_mode,
            object(),
        )

        # Use mode from context if set, otherwise use class-level setting
        if (
            mode := (
                context.get(key, default)
                if context is not None and isinstance(context, dict)
                else default
            )
        ) is not None:
            # Remove fields based on mode
            [
                result.pop(name, missing) is missing
                and result.pop(field.alias, missing) is missing
                and result.pop(field.serialization_alias, None)
                for name, field in (
                    self.model_flagged_fields
                    if mode == "exclude"
                    else self.model_unflagged_fields
                ).items()
            ]

        return result
