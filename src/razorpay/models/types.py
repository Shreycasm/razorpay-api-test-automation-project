from typing import Annotated, Any

from pydantic import Field

Amount = Annotated[int, Field(ge=100)]
Receipt = Annotated[str, Field(max_length=40)]

NotesKey = Annotated[str, Field(max_length=256)]
NotesValue = Annotated[Any, Field(max_length=256)]
Notes = Annotated[dict[NotesKey, NotesValue],Field(max_length=15)]