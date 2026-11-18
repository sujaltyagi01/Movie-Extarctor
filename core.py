
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()


# Pydantic Model
class Movie(BaseModel):
    title: str
    director: Optional[str] = None
    release: Optional[int] = None
    summary: str
    description: str
    rating: Optional[float] = None


# Output Parser
parser = PydanticOutputParser(pydantic_object=Movie)


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set.")


model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key
)


# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a professional Movie Information Extraction Assistant.

Extract structured information from the user's movie or series description.

Rules:
- Do not guess unknown facts.
- If information is missing, use null.
- Keep the summary within 2-3 lines.
- Return only structured output.

{format_instructions}
"""),

    ("human", """
Extract information from this paragraph:

{paragraph}
""")
])


# User Input
paragraph = input("\nGive your movie/series description: ")


# Create Prompt
final_prompt = prompt.invoke({
    "paragraph": paragraph,
    "format_instructions": parser.get_format_instructions()
})


# Get LLM Response
response = model.invoke(final_prompt)


# Parse Response
result = parser.parse(response.content)


print("\nMovie/Series Information:")
print(result.model_dump_json(indent=4))
