"""Tests for `oold` package."""

import importlib
from typing import Any

import datamodel_code_generator

import oold.model.model as model
from oold.generator import Generator


def _run(pydantic_version="v1"):
    if pydantic_version == "v1":
        from oold.model.v1 import (
            ResolveParam,
            Resolver,
            ResolveResult,
            SetResolverParam,
            set_resolver,
        )

        output_model_type = datamodel_code_generator.DataModelType.PydanticBaseModel
    else:
        from oold.model import (
            ResolveParam,
            Resolver,
            ResolveResult,
            SetResolverParam,
            set_resolver,
        )

        output_model_type = datamodel_code_generator.DataModelType.PydanticV2BaseModel

    """Tests for `oold` package."""

    schemas = [
        {
            "id": "./bar2/Bar2",
            "title": "Bar2",
            "type": "object",
            "properties": {
                "type": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["Bar2"],
                },
                "prop1": {"type": "string"},
            },
        },
        {
            "id": "Bar",
            "title": "Bar",
            "type": "object",
            "allOf": [{"$ref": "./bar2/Bar2.json"}],
            "properties": {
                "type": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["Bar"],
                },
                "prop1": {"type": "string"},
            },
        },
        {
            "id": "Foo",
            "title": "Foo",
            "type": "object",
            "properties": {
                "type": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["Foo"],
                },
                "literal": {"type": "string"},
                "b": {"type": "string", "range": "Bar.json"},
                "b2": {
                    "type": "array",
                    "items": {"type": "string", "range": "Bar.json"},
                },
            },
        },
    ]
    graph = [
        {"id": "ex:a", "type": ["Foo"], "literal": "test1", "b": "ex:b"},
        {"id": "ex:b", "type": ["Bar"], "prop1": "test2"},
        {"id": "ex:b1", "type": ["Bar"], "prop1": "test3"},
        {"id": "ex:b2", "type": ["Bar"], "prop1": "test4"},
    ]

    g = Generator()
    g.generate(schemas, main_schema="Foo.json", output_model_type=output_model_type)
    importlib.reload(model)

    class MyResolver(Resolver):
        graph: (Any)

        def resolve_iri(self, iri):
            for node in self.graph:
                if node["id"] == iri:
                    cls = node["type"][0]
                    entity = eval(f"model.{cls}(**node)")
                    return entity

        def resolve(self, request: ResolveParam):
            # print("RESOLVE", request)
            nodes = {}
            for iri in request.iris:
                nodes[iri] = self.resolve_iri(iri)
            return ResolveResult(nodes=nodes)

    r = MyResolver(graph=graph)
    set_resolver(SetResolverParam(iri="ex", resolver=r))

    f = model.Foo(id="ex:f", b="ex:b", b2=["ex:b1", "ex:b2"])
    print(f.b)

    print(f.b.id)
    assert f.b.id == "ex:b"
    for b in f.b2:
        print(b)
    assert f.b2[0].id == "ex:b1" and f.b2[0].prop1 == "test3"
    assert f.b2[1].id == "ex:b2" and f.b2[1].prop1 == "test4"


def test_core():
    _run(pydantic_version="v1")
    _run(pydantic_version="v2")


if __name__ == "__main__":
    test_core()
