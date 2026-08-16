import json
from functools import cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class SchemaValidator:

    def __init__(
        self,
        schema_directory: Path,
    ) -> None:

        self._schema_directory = schema_directory
        self._registry = Registry(retrieve=self._retrieve_schema)
        self._current_schema_dir: Path | None = None

    @cache
    def _load_schema(
        self,
        schema_path: Path,
    ) -> dict[str, Any]:

        schema_path = self._schema_directory / schema_path

        with schema_path.open(encoding="utf-8") as file:
            return json.load(file)

    def _retrieve_schema(
        self,
        uri: str,
    ) -> Resource:

        if self._current_schema_dir is None:
            raise RuntimeError(
                "Current schema directory has not been set."
            )

        schema_path = (self._current_schema_dir / uri)
        relative_path = schema_path.relative_to(self._schema_directory)
        schema = self._load_schema(relative_path)

        return Resource.from_contents(schema)

    def validate(
        self,
        instance: Any,
        schema_name: Path,
    ) -> None:

        schema = self._load_schema(
            schema_name
        )

        self._current_schema_dir = (
            self._schema_directory / schema_name
        ).parent

        Draft202012Validator(
            schema,
            registry=self._registry,
        ).validate(instance)