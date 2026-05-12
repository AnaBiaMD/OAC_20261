# Montador RISC-V32I

## Contribuidores

- Isabella Lemos Alvarenga
- Ana Beatriz Macedo Dourado
- Pedro Dourado Braga
- Thaís Aragão Bianchini
- Eron Marins dos Santos

## Descrição

Este projeto consiste na implementação de um montador (assembler) para a arquitetura RISC-V32I. O programa é responsável por traduzir instruções escritas em assembly para código de máquina em hexadecimal, gerando arquivos compatíveis com memória inicializada e ambientes de simulação.

O projeto foi desenvolvido com fins acadêmicos para aprofundar os conceitos de arquitetura de computadores, linguagem de montagem e codificação de instruções.

---

## Objetivos

- Implementar um assembler para a ISA RISC-V32I;
- Traduzir instruções assembly para código de máquina;
- Gerar arquivos de saída no formato `.mif`;
- Exercitar conceitos de arquitetura de computadores;
- Compreender o funcionamento interno de um montador.

---

## Funcionalidades

- Leitura de arquivos `.asm`;
- Parsing de instruções e operandos;
- Conversão para representação binária;
- Geração de instruções em hexadecimal;
- Geração automática do arquivo `data.mif`;
- Suporte aos formatos de instrução:
  - Tipo R
  - Tipo I
  - Tipo S
  - Tipo B
  - Tipo U
  - Tipo J

---

## Estrutura do Projeto

```text
.
├── _data.mif             (arquivo de memória inicializada para simulação)
├── _text.mif             (memória de instruções gerada pelo assembler)
├── assembler.py          (arquivo principal do montador)
├── CHECKLIST_INSTRUCOES  (lista de instruções implementadas/testadas no projeto)
├── entrada.asm           (código assembly de entrada a ser traduzido)
├── saida.txt             (saída gerada com as instruções em hexadecimal)
└── README.md             (documentação do projeto)
