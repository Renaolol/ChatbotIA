# Chatbot IA – Assistente Jurídico de Transporte

Este projeto implementa um chatbot especializado em legislação de transporte, com interface em Streamlit, autenticação básica por formulário e base de conhecimento alimentada a partir de arquivos `.docx`. O agente combina **Agno** (framework de agentes), **ChromaDB** para vetorizar documentos e a API da OpenAI para geração de respostas fundamentadas na base carregada.

## 📁 Estrutura do Projeto
- `streamlit_app.py` – Interface principal do chatbot com fluxo de login.
- `openai_agent.py` – Monta o agente, carrega a base de conhecimento e define instruções.
- `ingest_docx.py` – Script para indexar novos documentos `.docx` no vetor de conhecimento.
- `data/` – Diretório esperado para os arquivos `.docx` que alimentam a base.
- `tmp/` – Diretório usado para o banco SQLite e a coleção Chroma.
- `.env` – Configuração de segredos e credenciais (não versionado).
- `requirements.txt` – Dependências com versões fixas.

## ✅ Pré-requisitos
- Python 3.11+ (recomendado utilizar ambiente virtual).
- Conta com acesso à API da OpenAI.
- Documentos `.docx` contendo os textos legais que servirão de base.

## ⚙️ Configuração do Ambiente
1. **Clone o repositório** (ou faça o download do código).
2. **Crie e ative** um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure o `.env`** na raiz do projeto:
   ```env
   OPENAI_API_KEY=seu_token_openai
   APP_USERS=usuario:senha;outro:senha2
   ```
   - `OPENAI_API_KEY`: chave da OpenAI.
   - `APP_USERS`: pares `usuario:senha` separados por `;`. Esses usuários terão acesso ao chatbot.

## 📚 Ingestão da Base de Conhecimento
1. Copie os arquivos `.docx` para a pasta `data/`.
2. Execute o script de ingestão (somente se ainda não tiver indexado ou houver novos documentos):
   ```bash
   python ingest_docx.py
   ```
   O script criará/atualizará os embeddings no diretório `tmp/chromadb`.

## 💬 Executando o Chatbot
1. Certifique-se de que o `.env` está preenchido e os documentos indexados.
2. Rode o app Streamlit:
   ```bash
   streamlit run streamlit_app.py --server.port=801
   ```
3. Acesse a URL que o Streamlit indicar (por padrão `http://localhost:801`).
4. Informe usuário e senha configurados em `APP_USERS`. Após login bem-sucedido, o chatbot fica disponível para consultas.

## 🚢 Executando com Docker
O repositório inclui um `Dockerfile` pronto para publicação em serviços como o EasyPanel.

1. **Monte a imagem**:
   ```bash
   docker build -t chatbot-ia .
   ```
2. **Execute o container** apontando para os diretórios de dados e definindo as variáveis de ambiente:
   ```bash
   docker run -p 801:801 \
     -e OPENAI_API_KEY=seu_token_openai \
     -e APP_USERS="usuario:senha;outro:senha2" \
     -v /caminho/para/data:/app/data \
     -v /caminho/para/tmp:/app/tmp \
     chatbot-ia
   ```
   - Monte `data/` com os `.docx` e `tmp/` para persistir embeddings/banco entre reinícios.
   - Em painéis como o EasyPanel, basta criar o app, informar as variáveis de ambiente e mapear os volumes para essas pastas.
3. Acesse `http://<host>:801` para interagir com o chatbot.

## 🔐 Fluxo de Login
- O formulário de autenticação é exibido antes de qualquer interação com o agente.
- As credenciais são validadas localmente usando os pares definidos em `APP_USERS`.
- O botão **Sair** (sidebar) encerra a sessão, limpa o histórico de mensagens e retorna para a tela de login.

## 🧠 Sobre o Agente
- Carrega automaticamente os documentos `.docx` (modo padrão) ao inicializar, salvo se `preload_knowledge=False` for passado para `build_agent`.
- Usa ChromaDB como vetor de conhecimento persistente.
- Mantém histórico e memórias para contextualizar respostas.
- Garante que todas as respostas sigam o roteiro jurídico definido em `openai_agent.py`.

## 🛠️ Manutenção e Atualizações
- Adicione novos usuários apenas editando `APP_USERS` no `.env`.
- Reexecute `python ingest_docx.py` sempre que incluir novos `.docx` ou alterar os existentes.
- Limpe a pasta `tmp/` caso deseje reprocessar toda a base do zero.
- Verifique periodicamente se há atualizações nas dependências necessárias.

## 🤝 Contribuindo
1. Crie um fork ou nova branch.
2. Faça suas alterações (incluindo testes manuais do fluxo).
3. Abra um pull request descrevendo o impacto das mudanças.

---

Se surgirem dúvidas ou precisar expandir funcionalidades (como autenticação mais robusta ou novos formatos de documentos), basta comentar nos issues do projeto! 🚀
