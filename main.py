from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class StatusOrdem(Enum):
    ABERTA = "Aberta"
    FINALIZADA = "Finalizada"


@dataclass
class Pessoa(ABC):
    nome: str
    telefone: str

    @abstractmethod
    def resumo(self) -> str:
        pass


@dataclass
class Cliente(Pessoa):
    cpf: str
    veiculos: list["Veiculo"] = field(default_factory=list)

    def adicionar_veiculo(self, veiculo: "Veiculo") -> None:
        self.veiculos.append(veiculo)

    def resumo(self) -> str:
        return f"{self.nome} | CPF: {self.cpf} | Tel: {self.telefone}"


@dataclass
class Funcionario(Pessoa):
    matricula: str
    cargo: str

    def resumo(self) -> str:
        return f"{self.matricula} - {self.nome} | {self.cargo}"

    def executar_servico(self, servico: "Servico") -> str:
        # Polimorfismo: qualquer subclasse de Servico pode ser executada aqui.
        return f"{self.nome} executou {servico.descricao()}"


@dataclass
class Veiculo:
    placa: str
    modelo: str
    porte: str

    def resumo(self) -> str:
        return f"{self.modelo} | Placa: {self.placa} | Porte: {self.porte}"


class Servico(ABC):
    def __init__(self, nome: str, preco_base: float) -> None:
        self.nome = nome
        self.preco_base = preco_base

    @abstractmethod
    def calcular_preco(self) -> float:
        pass

    def descricao(self) -> str:
        return self.nome


class LavagemSimples(Servico):
    def __init__(self) -> None:
        super().__init__("Lavagem simples", 35.0)

    def calcular_preco(self) -> float:
        return self.preco_base


class LavagemCompleta(Servico):
    def __init__(self) -> None:
        super().__init__("Lavagem completa", 65.0)

    def calcular_preco(self) -> float:
        return self.preco_base + 20.0


class Polimento(Servico):
    def __init__(self) -> None:
        super().__init__("Polimento", 90.0)

    def calcular_preco(self) -> float:
        return self.preco_base * 1.15


@dataclass
class ItemServico:
    servico: Servico
    funcionario: Funcionario

    def subtotal(self) -> float:
        return self.servico.calcular_preco()

    def resumo(self) -> str:
        return f"{self.servico.descricao()} | {self.funcionario.nome} | R$ {self.subtotal():.2f}"


@dataclass
class Pagamento:
    forma: str
    valor: float
    confirmado: bool = False

    def confirmar(self) -> None:
        self.confirmado = True


@dataclass
class OrdemServico:
    codigo: int
    cliente: Cliente
    veiculo: Veiculo
    data: date
    itens: list[ItemServico] = field(default_factory=list)
    status: StatusOrdem = StatusOrdem.ABERTA
    pagamento: Pagamento | None = None

    def adicionar_servico(self, servico: Servico, funcionario: Funcionario) -> None:
        self.itens.append(ItemServico(servico=servico, funcionario=funcionario))

    def total(self) -> float:
        return sum(item.subtotal() for item in self.itens)

    def finalizar(self, forma_pagamento: str) -> None:
        if not self.itens:
            raise ValueError("Nao e possivel finalizar uma ordem sem servicos.")
        self.pagamento = Pagamento(forma=forma_pagamento, valor=self.total())
        self.pagamento.confirmar()
        self.status = StatusOrdem.FINALIZADA

    def resumo(self) -> str:
        linhas = [
            f"Ordem #{self.codigo} | {self.data.strftime('%d/%m/%Y')} | {self.status.value}",
            f"Cliente: {self.cliente.resumo()}",
            f"Veiculo: {self.veiculo.resumo()}",
            "Servicos:",
        ]
        linhas.extend(f"  - {item.resumo()}" for item in self.itens)
        linhas.append(f"Total: R$ {self.total():.2f}")
        if self.pagamento:
            linhas.append(f"Pagamento: {self.pagamento.forma} | Confirmado: {self.pagamento.confirmado}")
        return "\n".join(linhas)


