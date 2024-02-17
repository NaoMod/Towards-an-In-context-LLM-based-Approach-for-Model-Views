import logging
import streamlit as st

from utils.config import Config

logger = logging.getLogger(__name__)

@st.cache_resource(ttl="1h")  # Cache the resource
def configure():
    """
    Parameters
    ----------
    None

    Returns
    -------
    tuple
        A tuple containing the LLM object and the OpenAI key.
    """
    config = Config()
    config.load_keys()
    llm = config.get_llm()
    open_ai_key = config.get_open_ai_key()

    return llm, open_ai_key