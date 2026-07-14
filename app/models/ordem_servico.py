from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from app.models.pessoa import Cliente, Funcionario
from app.models.servico import Servico
from app.models.veiculo import Veiculo


class StatusOrdem(Enum):
    ABERTA = "Aberta"
    FINALIZADA = "Finalizada"


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
            linhas.append(
                f"Pagamento: {self.pagamento.forma} | "
                f"Confirmado: {self.pagamento.confirmado}"
            )
        return "\n".join(linhas)