class RelatorioFinanceiro:
    def gerar(self, ordens: list[OrdemServico]) -> str:
        finalizadas = [ordem for ordem in ordens if ordem.status == StatusOrdem.FINALIZADA]
        abertas = [ordem for ordem in ordens if ordem.status == StatusOrdem.ABERTA]
        total = sum(ordem.total() for ordem in finalizadas)
        ticket_medio = total / len(finalizadas) if finalizadas else 0.0

        return (
            "RELATORIO FINANCEIRO\n"
            f"Ordens finalizadas: {len(finalizadas)}\n"
            f"Ordens abertas: {len(abertas)}\n"
            f"Faturamento total: R$ {total:.2f}\n"
            f"Ticket medio: R$ {ticket_medio:.2f}"
        )


class LavaJatoApp:
    def __init__(self) -> None:
        self.clientes: list[Cliente] = []
        self.funcionarios: list[Funcionario] = [
            Funcionario("Mariana Souza", "(11) 98888-1111", "F001", "Lavador"),
            Funcionario("Carlos Lima", "(11) 97777-2222", "F002", "Polidor"),
        ]
        self.ordens: list[OrdemServico] = []
        self.proximo_codigo = 1
        self.tipos_servico = {
            "1": LavagemSimples,
            "2": LavagemCompleta,
            "3": Polimento,
        }

    def executar(self) -> None:
        while True:
            self.mostrar_menu()
            opcao = input("Escolha uma opcao: ").strip()

            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.cadastrar_veiculo()
            elif opcao == "3":
                self.registrar_lavagem()
            elif opcao == "4":
                self.listar_ordens()
            elif opcao == "5":
                self.mostrar_relatorio()
            elif opcao == "6":
                self.listar_clientes()
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opcao invalida.")

            self.pausar()

    def mostrar_menu(self) -> None:
        print("\n" + "=" * 52)
        print("SISTEMA DE LAVA JATO - NIVEL 1")
        print("=" * 52)
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar veiculo para cliente")
        print("3 - Registrar lavagem")
        print("4 - Listar ordens de servico")
        print("5 - Relatorio financeiro")
        print("6 - Listar clientes")
        print("0 - Sair")

    def cadastrar_cliente(self) -> Cliente:
        print("\nCADASTRO DE CLIENTE")
        nome = self.ler_texto("Nome: ")
        telefone = self.ler_texto("Telefone: ")
        cpf = self.ler_texto("CPF: ")

        cliente = Cliente(nome=nome, telefone=telefone, cpf=cpf)
        self.clientes.append(cliente)
        print("Cliente cadastrado com sucesso.")
        return cliente

    def cadastrar_veiculo(self) -> Veiculo | None:
        print("\nCADASTRO DE VEICULO")
        cliente = self.selecionar_cliente()
        if not cliente:
            return None

        placa = self.ler_texto("Placa: ").upper()
        modelo = self.ler_texto("Modelo: ")
        porte = self.ler_texto("Porte (pequeno/medio/grande): ").lower()

        veiculo = Veiculo(placa=placa, modelo=modelo, porte=porte)
        cliente.adicionar_veiculo(veiculo)
        print("Veiculo cadastrado com sucesso.")
        return veiculo

    def registrar_lavagem(self) -> OrdemServico | None:
        print("\nREGISTRO DE LAVAGEM")
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
                print("A ordem precisa ter pelo menos um servico.")
                continue

            funcionario = self.selecionar_funcionario()
            if not funcionario:
                print("Servico cancelado por falta de funcionario.")
                continue

            ordem.adicionar_servico(servico, funcionario)
            print(funcionario.executar_servico(servico))

            continuar = input("Adicionar outro servico na mesma ordem? (s/n): ").strip().lower()
            if continuar != "s":
                break

        finalizar = input("Finalizar e receber pagamento agora? (s/n): ").strip().lower()
        if finalizar == "s":
            forma = self.ler_texto("Forma de pagamento (Pix/Dinheiro/Cartao): ")
            ordem.finalizar(forma)

        self.ordens.append(ordem)
        print("\nLavagem registrada com sucesso.")
        print(ordem.resumo())
        return ordem

    def listar_ordens(self) -> None:
        print("\nORDENS DE SERVICO")
        if not self.ordens:
            print("Nenhuma ordem registrada.")
            return

        for ordem in self.ordens:
            print("-" * 52)
            print(ordem.resumo())

    def mostrar_relatorio(self) -> None:
        print()
        print(RelatorioFinanceiro().gerar(self.ordens))

    def listar_clientes(self) -> None:
        print("\nCLIENTES")
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return

        for indice, cliente in enumerate(self.clientes, start=1):
            print(f"{indice} - {cliente.resumo()}")
            if cliente.veiculos:
                for veiculo in cliente.veiculos:
                    print(f"    Veiculo: {veiculo.resumo()}")
            else:
                print("    Sem veiculos cadastrados.")

    def testar_funcionalidades(self, ordem: OrdemServico) -> None:
        assert ordem.cliente.veiculos[0] is ordem.veiculo
        assert len(ordem.itens) >= 1
        assert ordem.status == StatusOrdem.FINALIZADA
        assert ordem.pagamento is not None
        assert ordem.pagamento.confirmado is True
        assert round(ordem.total(), 2) > 0

        servicos: list[Servico] = [LavagemSimples(), LavagemCompleta(), Polimento()]
        precos = [round(servico.calcular_preco(), 2) for servico in servicos]
        assert precos == [35.0, 85.0, 103.5]

    def selecionar_cliente(self) -> Cliente | None:
        if not self.clientes:
            print("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
            return None

        self.listar_clientes()
        indice = self.ler_indice("Numero do cliente: ", len(self.clientes))
        return self.clientes[indice - 1] if indice else None

    def selecionar_veiculo(self, cliente: Cliente) -> Veiculo | None:
        if not cliente.veiculos:
            print("Este cliente ainda nao possui veiculo cadastrado.")
            return None

        print("\nVEICULOS DO CLIENTE")
        for indice, veiculo in enumerate(cliente.veiculos, start=1):
            print(f"{indice} - {veiculo.resumo()}")

        indice = self.ler_indice("Numero do veiculo: ", len(cliente.veiculos))
        return cliente.veiculos[indice - 1] if indice else None

    def selecionar_servico(self) -> Servico | None:
        print("\nSERVICOS")
        print("1 - Lavagem simples - R$ 35.00")
        print("2 - Lavagem completa - R$ 85.00")
        print("3 - Polimento - R$ 103.50")
        print("0 - Parar de adicionar servicos")

        opcao = input("Servico: ").strip()
        if opcao == "0":
            return None

        classe_servico = self.tipos_servico.get(opcao)
        if not classe_servico:
            print("Servico invalido.")
            return self.selecionar_servico()

        return classe_servico()

    def selecionar_funcionario(self) -> Funcionario | None:
        print("\nFUNCIONARIOS")
        for indice, funcionario in enumerate(self.funcionarios, start=1):
            print(f"{indice} - {funcionario.resumo()}")

        indice = self.ler_indice("Numero do funcionario: ", len(self.funcionarios))
        return self.funcionarios[indice - 1] if indice else None

    @staticmethod
    def ler_texto(mensagem: str) -> str:
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("Campo obrigatorio.")

    @staticmethod
    def ler_indice(mensagem: str, limite: int) -> int | None:
        while True:
            valor = input(mensagem).strip()
            if not valor.isdigit():
                print("Digite um numero valido.")
                continue

            indice = int(valor)
            if 1 <= indice <= limite:
                return indice

            print("Opcao fora da lista.")

    @staticmethod
    def pausar() -> None:
        input("\nPressione Enter para continuar...")


def main() -> None:
    LavaJatoApp().executar()


if __name__ == "__main__":
    main()
