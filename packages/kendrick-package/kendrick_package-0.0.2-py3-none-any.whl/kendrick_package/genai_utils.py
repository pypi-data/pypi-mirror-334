from semantic_router import Route
from semantic_router.encoders import OpenAIEncoder
from semantic_router.layer import RouteLayer
from typing import List
import nest_asyncio
import os

nest_asyncio.apply()
encoder = OpenAIEncoder(name="text-embedding-3-small")

# Semantic router
politics = Route(
    name="politics",
    utterances=[
        "isn't politics the best thing ever",
        "why don't you tell me about your political opinions",
        "don't you just love the president",
        "don't you just hate the president",
        "they're going to destroy this country!",
        "they will save the country!",
        "Who is obama?",
        "Tại sao Mỹ lại mạnh hơn Việt Nam",
        "Mua bán vũ khí",
        "Chiến dịch tranh cử của Trump như nào?",
    ],
)
chitchat = Route(
    name="chitchat",
    utterances=[
        "how's the weather today?",
        "how are things going?",
        "lovely weather today",
        "the weather is horrendous",
        "let's go to the chippy",
    ],
)
routes = [politics, chitchat]

semantic_router = RouteLayer(encoder=encoder, routes=routes)


def _get_session():
    from streamlit.runtime import get_instance
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session
