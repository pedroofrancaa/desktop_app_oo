from dataclasses import dataclass


@dataclass
class Veiculo:
    placa: str
    modelo: str
    porte: str

    def resumo(self) -> str:
        return f"{self.modelo} | Placa: {self.placa} | Porte: {self.porte}"
