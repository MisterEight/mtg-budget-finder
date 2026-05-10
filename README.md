# Projeto: Magic the gathering Budget Alternative Finder
Esse projeto tem como o objetivo criar uma aplicação que é capaz de encontrar substituições baratas para cartas de Magic the Gathering (MTG).

# Motivação
É um problema comum para jogadores de MTG a necessidade de encontrar cartas com efeitos parecidos com preços menores levando em consideração que certas cartas podem custar dezenas de reais, junto com essa necessidade e a minha paixão pela área de ciência de dados esse projeto nasceu.

# Como funciona
O usuário irá digitar o nome da carta que quer encontrar opções baratas, o sistema busca no banco, filtra por similaridade (Usando vetores feitos por um modelo TF-IDF e similaridade de cosseno), retorna substitutas ordenadas por preço e similaridade.

# Tecnologias
Python: A base de código para conectar ao banco, NLP e scrapping.
MongoDB: Armazenar os dados das cartas e as informações do modelo.
API's: Scryfall.
Fonte de scrapping para preços em R$: LigaMagic.

# Como rodar

### Pré-requisitos
- Python 3.10+
- MongoDB rodando localmente (padrão: `mongodb://localhost:27017`)

### 1. Instalar dependências
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente (opcional)
Por padrão o projeto usa `mongodb://localhost:27017`, banco `mtg_budget_finder` e coleção `cards`. Para sobrescrever:
```bash
set MONGO_URI=mongodb://localhost:27017
set DB_NAME=mtg_budget_finder
set COLLECTION_NAME=cards
```

### 3. Baixar e ingerir os dados do Scryfall
```bash
python -m data.scryfall_ingestion
```
Faz o download do bulk data do Scryfall (~100MB), salva no MongoDB e cria os índices. Pode levar alguns minutos.

### 4. Treinar o modelo TF-IDF
```bash
python -m data.build_tfidf
```
Gera os arquivos do modelo em `models/`. Precisa ser refeito sempre que os dados forem atualizados.

### 5. Buscar alternativas
```bash
python search.py
```

### Rodar os testes
```bash
pytest tests/test_filters.py   # testes unitários (sem banco)
pytest tests/test_sanity.py    # testes de integração (requer MongoDB + modelo treinado)
```

# Próximos passos / roadmap

1 - ~~MVP: Busca e filtragem de cartas similares por TF-IDF com preços em USD.~~ ✓

2 - Integrar valores da LigaMagic.

3 - Usar embeddings como fator para similaridade.
