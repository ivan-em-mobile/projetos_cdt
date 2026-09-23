from pathlib import Path

from app.cli.menu import iniciar_menu
from app.database.schema import criar_tabelas
from app.services.usuario_service import criar_usuario_root


def obter_versao():
    caminho_versao = (
        Path(__file__).parent
        / "VERSION"
    )

    with open(
        caminho_versao,
        "r",
        encoding="utf-8",
    ) as arquivo:
        return arquivo.read().strip()


def main():
    versao = obter_versao()

    criar_tabelas()
    criar_usuario_root()

    print("=" * 40)
    print("SMARTFIT GYM MANAGER")
    print(f"Versão {versao}")
    print("=" * 40)

    iniciar_menu()


if __name__ == "__main__":
    main()