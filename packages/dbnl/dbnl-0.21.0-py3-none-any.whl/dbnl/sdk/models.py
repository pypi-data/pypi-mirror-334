from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Generic, Literal, NamedTuple, Optional, TypedDict, TypeVar, Union

import pandas as pd
from dataclasses_json import DataClassJsonMixin
from typing_extensions import NotRequired, Self, override

REPR_INDENT = 4


@dataclass(repr=False)
class DBNLObject(DataClassJsonMixin):
    def __repr__(self) -> str:
        return self._pretty_print()

    def _pretty_print(self, nested_indent: int = 0) -> str:
        field_reprs = []
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, list):
                value_repr = " " * (
                    2 * REPR_INDENT + nested_indent
                ) + f",\n{' ' * (2 * REPR_INDENT + nested_indent)}".join([f"{d}" for d in value])
                field_reprs.append(f"{field.name}=[\n{value_repr}\n{' ' * (REPR_INDENT + nested_indent)}]")
            elif isinstance(value, dict):
                value_repr = " " * (
                    2 * REPR_INDENT + nested_indent
                ) + f",\n{' ' * (2 * REPR_INDENT + nested_indent)}".join([
                    f"'{k}': {repr(v)}" for k, v in value.items()
                ])
                field_reprs.append(
                    f"{field.name}=" + "{" + f"\n{value_repr}\n{' ' * (REPR_INDENT + nested_indent)}" + "}"
                )
            elif isinstance(value, DBNLObject):
                field_reprs.append(f"{field.name}={value._pretty_print(nested_indent=REPR_INDENT)}")
            else:
                field_reprs.append(f"{field.name}={repr(value)}")
        return (
            f"{self.__class__.__name__}(\n{' ' * (REPR_INDENT + nested_indent)}"
            + f",\n{' ' * (REPR_INDENT + nested_indent)}".join(field_reprs)
            + f"\n{' ' * nested_indent})"
        )


class _BaseFieldSchemaDict(TypedDict):
    name: str
    description: NotRequired[str | None]
    component: NotRequired[str | None]
    greater_is_better: NotRequired[bool | None]


PrimitiveTypeLiteral = Literal["boolean", "int", "long", "float", "double", "string", "category"]
ContainerTypeLiteral = Literal["list"]


class _PrimitiveFieldSchemaDict(_BaseFieldSchemaDict):
    type: PrimitiveTypeLiteral


class _FieldSchemaValueTypeDict(TypedDict):
    type: Literal["string"]


class _ContainerFieldSchemaDict(_BaseFieldSchemaDict):
    type: ContainerTypeLiteral
    value_type: NotRequired[_FieldSchemaValueTypeDict]


class PrimitiveColumnSchemaDict(_PrimitiveFieldSchemaDict):
    pass


class ContainerColumnSchemaDict(_ContainerFieldSchemaDict):
    pass


ColumnSchemaDict = Union[PrimitiveColumnSchemaDict, ContainerColumnSchemaDict]


class PrimitiveScalarSchemaDict(_PrimitiveFieldSchemaDict):
    pass


class ContainerScalarSchemaDict(_ContainerFieldSchemaDict):
    pass


ScalarSchemaDict = Union[PrimitiveScalarSchemaDict, ContainerScalarSchemaDict]


@dataclass(repr=False)
class Project(DBNLObject):
    id: str
    name: str
    description: Optional[str] = None


@dataclass(repr=False)
class _FieldSchemaValueType(DBNLObject):
    type: str


C = TypeVar("C", bound=Union[ColumnSchemaDict, ScalarSchemaDict])


@dataclass(repr=False)
class _FieldSchema(DBNLObject, Generic[C]):
    name: str
    type: str
    value_type: Optional[_FieldSchemaValueType] = None
    description: Optional[str] = None
    component: Optional[str] = None
    greater_is_better: Optional[bool] = None

    # NOTE: intentionally changed the signature to only accept FieldSchemaDict
    @classmethod
    @override
    def from_dict(
        cls,
        kvs: C,  # type: ignore[override]
        *,
        infer_missing: Any = False,
    ) -> Self:
        if isinstance(kvs, dict):
            return super().from_dict(dict(kvs), infer_missing=infer_missing)
        raise ValueError(f"Unsupported type for {cls.__name__}: {type(kvs)}")


class ColumnSchema(_FieldSchema[ColumnSchemaDict]):
    pass


class ScalarSchema(_FieldSchema[ScalarSchemaDict]):
    pass


@dataclass(repr=False)
class RunConfig(DBNLObject):
    id: str
    project_id: str
    columns: list[ColumnSchema]
    scalars: Optional[list[ScalarSchema]] = None
    description: Optional[str] = None
    display_name: Optional[str] = None
    row_id: Optional[list[str]] = None
    components_dag: Optional[dict[str, list[str]]] = None


@dataclass(repr=False)
class Run(DBNLObject):
    id: str
    project_id: str
    run_config_id: str
    display_name: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    run_config: Optional[RunConfig] = None


@dataclass(repr=False)
class RunQuery(DBNLObject):
    id: str
    project_id: str
    name: str
    query: dict[str, Any]


class AssertionDict(TypedDict):
    name: str
    params: dict[str, float | int | str]


class TestSpecDict(TypedDict):
    project_id: str
    name: str
    statistic_name: str
    statistic_params: dict[str, float | int | str]
    statistic_inputs: list[dict[str, Any]]
    assertion: AssertionDict
    description: NotRequired[str]
    tag_ids: NotRequired[list[str]]


class ResultData(NamedTuple):
    columns: pd.DataFrame
    scalars: Union[pd.DataFrame, None] = None


@dataclass(repr=False)
class TestSessionInput(DBNLObject):
    run_alias: str
    run_id: Optional[str] = None
    run_query_id: Optional[str] = None

    @override
    def to_dict(self, encode_json: bool = False) -> dict[str, Any]:
        return {k: v for k, v in super().to_dict(encode_json).items() if v is not None}


@dataclass(repr=False)
class TestSession(DBNLObject):
    id: str
    project_id: str
    inputs: list[TestSessionInput]
    status: Literal["PENDING", "RUNNING", "PASSED", "FAILED"]
    failure: Optional[str] = None
    num_tests_passed: Optional[int] = None
    num_tests_failed: Optional[int] = None
    num_tests_errored: Optional[int] = None
    include_tag_ids: Optional[list[str]] = None
    exclude_tag_ids: Optional[list[str]] = None
    require_tag_ids: Optional[list[str]] = None


@dataclass(repr=False)
class TestGenerationSession(DBNLObject):
    id: str
    project_id: str
    run_id: str
    status: Literal["PENDING", "RUNNING", "COMPLETED", "FAILED"]
    columns: Optional[list[dict[str, str]]] = None
    failure: Optional[str] = None
    num_generated_tests: Optional[int] = None


@dataclass(repr=False)
class TestRecalibrationSession(DBNLObject):
    id: str
    project_id: str
    test_session_id: str
    feedback: str
    status: Literal["PENDING", "RUNNING", "COMPLETED", "FAILED"]
    test_ids: Optional[list[str]] = None
    failure: Optional[str] = None
