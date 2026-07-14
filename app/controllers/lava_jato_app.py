from datetime import date

from app.models import (
    Cliente,
    Funcionario,
    LavagemCompleta,
    LavagemSimples,
    OrdemServico,
    Polimento,
    Servico,
    StatusOrdem,
    Veiculo,
)
from app.services import RelatorioFinanceiro
from app.views import MenuTerminal


class LavaJatoApp:
    """Controla os menus e coordena os modelos da aplicacao."""

    def __init__(self, view: MenuTerminal | None = None) -> None:
        self.view = view or MenuTerminal()
        self.clientes: list[Cliente] = []
        self.funcionarios: list[Funcionario] = [
            Funcionario("Mariana Souza", "(11) 98888-1111", "F001", "Lavador"),
            Funcionario("Carlos Lima", "(11) 97777-2222", "F002", "Polidor"),
        ]
        self.ordens: list[OrdemServico] = []
        self.proximo_codigo = 1
        self.tipos_servico: dict[str, type[Servico]] = {
            "1": LavagemSimples,
            "2": LavagemCompleta,
            "3": Polimento,
        }

    def executar(self) -> None:
        while True:
            self.view.mostrar_menu_principal()
            opcao = self.view.ler("Escolha uma opcao: ").strip()

            if opcao == "1":
                self.menu_clientes()
            elif opcao == "2":
                self.menu_veiculos()
            elif opcao == "3":
                self.menu_funcionarios()
            elif opcao == "4":
                self.menu_servicos()
            elif opcao == "5":
                self.menu_ordens()
            elif opcao == "6":
                self.menu_relatorios()
            elif opcao == "0":
                self.view.exibir("Sistema encerrado.")
                break
            else:
                self.view.exibir("Opcao invalida.")
                self.view.pausar()

    def menu_clientes(self) -> None:
        self.view.executar_submenu(
            "MENU DE CLIENTES",
            {
                "1": ("Cadastrar cliente", self.cadastrar_cliente),
                "2": ("Listar clientes", self.listar_clientes),
            },
        )

    def menu_veiculos(self) -> None:
        self.view.executar_submenu(
            "MENU DE VEICULOS",
            {
                "1": ("Cadastrar veiculo", self.cadastrar_veiculo),
                "2": ("Listar todos os veiculos", self.listar_veiculos),
            },
        )

    def menu_funcionarios(self) -> None:
        self.view.executar_submenu(
            "MENU DE FUNCIONARIOS",
            {
                "1": ("Cadastrar funcionario", self.cadastrar_funcionario),
                "2": ("Listar funcionarios", self.listar_funcionarios),
            },
        )

    def menu_servicos(self) -> None:
        self.view.executar_submenu(
            "MENU DE SERVICOS",
            {"1": ("Listar catalogo e precos", self.listar_servicos)},
        )

    def menu_ordens(self) -> None:
        self.view.executar_submenu(
            "MENU DE ORDENS DE SERVICO",
            {
                "1": ("Registrar nova lavagem", self.registrar_lavagem),
                "2": ("Listar todas as ordens", self.listar_ordens),
                "3": ("Consultar uma ordem", self.consultar_ordem),
                "4": ("Finalizar ordem aberta", self.finalizar_ordem),
            },
        )

    def menu_relatorios(self) -> None:
        self.view.executar_submenu(
            "MENU DE RELATORIOS",
            {"1": ("Relatorio financeiro", self.mostrar_relatorio)},
        )

    def cadastrar_cliente(self) -> Cliente:
        self.view.exibir("\nCADASTRO DE CLIENTE")
        nome = self.view.ler_texto("Nome: ")
        telefone = self.view.ler_texto("Telefone: ")
        cpf = self.view.ler_texto("CPF: ")

        cliente = Cliente(nome=nome, telefone=telefone, cpf=cpf)
        self.clientes.append(cliente)
        self.view.exibir("Cliente cadastrado com sucesso.")
        return cliente

    def cadastrar_veiculo(self) -> Veiculo | None:
        self.view.exibir("\nCADASTRO DE VEICULO")
        cliente = self.selecionar_cliente()
        if not cliente:
            return None

        placa = self.view.ler_texto("Placa: ").upper()
        modelo = self.view.ler_texto("Modelo: ")
        porte = self.view.ler_texto("Porte (pequeno/medio/grande): ").lower()

        veiculo = Veiculo(placa=placa, modelo=modelo, porte=porte)
        cliente.adicionar_veiculo(veiculo)
        self.view.exibir("Veiculo cadastrado com sucesso.")
        return veiculo

    def cadastrar_funcionario(self) -> Funcionario:
        self.view.exibir("\nCADASTRO DE FUNCIONARIO")
        nome = self.view.ler_texto("Nome: ")
        telefone = self.view.ler_texto("Telefone: ")
        matricula = self.view.ler_texto("Matricula: ").upper()
        cargo = self.view.ler_texto("Cargo: ")

        funcionario = Funcionario(
            nome=nome,
            telefone=telefone,
            matricula=matricula,
            cargo=cargo,
        )
        self.funcionarios.append(funcionario)
        self.view.exibir("Funcionario cadastrado com sucesso.")
        return funcionario

    def registrar_lavagem(self) -> OrdemServico | None:
        self.view.exibir("\nREGISTRO DE LAVAGEM")
        cliente = self.selecionar_cliente()
        if not cliente:
            return None

        veiculo = self.selecionar_veiculo(cliente)
        if not veiculo:
            return None

        ordem = OrdemServico(
            codigo=self.proximo_codigo,
            cliente=cliente,
            veiculo=veiculo,
            data=date.today(),
        )
        self.proximo_codigo += 1

        while True:
            servico = self.selecionar_servico()
            if not servico:
                if ordem.itens:
                    break
                self.view.exibir("A ordem precisa ter pelo menos um servico.")
                continue

            funcionario = self.selecionar_funcionario()
            if not funcionario:
                self.view.exibir("Servico cancelado por falta de funcionario.")
                continue

            ordem.adicionar_servico(servico, funcionario)
            self.view.exibir(funcionario.executar_servico(servico))

            continuar = self.view.ler(
                "Adicionar outro servico na mesma ordem? (s/n): "
            ).strip().lower()
            if continuar != "s":
                break

        finalizar = self.view.ler(
            "Finalizar e receber pagamento agora? (s/n): "
        ).strip().lower()
        if finalizar == "s":
            forma = self.view.ler_texto(
                "Forma de pagamento (Pix/Dinheiro/Cartao): "
            )
            ordem.finalizar(forma)

        self.ordens.append(ordem)
        self.view.exibir("\nLavagem registrada com sucesso.")
        self.view.exibir(ordem.resumo())
        return ordem

    def listar_ordens(self) -> None:
        self.view.exibir("\nORDENS DE SERVICO")
        if not self.ordens:
            self.view.exibir("Nenhuma ordem registrada.")
            return

        for ordem in self.ordens:
            self.view.exibir("-" * 52)
            self.view.exibir(ordem.resumo())

    def consultar_ordem(self) -> OrdemServico | None:
        self.view.exibir("\nCONSULTA DE ORDEM")
        if not self.ordens:
            self.view.exibir("Nenhuma ordem registrada.")
            return None

        for indice, ordem in enumerate(self.ordens, start=1):
            self.view.exibir(
                f"{indice} - Ordem #{ordem.codigo} | "
                f"{ordem.cliente.nome} | {ordem.status.value}"
            )

        indice = self.view.ler_indice("Numero da ordem: ", len(self.ordens))
        if not indice:
            return None

        ordem = self.ordens[indice - 1]
        self.view.exibir("-" * 52)
        self.view.exibir(ordem.resumo())
        return ordem

    def finalizar_ordem(self) -> OrdemServico | None:
        self.view.exibir("\nFINALIZACAO DE ORDEM")
        abertas = [
            ordem for ordem in self.ordens if ordem.status == StatusOrdem.ABERTA
        ]
        if not abertas:
            self.view.exibir("Nao ha ordens abertas para finalizar.")
            return None

        for indice, ordem in enumerate(abertas, start=1):
            self.view.exibir(
                f"{indice} - Ordem #{ordem.codigo} | {ordem.cliente.nome} | "
                f"Total: R$ {ordem.total():.2f}"
            )

        indice = self.view.ler_indice("Numero da ordem: ", len(abertas))
        if not indice:
            return None

        ordem = abertas[indice - 1]
        forma = self.view.ler_texto(
            "Forma de pagamento (Pix/Dinheiro/Cartao): "
        )
        ordem.finalizar(forma)
        self.view.exibir(f"Ordem #{ordem.codigo} finalizada com sucesso.")
        self.view.exibir(
            f"Pagamento de R$ {ordem.total():.2f} confirmado via {forma}."
        )
        return ordem

    def mostrar_relatorio(self) -> None:
        self.view.exibir()
        self.view.exibir(RelatorioFinanceiro().gerar(self.ordens))

    def listar_clientes(self) -> None:
        self.view.exibir("\nCLIENTES")
        if not self.clientes:
            self.view.exibir("Nenhum cliente cadastrado.")
            return

        for indice, cliente in enumerate(self.clientes, start=1):
            self.view.exibir(f"{indice} - {cliente.resumo()}")
            if cliente.veiculos:
                for veiculo in cliente.veiculos:
                    self.view.exibir(f"    Veiculo: {veiculo.resumo()}")
            else:
                self.view.exibir("    Sem veiculos cadastrados.")

    def listar_veiculos(self) -> None:
        self.view.exibir("\nVEICULOS")
        veiculos_encontrados = False
        for cliente in self.clientes:
            for veiculo in cliente.veiculos:
                veiculos_encontrados = True
                self.view.exibir(
                    f"{veiculo.resumo()} | Proprietario: {cliente.nome}"
                )

        if not veiculos_encontrados:
            self.view.exibir("Nenhum veiculo cadastrado.")

    def listar_funcionarios(self) -> None:
        self.view.exibir("\nFUNCIONARIOS")
        if not self.funcionarios:
            self.view.exibir("Nenhum funcionario cadastrado.")
            return

        for indice, funcionario in enumerate(self.funcionarios, start=1):
            self.view.exibir(
                f"{indice} - {funcionario.resumo()} | Tel: {funcionario.telefone}"
            )

    def listar_servicos(self) -> None:
        self.view.exibir("\nCATALOGO DE SERVICOS")
        for codigo, classe_servico in self.tipos_servico.items():
            servico = classe_servico()
            self.view.exibir(
                f"{codigo} - {servico.descricao()} | "
                f"Preco: R$ {servico.calcular_preco():.2f}"
            )

    def selecionar_cliente(self) -> Cliente | None:
        if not self.clientes:
            self.view.exibir(
                "Nenhum cliente cadastrado. Cadastre um cliente primeiro."
            )
            return None

        self.listar_clientes()
        indice = self.view.ler_indice("Numero do cliente: ", len(self.clientes))
        return self.clientes[indice - 1] if indice else None

    def selecionar_veiculo(self, cliente: Cliente) -> Veiculo | None:
        if not cliente.veiculos:
            self.view.exibir("Este cliente ainda nao possui veiculo cadastrado.")
            return None

        self.view.exibir("\nVEICULOS DO CLIENTE")
        for indice, veiculo in enumerate(cliente.veiculos, start=1):
            self.view.exibir(f"{indice} - {veiculo.resumo()}")

        indice = self.view.ler_indice(
            "Numero do veiculo: ", len(cliente.veiculos)
        )
        return cliente.veiculos[indice - 1] if indice else None

    def selecionar_servico(self) -> Servico | None:
        self.view.exibir("\nSERVICOS")
        self.view.exibir("1 - Lavagem simples - R$ 35.00")
        self.view.exibir("2 - Lavagem completa - R$ 85.00")
        self.view.exibir("3 - Polimento - R$ 103.50")
        self.view.exibir("0 - Parar de adicionar servicos")

        opcao = self.view.ler("Servico: ").strip()
        if opcao == "0":
            return None

        classe_servico = self.tipos_servico.get(opcao)
        if not classe_servico:
            self.view.exibir("Servico invalido.")
            return self.selecionar_servico()

        return classe_servico()

    def selecionar_funcionario(self) -> Funcionario | None:
        self.view.exibir("\nFUNCIONARIOS")
        for indice, funcionario in enumerate(self.funcionarios, start=1):
            self.view.exibir(f"{indice} - {funcionario.resumo()}")

        indice = self.view.ler_indice(
            "Numero do funcionario: ", len(self.funcionarios)
        )
        return self.funcionarios[indice - 1] if indice else None
