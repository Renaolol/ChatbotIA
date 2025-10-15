import asyncio
from openai_agent import build_agent, ensure_doc_loaded


# Executa a indexação manual dos documentos DOCX sem subir a interface
async def main():
    agent = build_agent(preload_knowledge=False)
    await ensure_doc_loaded(agent.knowledge)
    print("Ingestão concluída.")


if __name__ == "__main__":
    asyncio.run(main())
