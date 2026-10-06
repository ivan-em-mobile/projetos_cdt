# Requisitos do Sistema

## Projeto

SmartFit Gym Manager

## Objetivo Geral

Desenvolver uma aplicação em Python capaz de automatizar processos de gerenciamento de academia, utilizando a Smart Fit como referência para o domínio da aplicação.

## Módulos

O sistema será composto pelos seguintes módulos:

- gerenciamento de alunos;
- gerenciamento de planos e assinaturas;
- gerenciamento de pagamentos;
- controle de acesso e frequência;
- gerenciamento de fichas de treino;
- geração de relatórios;
- exportação de dados para JSON.

## Entidades Principais

- Aluno
- Plano
- Assinatura
- Pagamento
- Acesso
- Treino
- Exercício

## Regras Iniciais

1. Cada aluno deve possuir um identificador único.
2. Um aluno pode possuir uma assinatura associada a um plano.
3. O sistema deve controlar o status da assinatura.
4. Os pagamentos devem estar associados à assinatura.
5. O acesso do aluno deve ser registrado.
6. O sistema deve verificar as condições de acesso antes de registrar a entrada.
7. Cada aluno poderá possuir fichas de treino.
8. Uma ficha poderá conter vários exercícios.
9. Os dados deverão ser armazenados em SQLite.
10. O banco deverá poder ser exportado para JSON.