from app.models.ordem_servico import OrdemServico, StatusOrdem


class RelatorioFinanceiro:
    def gerar(self, ordens: list[OrdemServico]) -> str:
        finalizadas = [
            ordem for ordem in ordens if ordem.status == StatusOrdem.FINALIZADA
        ]
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
