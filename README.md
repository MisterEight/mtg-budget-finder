# Projeto: Magic the gathering Budget Alternative Finder
Esse projeto tem como o objetivo criar uma aplicação que é capaz de encontrar substituições baratas para cartas de Magic the Gathering (MTG).

# Motivação
É um problema comum para jogadores de MTG a necessidade de encontrar cartas com efeitos parecidos com preços menores levando em consideração que certas cartas podem custar dezenas de reais, junto com essa necessidade e a minha paixão pela área de ciência de dados esse projeto nasceu.

# Como funciona
O usuário irá digitar o nome da carta que quer encontrar opções baratas, o sistema busca no banco, filtra por similaridade, retorna substitutas ordenadas por preço e similaridade.

# Tecnologias
Python: A base de código para conectar ao banco, NLP e scrapping.
MongoDB: Armazenar os dados das cartas e as informações do modelo.
API's: Scryfall.
Fonte de scrapping para preços em R$: LigaMagic.

# Como rodar
### TODO: Ao ter o MVP criar a seção de como rodar.

# Próximos passos / roadmap

1 - MVP: Busca e filtragem de cartas similares por palavras-chaves com preços em USD.
2 - Integrar valores da LigaMagic.
3 - Adicionar o texto da carta como fator para similaridade.
