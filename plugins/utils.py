import base64
from io import BytesIO
import httpx

cl = httpx.AsyncClient(base_url='https://api.codeltix.com' , follow_redirects=True , timeout=20)
async def get_ai_response(history: list[dict[str, str]]) -> str:
    """
    Get the AI response for the given history of messages.

    Args:
        history: A list of dictionaries with 'role' and 'content' keys
            representing the conversation history.

    Returns:
        The AI response as a string.

    Raises:
        httpx.HTTPStatusError: If the server returns an unsuccessful status code.
        httpx.RequestError: If a network error occurs.
        Exception: If any other unexpected error occurs.
    """
    try:
        response = await cl.post('/ai', json={'history': history})
        response.raise_for_status()
        reply = response.json().get("message", "No response text found")
        source = response.json().get("source", None)
        source_title = response.json().get("source_title", None)
        if source and source_title:
            reply += f"\n\nSource: <a href='{source}'>{source_title}</a>"
        return reply
    except httpx.HTTPStatusError as exc:
        print(f'HTTP error occurred: {exc}')
    except httpx.RequestError as exc:
        print(f'Request error occurred: {exc}')
    except Exception as exc:
        print(f'An unexpected error occurred: {exc}')
    return 'I\'m sorry, I\'m not able to respond to that right now.'
