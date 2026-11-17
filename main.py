from pathlib import Path
from base_conhecimento import BaseConhecimento
from assistente import Assistente

CAMINHO_BASE = Path(__file__).resolve().parent / "data" / "base_conhecimento.json"


def exportar(assistente):
   # caso tente exportar sem ter feito nenhum atendimento, avisa que não tem nada pra exportar e pede pra fazer um atendimento
   # também avisa que os atendimentos serão exportados automaticamwnte no final da sessão.
    if len(assistente.sessao) == 0:
        print("Não há novos atendimentos para exportar. Faça uma pergunta ou use as categorias; ao sair, o CSV é exportado automaticamente.")
        return

    path_csv = assistente.exportar_csv()

    if path_csv is None:
        print("Não foi possível exportar os atendimentos")
    else:
        print(f"Os atendimentos foram exportados para {path_csv}")


def main():
    base = BaseConhecimento(CAMINHO_BASE)
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    print(f"\nBem-vindo(a) ao {assistente.nome}!")
    print("O objetivo desse assistente é fornecer orientações para universitários e estudantes de baixa renda.")
    print("Este assistente NÃO é um canal oficial.")
    print("Não digite CPF, telefone ou e-mail: perguntas com 8 ou mais números ou com @ são recusadas.")

    while True:
        print(f"\n{assistente.nome}")
        print("[1] Fazer uma pergunta")
        print("[2] Navegar por categorias")
        print("[3] Ver indicadores")
        print("[4] Exportar atendimentos para CSV")
        print("[0] Sair do programa")

        opt = input("Escolha uma opção: ").strip()
        if opt == "1":
            assistente.perguntar()
        elif opt == "2":
            assistente.navegar()
        elif opt == "3":
            assistente.indicadores()
        elif opt == "4":
            exportar(assistente)
        elif opt == "0":
            if len(assistente.sessao) == 0:
                # se não tiver nenhum atendimento, não exporta csv e a mensagem de saída é diferente
                print("Até mais!")
            else:
                assistente.pedir_nota()
                # exporta o csv da sessão automaticamente, já com a nota dada pelo usuário
                exportar(assistente)
                print("Obrigado por utilizar o assistente e pela avaliação, até mais! :)")
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()