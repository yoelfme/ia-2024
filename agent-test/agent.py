from typing import List

from langchain_openai import ChatOpenAI # LLM class
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # Prompt
from langchain.agents import AgentExecutor, create_openai_functions_agent
from fastapi import FastAPI
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from langserve import add_routes

from tools.word_counter import get_word_length # Tool

# Agent
llm = ChatOpenAI(model="gpt-3.5-turbo") # LLM model instance
tools = [get_word_length] # Define tools list

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# Server
app = FastAPI(
    title="Word Counter Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces and agents",
)

class Input(BaseModel):
    input: str
    chat_history: List[BaseMessage] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "location"}},
    )

class Output(BaseModel):
    output: str

add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output),
    path="/agent",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)