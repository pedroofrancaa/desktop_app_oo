# Sistema de Lava Jato - Nivel 2

Projeto em Python para demonstrar modelagem orientada a objetos no Nivel 2 da macro tarefa.
O sistema funciona no terminal e possui um menu principal com acesso aos menus de clientes,
veiculos, funcionarios, servicos, ordens de servico e relatorios.

Os dados permanecem em memoria durante a execucao. Ao fechar o programa, eles sao apagados,
pois o banco de dados sera exigido somente no Nivel 3.

## Estrutura do projeto

```text
desktop_app_oo/
|-- main.py
|-- app/
|   |-- models/
|   |   |-- pessoa.py
|   |   |-- veiculo.py
|   |   |-- servico.py
|   |   `-- ordem_servico.py
|   |-- controllers/
|   |   `-- lava_jato_app.py
|   |-- services/
|   |   `-- relatorio_financeiro.py
|   `-- views/
|       `-- menu_terminal.py
|-- tests/
`-- docs/
```

- `models`: classes e regras do dominio do lava-jato.
- `controllers`: fluxo do programa e coordenacao entre modelos e menus.
- `services`: geracao do relatorio financeiro.
- `views`: painel visual, entradas e mensagens do terminal.
- `main.py`: ponto de entrada que inicia a aplicacao.

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

- Clientes: cadastrar e listar, incluindo seus veiculos.
- Veiculos: cadastrar para um cliente e listar com o proprietario.
- Funcionarios: cadastrar e listar.
- Servicos: consultar o catalogo e os precos polimorficos.
- Ordens: registrar uma lavagem com um ou mais servicos, listar e consultar.
- Pagamentos: finalizar imediatamente ou deixar a ordem aberta para receber depois.
- Relatorios: consultar ordens abertas, finalizadas, faturamento e ticket medio.

## Como testar

Os testes automatizados validam os precos dos servicos, o relatorio, a navegacao do menu e o
fluxo completo de uma ordem aberta ate a confirmacao do pagamento:

```bash
python -m unittest discover -s tests -v
```

## UML

A modelagem UML esta em:

```text
docs/uml_lava_jato.puml
```

## Roteiro do video

O roteiro sugerido para a apresentacao de ate 6 minutos esta em:

```text
docs/roteiro_video_nivel_2.txt
```
