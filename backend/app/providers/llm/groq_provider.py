"""
Groq LLM Provider.

Concrete implementation of the LLMProvider interface.

Author: Hrithik
"""

from __future__ import annotations

import json

from groq import AsyncGroq
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import (
    InvalidLLMResponse,
    LLMProviderError,
)
from app.core.logging import get_logger

from app.prompts.system_prompt import SYSTEM_PROMPT
from app.prompts.user_prompt import build_user_prompt

from app.providers.llm.base import LLMProvider

from app.schemas.common import AnalysisContext
from app.schemas.llm_output import LLMOutput

logger = get_logger(__name__)


class GroqProvider(LLMProvider):

    provider_name = "groq"

    model_name = "llama-3.3-70b-versatile"

    def __init__(self):

        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

    async def evaluate(
        self,
        context: AnalysisContext,
    ) -> LLMOutput:

        prompt = build_user_prompt(context)

        #######################################################################
        # Call Groq
        #######################################################################

        try:

            response = await self.client.chat.completions.create(
                model=self.model_name,
                temperature=0.2,
                response_format={
                    "type": "json_object",
                },
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

        except Exception:

            logger.exception("Groq LLM request failed.")

            raise LLMProviderError()

        #######################################################################
        # Parse response
        #######################################################################

        try:

            content = response.choices[0].message.content

            if content is None:
                raise InvalidLLMResponse(
                    "Groq returned empty content."
                )

            logger.info(
                "Raw LLM Response:\n%s",
                content,
            )

            # Remove markdown code fences if present
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            data = json.loads(content)

            logger.info(
                "Parsed JSON successfully."
            )

            result = LLMOutput.model_validate(data)

            logger.info(
                "LLMOutput validated successfully."
            )

            return result

        except ValidationError as exc:

            logger.exception(
                "LLMOutput validation failed."
            )

            logger.error(
                "Validation errors: %s",
                exc.errors(),
            )

            raise InvalidLLMResponse() from exc

        except json.JSONDecodeError as exc:

            logger.exception(
                "Invalid JSON returned by LLM."
            )

            logger.error(
                "Content was:\n%s",
                content,
            )

            raise InvalidLLMResponse() from exc

        except Exception as exc:

            logger.exception(
                "Unexpected LLM parsing error."
            )

            raise InvalidLLMResponse() from exc