from collections.abc import Callable


class MenuTerminal:
    """Cuida da exibicao e da leitura de dados no terminal."""

    LARGURA = 50

    def mostrar_menu_principal(self) -> None:
        self.imprimir_caixa(
            "SISTEMA DE LAVA JATO",
            [
                "  [1] Clientes          [4] Servicos",
                "  [2] Veiculos          [5] Ordens de servico",
                "  [3] Funcionarios      [6] Relatorios",
                "",
                "  [0] Encerrar sistema",
            ],
            subtitulo="NIVEL 2",
        )

    def executar_submenu(
        self,
        titulo: str,
        opcoes: dict[str, tuple[str, Callable[[], object]]],
    ) -> None:
        while True:
            linhas = [
                f"  [{codigo}] {descricao}"
                for codigo, (descricao, _) in opcoes.items()
            ]
            linhas.extend(["", "  [0] Voltar ao menu principal"])
            self.imprimir_caixa(titulo, linhas)

            opcao = self.ler("Escolha uma opcao: ").strip()
            if opcao == "0":
                return

            item = opcoes.get(opcao)
            if not item:
                self.exibir("Opcao invalida.")
                self.pausar()
                continue

            item[1]()
            self.pausar()

    def imprimir_caixa(
        self,
        titulo: str,
        linhas: list[str],
        subtitulo: str | None = None,
    ) -> None:
        self.exibir("\n╔" + "═" * self.LARGURA + "╗")
        self.exibir(f"║{titulo:^{self.LARGURA}}║")
        if subtitulo:
            self.exibir(f"║{subtitulo:^{self.LARGURA}}║")
        self.exibir("╠" + "═" * self.LARGURA + "╣")
        for linha in linhas:
            self.exibir(f"║{linha:<{self.LARGURA}}║")
        self.exibir("╚" + "═" * self.LARGURA + "╝")

    @staticmethod
    def exibir(mensagem: object = "") -> None:
        print(mensagem)

    @staticmethod
    def ler(mensagem: str) -> str:
        return input(mensagem)

    def ler_texto(self, mensagem: str) -> str:
        while True:
            valor = self.ler(mensagem).strip()
            if valor:
                return valor
            self.exibir("Campo obrigatorio.")

    def ler_indice(self, mensagem: str, limite: int) -> int | None:
        while True:
            valor = self.ler(mensagem).strip()
            if not valor.isdigit():
                self.exibir("Digite um numero valido.")
                continue

            indice = int(valor)
            if 1 <= indice <= limite:
                return indice

            self.exibir("Opcao fora da lista.")

    def pausar(self) -> None:
        self.ler("\nPressione Enter para continuar...")
