from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, field_validator


###########################################################################
# Analyze Request Metadata
###########################################################################


class AnalyzeRequest(BaseModel):
    """
    Metadata accompanying an audio upload.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    reference_text: str | None = Field(
        default=None,
        description="Reference sentence the user was asked to read.",
        max_length=1000,
    )

    language: str = Field(
        default="en",
        description="Language spoken in the audio.",
    )

    @field_validator("reference_text")
    @classmethod
    def validate_reference_text(cls, value: str | None):
        if value is None:
            return value

        if not value.strip():
            return None

        return value.strip()

    @classmethod
    def as_form(
        cls,
        reference_text: Annotated[
            str | None,
            Form(description="Expected sentence (optional)")
        ] = None,
        language: Annotated[
            str,
            Form(description="Language code")
        ] = "en",
    ):
        """
        Enables parsing multipart/form-data directly into Pydantic.
        """
        return cls(
            reference_text=reference_text,
            language=language,
        )