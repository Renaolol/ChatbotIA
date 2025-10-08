from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat 
from agno.knowledge import Knowledge
from agno.tools.knowledge import KnowledgeTools
from agno.knowledge.reader.docx_reader import DocxReader
from agno.tools.file import FileTools
from pathlib import Path
from agno.vectordb.chroma import ChromaDb
from agno.db.sqlite import SqliteDb
from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.chunking.fixed import FixedSizeChunking

load_dotenv()
data_dir = Path(__file__).parent / "data"
doc_paths = list(data_dir.glob("*.docx"))
if not doc_paths:
    raise FileNotFoundError(f"Nenhum DOCX encontrado em {data_dir}")
doc_path = doc_paths[0]

reader = DocxReader(chunking_strategy=FixedSizeChunking(chunk_size=1000, overlap=200))
docs = reader.read(doc_path)            # carrega o conteúdo do DOCX

vector_store = ChromaDb(
    path=str(Path("data/chroma_store")),   # diretório onde o Chroma salva as coleções
    collection="resolucao5867"
)
contents_store = SqliteDb(db_file=str(Path("data/knowledge.sqlite")))  # persistência dos metadados

base_conhecimento = Knowledge(
    vector_db=vector_store,
    contents_db=contents_store,
    max_results=5
)
base_conhecimento.add_content(path=str(doc_path), reader=reader, skip_if_exists=True)
agente_transporte = Agent(model=OpenAIChat(id="gpt-4o-mini"),markdown=True,stream=True,
                        tools=[KnowledgeTools(knowledge=base_conhecimento)], 
                        instructions="Responda somente com base na base de conhecimento carregada. NENHUMA RESPOSTA DEVE SER DADA QUE NÃO SEJA RELACIONADA A BASE DE CONHECIMENTO")
while True:
    pergunta = input("Insira sua pergunta!\n")

    if pergunta == "Sair":
        break
    agente_transporte.print_response(pergunta)