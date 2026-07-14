from abc import ABC, abstractmethod


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
