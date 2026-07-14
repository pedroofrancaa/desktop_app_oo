from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.servico import Servico
    from app.models.veiculo import Veiculo


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
    veiculos: list[Veiculo] = field(default_factory=list)

    def adicionar_veiculo(self, veiculo: Veiculo) -> None:
        self.veiculos.append(veiculo)

    def resumo(self) -> str:
        return f"{self.nome} | CPF: {self.cpf} | Tel: {self.telefone}"


@dataclass
class Funcionario(Pessoa):
    matricula: str
    cargo: str

    def resumo(self) -> str:
        return f"{self.matricula} - {self.nome} | {self.cargo}"

    def executar_servico(self, servico: Servico) -> str:
        return f"{self.nome} executou {servico.descricao()}"
