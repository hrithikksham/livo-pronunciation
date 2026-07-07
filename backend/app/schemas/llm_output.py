
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


###########################################################################
# LLM Mistake
###########################################################################


class LLMMistake(BaseModel):
    """
    Individual pronunciation issue identified by the LLM.
    """

    model_config = ConfigDict(extra="forbid")

    word: str = Field(..., min_length=1)

    issue_type: Literal[
        "mispronunciation",
        "stress",
        "intonation",
        "fluency",
        "omission",
        "insertion",
        "unclear",
    ]

    explanation: str = Field(..., min_length=5)

    suggestion: str = Field(..., min_length=5)


###########################################################################
# LLM Score Breakdown
###########################################################################


class LLMScoreBreakdown(BaseModel):
    """
    Scores returned by the LLM.
    """

    model_config = ConfigDict(extra="forbid")

    clarity: int = Field(..., ge=0, le=100)

    fluency: int = Field(..., ge=0, le=100)

    word_accuracy: int = Field(..., ge=0, le=100)


###########################################################################
# LLM Output
###########################################################################


class LLMOutput(BaseModel):
    """
    Complete JSON expected from the LLM.
    """

    model_config = ConfigDict(extra="forbid")

    score_breakdown: LLMScoreBreakdown

    mistakes: list[LLMMistake] = Field(default_factory=list)

    overall_feedback: str = Field(
        ...,
        min_length=10,
        max_length=500,
    )