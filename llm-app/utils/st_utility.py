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

# A hack to "clear" the previous result when submitting a new prompt. This avoids
# the "previous run's text is grayed-out but visible during rerun" Streamlit behavior.
class DirtyState:
    NOT_DIRTY = "NOT_DIRTY"
    DIRTY = "DIRTY"
    UNHANDLED_SUBMIT = "UNHANDLED_SUBMIT"


def get_dirty_state() -> str:
    return st.session_state.get("dirty_state", DirtyState.NOT_DIRTY)


def set_dirty_state(state: str) -> None:
    st.session_state["dirty_state"] = state


def with_clear_container(submit_clicked: bool) -> bool:
    if get_dirty_state() == DirtyState.DIRTY:
        if submit_clicked:
            set_dirty_state(DirtyState.UNHANDLED_SUBMIT)
            st.experimental_rerun()
        else:
            set_dirty_state(DirtyState.NOT_DIRTY)

    if submit_clicked or get_dirty_state() == DirtyState.UNHANDLED_SUBMIT:
        set_dirty_state(DirtyState.DIRTY)
        return True

    return False