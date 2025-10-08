from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat 

load_dotenv()
while True:
    pergunta = input("Insira sua pergunta!\n")
    agente_transporte = Agent(model=OpenAIChat(id="gpt-4o-mini"),markdown=True,stream=True
                            ,instructions="Responda da forma mais arrogante possível")
    if pergunta == "Sair":
        break
    agente_transporte.print_response(pergunta)