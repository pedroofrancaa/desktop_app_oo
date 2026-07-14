import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from app.controllers import LavaJatoApp
from app.models import (
    LavagemCompleta,
    LavagemSimples,
    Polimento,
    StatusOrdem,
)
from app.services import RelatorioFinanceiro


class TestModelos(unittest.TestCase):
    def test_polimorfismo_dos_precos(self) -> None:
        servicos = [LavagemSimples(), LavagemCompleta(), Polimento()]
        precos = [round(servico.calcular_preco(), 2) for servico in servicos]
        self.assertEqual(precos, [35.0, 85.0, 103.5])

    def test_relatorio_sem_ordens(self) -> None:
        relatorio = RelatorioFinanceiro().gerar([])
        self.assertIn("Ordens finalizadas: 0", relatorio)
        self.assertIn("Faturamento total: R$ 0.00", relatorio)


class TestFluxoNivel2(unittest.TestCase):
    def setUp(self) -> None:
        self.app = LavaJatoApp()

    def test_fluxo_completo_de_ordem_aberta_ate_pagamento(self) -> None:
        with patch("builtins.input", side_effect=["Ana", "11999990000", "12345678900"]):
            cliente = self.app.cadastrar_cliente()

        with patch("builtins.input", side_effect=["1", "ABC1D23", "Onix", "medio"]):
            veiculo = self.app.cadastrar_veiculo()

        self.assertIsNotNone(veiculo)
        self.assertIs(cliente.veiculos[0], veiculo)

        entradas_da_ordem = [
            "1",  # cliente
            "1",  # veiculo
            "2",  # lavagem completa
            "1",  # funcionario
            "n",  # nao adicionar outro servico
            "n",  # deixar a ordem aberta
        ]
        with patch("builtins.input", side_effect=entradas_da_ordem):
            ordem = self.app.registrar_lavagem()

        self.assertIsNotNone(ordem)
        self.assertEqual(ordem.status, StatusOrdem.ABERTA)
        self.assertEqual(ordem.total(), 85.0)

        with patch("builtins.input", side_effect=["1", "Pix"]):
            finalizada = self.app.finalizar_ordem()

        self.assertIs(finalizada, ordem)
        self.assertEqual(ordem.status, StatusOrdem.FINALIZADA)
        self.assertIsNotNone(ordem.pagamento)
        self.assertTrue(ordem.pagamento.confirmado)

    def test_menu_da_acesso_a_clientes_e_servicos(self) -> None:
        entradas = [
            "1",  # menu de clientes
            "2",  # listar clientes
            "",   # pausa
            "0",  # voltar
            "4",  # menu de servicos
            "1",  # listar catalogo
            "",   # pausa
            "0",  # voltar
            "0",  # sair
        ]
        saida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
            self.app.executar()

        texto = saida.getvalue()
        self.assertIn("MENU DE CLIENTES", texto)
        self.assertIn("CATALOGO DE SERVICOS", texto)
        self.assertIn("Lavagem simples", texto)
        self.assertIn("Sistema encerrado.", texto)


if __name__ == "__main__":
    unittest.main()
