"""
By default, fast API does not handle converting JSONB to and from Pydantic models.
"""

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Session

from activemodel import BaseModel
from activemodel.mixins import PydanticJSONMixin, TypeIDMixin
from activemodel.session_manager import global_session
from test.models import AnotherExample, ExampleWithComputedProperty


class SubObject(PydanticBaseModel):
    name: str
    value: int


class ExampleWithJSONB(
    BaseModel, PydanticJSONMixin, TypeIDMixin("json_test"), table=True
):
    list_field: list[SubObject] = Field(sa_type=JSONB)
    # list_with_generator: list[SubObject] = Field(sa_type=JSONB)
    optional_list_field: list[SubObject] | None = Field(sa_type=JSONB, default=None)
    generic_list_field: list[dict] = Field(sa_type=JSONB)
    object_field: SubObject = Field(sa_type=JSONB)
    unstructured_field: dict = Field(sa_type=JSONB)
    semi_structured_field: dict[str, str] = Field(sa_type=JSONB)
    optional_object_field: SubObject | None = Field(sa_type=JSONB, default=None)

    normal_field: str | None = Field(default=None)


def test_json_serialization(create_and_wipe_database):
    sub_object = SubObject(name="test", value=1)

    example = ExampleWithJSONB(
        list_field=[sub_object],
        # list_with_generator=(x for x in [sub_object]),
        generic_list_field=[{"one": "two", "three": 3, "four": [1, 2, 3]}],
        optional_list_field=[sub_object],
        object_field=sub_object,
        unstructured_field={"one": "two", "three": 3, "four": [1, 2, 3]},
        normal_field="test",
        semi_structured_field={"one": "two", "three": "three"},
        optional_object_field=sub_object,
    ).save()

    # make sure the types are preserved when saved
    assert isinstance(example.list_field[0], SubObject)
    assert example.optional_list_field
    assert isinstance(example.optional_list_field[0], SubObject)
    assert isinstance(example.object_field, SubObject)
    assert isinstance(example.optional_object_field, SubObject)

    fresh_example = ExampleWithJSONB.get(example.id)

    assert fresh_example is not None
    assert isinstance(fresh_example.object_field, SubObject)
    assert isinstance(fresh_example.optional_object_field, SubObject)
    assert isinstance(fresh_example.generic_list_field, list)
    assert isinstance(fresh_example.generic_list_field[0], dict)
    assert isinstance(fresh_example.list_field[0], SubObject)
    assert fresh_example.optional_list_field
    assert isinstance(fresh_example.optional_list_field[0], SubObject)
    assert isinstance(fresh_example.unstructured_field, dict)


def test_computed_serialization(create_and_wipe_database):
    # count()s are a bit paranoid because I don't understand the sqlalchemy session model yet

    with global_session():
        another_example = AnotherExample(note="test").save()

        example = ExampleWithComputedProperty(
            another_example_id=another_example.id,
        ).save()

        assert ExampleWithComputedProperty.count() == 1
        assert AnotherExample.count() == 1

        # what if the query is done through our magic `select()` method
        example_2 = list(ExampleWithComputedProperty.select().all())[0]

        assert Session.object_session(another_example)
        assert Session.object_session(example)

        example.model_dump_json()
        example_2.model_dump_json()

    assert ExampleWithComputedProperty.count() == 1
    assert AnotherExample.count() == 1
