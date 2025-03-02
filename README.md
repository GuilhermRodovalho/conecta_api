# API Conecta

## Estrutura do Projeto
- **app/**: Código-fonte (rotas, modelos, schemas, configuração do banco).
- **tests/**: Testes automatizados.
- **docs/**: Documentação adicional.
- **requirements.txt**: Lista de dependências.
- **Dockerfile** e **docker-compose.yml**: Configuração de containerização.

## Instalação
1. Clone o repositório:
   ```
   git clone <URL-do-repositório>
   ```
2. Acesse a pasta do projeto:
   ```
   cd conecta_api
   ```
3. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Dependências de Desenvolvimento
Instale ferramentas de qualidade de código, se necessário:
```
pip install ruff
```

## Como Rodar
- Execução local:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
- Utilizando Docker:
   ```
   docker-compose up --build
   ```

## Notas
- Certifique-se de que o banco de dados está configurado corretamente (variável DATABASE_URL no docker-compose).
