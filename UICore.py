
import os
import json
import streamlit as st

from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# Load .env from parent folder
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Check API key
api_key = os.getenv("GROQ_API_KEY")


# ---------------------------------------------------------------- PAGE SETUP

st.set_page_config(
    page_title="Movie Extractor",
    page_icon="🎬",
    layout="wide"
)


FIELDS = [
    "Movie Title", "Release Year", "Genre", "Director", "Main Cast",
    "Setting/Location", "Plot", "Themes", "Ratings", "Notable Features",
    "Short Summary",
]


SYSTEM_PROMPT = """
You are a professional Movie Information Extraction Assistant.

Your task:
Extract useful structured information from a movie or series
description provided by the user.

Rules:
- Do NOT add explanations.
- Do NOT add extra commentary.
- Follow the exact output format.
- If information is missing, write "Not available".
- Do NOT guess unknown facts.
- Keep the Short Summary to 2-3 lines maximum.

Output Format:

Movie Title:
Release Year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""


HUMAN_PROMPT = """
Extract information from this paragraph:

{paragraph}
"""


EXAMPLE = (
    "Inception is a 2010 science fiction thriller directed by Christopher Nolan, "
    "starring Leonardo DiCaprio, Joseph Gordon-Levitt and Elliot Page. A thief who "
    "steals secrets through dream-sharing technology is hired to plant an idea in a "
    "CEO's mind. The film explores reality, guilt and memory, and is known for its "
    "layered dream sequences and Hans Zimmer's score. It holds an 8.8 rating on IMDb."
)


# ---------------------------------------------------------------- HELPERS

@st.cache_resource(show_spinner=False)
def get_model(api_key: str, model_name: str):

    return ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0
    )


def run_extraction(api_key, model_name, paragraph):

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT)
    ])

    model = get_model(api_key, model_name)

    final_prompt = prompt.invoke({
        "paragraph": paragraph
    })

    response = model.invoke(final_prompt)

    return response.content


def parse_output(text: str) -> dict:

    """Convert Label: Value output into a dictionary."""

    data = {f: "" for f in FIELDS}
    current = None

    for line in text.splitlines():

        matched = False

        for f in FIELDS:

            if line.strip().lower().startswith(f.lower() + ":"):

                current = f
                data[f] = line.split(":", 1)[1].strip()
                matched = True
                break

        if not matched and current and line.strip():

            data[current] += (
                " " if data[current] else ""
            ) + line.strip()

    return {
        k: (v or "Not available")
        for k, v in data.items()
    }


def split_list(value: str) -> list:

    """Split A, B and C into a list."""

    if value == "Not available":
        return [value]

    return [
        p.strip()
        for p in value.replace(" and ", ", ").split(",")
        if p.strip()
    ]


def card(label, value, icon):

    with st.container(border=True):

        st.caption(f"{icon}  {label.upper()}")

        st.markdown(
            f"**{value}**" if len(value) < 60 else value
        )


def list_card(label, value, icon):

    """Display list items on separate lines."""

    with st.container(border=True):

        st.caption(f"{icon}  {label.upper()}")

        st.markdown(
            "\n".join(f"- {item}" for item in split_list(value))
        )


# ---------------------------------------------------------------- SESSION STATE

st.session_state.setdefault("history", [])
st.session_state.setdefault("text", "")


# ---------------------------------------------------------------- SIDEBAR

with st.sidebar:

    st.header("⚙️ Settings")

    model_name = st.selectbox(
        "Model",
        [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "llama-3.3-70b-versatile"
        ]
    )

    st.divider()

    st.subheader("🕘 History")

    if not st.session_state.history:

        st.caption("Nothing yet. Your extractions will appear here.")

    for i, item in enumerate(reversed(st.session_state.history)):

        title = item["data"]["Movie Title"]

        if st.button(
            f"🎞️ {title[:28]}",
            key=f"hist_{i}",
            use_container_width=True
        ):

            st.session_state.selected = item

    if st.session_state.history and st.button(
        "Clear history",
        use_container_width=True
    ):

        st.session_state.history = []

        st.session_state.pop("selected", None)

        st.rerun()


# ---------------------------------------------------------------- MAIN UI

st.title("🎬 Movie / Series Information Extractor")

st.caption(
    "Paste a description and get clean, structured details back."
)


col_a, col_b = st.columns([4, 1])

with col_b:

    if st.button("Load example", use_container_width=True):

        st.session_state.text = EXAMPLE

        st.rerun()


paragraph = st.text_area(
    "Movie / series description",
    key="text",
    height=180,
    placeholder="Paste a paragraph about a movie or series here..."
)


extract = st.button(
    "✨ Extract information",
    type="primary"
)


# ---------------------------------------------------------------- EXTRACTION

if extract:

    if not api_key:

        st.error("GROQ_API_KEY is not set. Please check your .env file.")

    elif not paragraph.strip():

        st.warning("Please enter a description first.")

    else:

        with st.spinner("Extracting movie information..."):

            try:

                raw = run_extraction(
                    api_key,
                    model_name,
                    paragraph
                )

                entry = {
                    "raw": raw,
                    "data": parse_output(raw)
                }

                st.session_state.history.append(entry)

                st.session_state.selected = entry

            except Exception as e:

                st.error(f"Something went wrong: {e}")


# ---------------------------------------------------------------- RESULTS

result = st.session_state.get("selected")

if result:

    d = result["data"]

    st.divider()

    st.header(d["Movie Title"])

    st.info(
        d["Short Summary"],
        icon="📝"
    )


    # Movie details in two columns

    left, right = st.columns(2)

    with left:

        card("Release Year", d["Release Year"], "📅")

        card("Genre", d["Genre"], "🎭")

        card("Director", d["Director"], "🎥")

        card("Ratings", d["Ratings"], "⭐")


    with right:

        list_card("Main Cast", d["Main Cast"], "👥")

        card(
            "Setting / Location",
            d["Setting/Location"],
            "📍"
        )


    card("Plot", d["Plot"], "📖")


    c7, c8 = st.columns(2)

    with c7:

        list_card("Themes", d["Themes"], "💡")

    with c8:

        card(
            "Notable Features",
            d["Notable Features"],
            "🏆"
        )


    # ---------------------------------------------------------------- EXPORT

    st.subheader("Export")

    e1, e2, _ = st.columns([1, 1, 4])

    e1.download_button(
        "⬇️ JSON",
        json.dumps(d, indent=2, ensure_ascii=False),
        file_name="movie_info.json",
        mime="application/json"
    )

    e2.download_button(
        "⬇️ Text",
        result["raw"],
        file_name="movie_info.txt",
        mime="text/plain"
    )


    with st.expander("Raw model output"):

        st.code(
            result["raw"],
            language="text"
        )
