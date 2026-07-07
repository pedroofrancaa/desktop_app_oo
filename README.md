# Sistema de Lava Jato - Nivel 1

Projeto em Python para demonstrar modelagem orientada a objetos no Nivel 1 da macro tarefa.
O sistema funciona no terminal e permite cadastrar cliente, cadastrar veiculo, registrar lavagem,
listar ordens e emitir relatorio financeiro.

## Como executar no CMD

Abra o terminal nesta pasta e rode:

```bash
python main.py
```

Tambem e possivel rodar pelo arquivo:

```bash
.\executar.cmd
```

Se o comando `python` nao estiver disponivel, tente:

```bash
py main.py
```

## O que o projeto demonstra

- Heranca: `Pessoa` gera `Cliente` e `Funcionario`; `Servico` gera `LavagemSimples`, `LavagemCompleta` e `Polimento`.
- Polimorfismo: `calcular_preco()` funciona de forma diferente em cada servico.
- Composicao: `OrdemServico` possui `ItemServico` e `Pagamento`.
- Associacao: `Cliente` possui `Veiculo`; `OrdemServico` associa cliente, veiculo e funcionarios.
- Dependencia: `RelatorioFinanceiro` depende de `OrdemServico` para gerar o faturamento.

## Funcionalidades implementadas

- Cadastrar cliente.
- Cadastrar veiculo vinculado ao cliente.
- Registrar lavagem com um ou mais servicos.
- Selecionar funcionario responsavel pelo servico.
- Finalizar ordem com pagamento.
- Listar ordens de servico.
- Gerar relatorio financeiro.

## UML

A imagem UML esta em:

```text
docs/uml_lava_jato.svg
```

Tambem existe uma versao PlantUML em:

```text
docs/uml_lava_jato.puml
```
