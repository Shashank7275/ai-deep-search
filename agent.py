from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tool import search_web, scrape_url
from dotenv import load_dotenv
import os

try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

load_dotenv()

# Model setup
llm = ChatMistralAI(
    model=os.getenv("MISTRAL_MODEL", " mistral-code-latest"),
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY")
)

# 1st agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[search_web]
    )

# 2nd agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful research papers."
    ),

    (
        "human",
        """Write a detailed research paper on the topic below.

Topic: {topic}

Research Gathered:
{Research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic prompt
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp constructive research critic. Be honest and specific."
    ),

    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{REPORT}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()