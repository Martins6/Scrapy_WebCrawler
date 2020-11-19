# Planos de Deploy

Para executar os Crawlers em produção a maneira mais natural de eu pensar sobre isso seria criar um REST API com Flask em Python e dockerizar (usar Docker containers) com todo esse ambiente de forma que quando alguém requisitasse os dados poderíamos passar através de JSON seja uma linha em especial ou o conjunto todo.

Haveria também a forma de criar um banco de dados como MySQL ou PostgreSQL e dockerizar novamente e a pessoa que quisesse os dados criarias as queries conforme quisesse.