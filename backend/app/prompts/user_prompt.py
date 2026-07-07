from app.schemas.common import AnalysisContext


def build_user_prompt(context: AnalysisContext) -> str:
    reference_section = (
        context.reference_text.strip()
        if context.reference_text and context.reference_text.strip()
        else "(none provided — this is free speech, evaluate pronunciation only, not content accuracy)"
    )

    if context.flagged_words:
        flagged_section = "\n".join(
            f"- \"{word.word}\" — {word.issue_type}"
            for word in context.flagged_words
        )
    else:
        flagged_section = "(none — no low-confidence or mismatched words detected)"

    return f"""Reference Text:
{reference_section}

Transcript:
{context.transcript.strip()}

Flagged Words:
{flagged_section}

Evaluate this transcript for pronunciation, clarity, and fluency only.
Base every mistake strictly on the Flagged Words list above — if it says "none," return an empty mistakes array.
Return only the JSON object specified in your instructions.
"""