import logging

from django.conf import settings
from django.core.files.base import ContentFile

from .models import MovieNightImage, MovieSuggestion

logger = logging.getLogger(__name__)


def generate_movie_night_image():
    import anthropic
    from google import genai
    from google.genai.types import GenerateContentConfig

    titles = list(MovieSuggestion.objects.values_list("title", flat=True))
    if not titles:
        return

    claude = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    prompt_response = claude.messages.create(
        model="claude-opus-4-8",
        max_tokens=300,
        system=(
            "You write vivid, single-paragraph prompts for an AI image generator. "
            "Given a list of movie titles suggested by a group for movie night, "
            "write one descriptive image prompt for a poster-style collage that "
            "captures the mood and variety of the list. Do not render the titles "
            "as literal text in the image. Respond with only the prompt, no preamble."
        ),
        messages=[{"role": "user", "content": ", ".join(titles)}],
    )
    image_prompt = next(b.text for b in prompt_response.content if b.type == "text")

    client = genai.Client(
        vertexai=True,
        project=settings.GOOGLE_CLOUD_PROJECT,
        location=settings.VERTEX_AI_LOCATION,
    )
    result = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=image_prompt,
        config=GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
    )
    image_bytes = next(
        part.inline_data.data
        for part in result.candidates[0].content.parts
        if part.inline_data is not None
    )

    movie_image = MovieNightImage(prompt_used=image_prompt)
    movie_image.image.save("movienight.png", ContentFile(image_bytes), save=True)
