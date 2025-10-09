from agno.os import AgentOS
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
import asyncio
from agno.knowledge.reader.docx_reader import DocxReader
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.chunking.fixed import FixedSizeChunking
import streamlit as st

vector_bd = ChromaDb(collection="docx_agent", path="tmp/chromadb")

reader = DocxReader(chunking_strategy=FixedSizeChunking(chunk_size=1000, overlap=200))

knowledge=Knowledge(vector_db=vector_bd)
asyncio.run(knowledge.add_content_async(name="Resolução 5867-2020",path="RESOLUÇÃO Nº 5867-2020.docx", 
            reader=reader))
db = SqliteDb(db_file="tmp/data.db")

assistant = Agent(name="Assistente",
                  model = OpenAIChat(id="gpt-4o-mini"),
                  add_memories_to_context=True,
                  add_history_to_context=True,
                  instructions="SEMPRE DEVE CONSULTAR A BASE DE CONHECIMENTO ANTES DE FORNECER QUALQUER RESPOSTAO",
                  knowledge=knowledge,
                  search_knowledge=True,
                  db=db,
                  markdown=True)

agent_os = AgentOS(id="First",
                       description="Meu primeiro AgentOS",
                       agents=[assistant])

app = agent_os.get_app()
if __name__ == "__main__":

    agent_os.serve(app="Openai:app", reload=True)
