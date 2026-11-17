import csv, json, time
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORICO_PATH = DATA_DIR / "historico.json"
CSV_PATH = DATA_DIR / "atendimentos.csv"


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base                       # objeto BaseConhecimento
        self.historico = self.ler_historico()  # lista de dicts
        self.sessao = []                       # atendimentos desta execução

    # historico
    def ler_historico(self):
        if not HISTORICO_PATH.exists():
            return []
        try:
            dados = json.loads(HISTORICO_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:   # arquivo corrompido não trava o programa
            return []
        if type(dados) == list:
            return dados
        return []

    def salvar_historico(self):
        try:
            HISTORICO_PATH.write_text(
                json.dumps(self.historico, ensure_ascii=False, indent=2),
                encoding="utf-8")
        except PermissionError:
            print("Aviso: não foi possível salvar o histórico.")

    # validações
    def tem_dado_pessoal(self, texto):
        # consideramos dados pessoais quando a pergunta tem 8 ou mais dígitos e/ou inclui um @
        digitos = 0
        for letra in texto:
            if letra.isdigit():
                digitos += 1
        return digitos >= 8 or "@" in texto

    def perguntar_sim_nao(self, texto):
        while True:
            resp = input(texto).strip().lower()
            if resp == "s":
                return True
            if resp == "n":
                return False
            print("Resposta inválida. Digite s ou n.")

    # perguntas
    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""
        id_orientacao = None
        encontrou = False
        ajudou = False

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                break
            if not pergunta:
                print("Você não digitou nada. Escreva sua dúvida ou 0 para voltar.")
                continue
            if self.tem_dado_pessoal(pergunta):
                # se a pergunta tem dados pessoais ela não é registrada
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima_pergunta = pergunta
            resultados = self.base.buscar(pergunta)

            if len(resultados) == 0 or resultados[0][0] < 3:
                encontrou = False
                ajudou = False
                id_orientacao = None
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras (ex.: prouni, fies, cadunico, bilhete unico)")
                print("ou use a navegação por categorias no menu:")
                for categoria in self.base.categorias():
                    print(f"  - {categoria}")
                continue

            pontos, melhor = resultados[0]
            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MÉDIA"

            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)\n")
            melhor.exibir()

            alternativas = resultados[1:3]   # até duas alternativas
            if len(alternativas) > 0:
                print("\nOutras orientações que podem ajudar:")
                for pts, orientacao in alternativas:
                    print(f"  - {orientacao.titulo} [{orientacao.categoria}] ({pts} pontos)")

            encontrou = True
            id_orientacao = melhor.id
            print()
            ajudou = self.perguntar_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
            if ajudou:
                break
            print("Desculpa! Tente reescrever a dúvida com outras palavras.")

        if tentativas > 0:
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", ultima_pergunta, id_orientacao,
                           encontrou, ajudou, tentativas, tempo)

    # navegação por categorias

    def navegar(self):
        categorias = self.base.categorias()
        if len(categorias) == 0:
            print("A base de conhecimento está vazia.")
            return

        while True:
            print("\n----- Categorias -----")
            for i, categoria in enumerate(categorias):
                print(f"[{i + 1}] {categoria}")
            print("[0] Voltar")

            opcao = input("Escolha uma categoria: ").strip()
            if opcao == "0":
                return
            try:
                numero = int(opcao)
            except ValueError:
                print("Opção inválida. Digite um número da lista.")
                continue
            if numero < 1 or numero > len(categorias):
                print("Opção inválida. Digite um número da lista.")
                continue

            self.navegar_orientacoes(categorias[numero - 1])

    def navegar_orientacoes(self, categoria):
        lista = self.base.por_categoria(categoria)

        while True:
            print(f"\n---- {categoria} ----")
            for i, orientacao in enumerate(lista):
                print(f"[{i + 1}] {orientacao.titulo}")
            print("[0] Voltar")

            opcao = input("Escolha uma orientação: ").strip()
            if opcao == "0":
                return
            try:
                numero = int(opcao)
            except ValueError:
                print("Opção inválida. Digite um número da lista.")
                continue
            if numero < 1 or numero > len(lista):
                print("Opção inválida. Digite um número da lista.")
                continue

            inicio = time.time()
            orientacao = lista[numero - 1]
            print()
            orientacao.exibir()
            print()
            ajudou = self.perguntar_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("categoria", orientacao.titulo, orientacao.id,
                           True, ajudou, 1, tempo)

    # histórico
    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo):
        atendimento = {
            "data": date.today().isoformat(),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": tempo
        }
        self.historico.append(atendimento)
        self.sessao.append(atendimento)
        self.salvar_historico()

    def pedir_nota(self):
        # pede uma nota de 1 a 5 no final do atendimento, apenas se houve atendimento
        if len(self.sessao) == 0:
            return
        while True:
            resp = input("\nDe 1 a 5, qual a facilidade de usar o assistente? ").strip()
            try:
                nota = int(resp)
            except ValueError:
                print("Nota inválida. Digite um número de 1 a 5.")
                continue
            if nota >= 1 and nota <= 5:
                break
            print("Nota inválida. Digite um número de 1 a 5.")
        for atendimento in self.sessao:
            atendimento["nota_facilidade"] = nota
        self.salvar_historico()

    # indicadores
    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("Ainda não há atendimentos registrados. Tente novamente após o atendimento.")
            return

        encontrados = 0
        ajudaram = 0
        soma_tempo = 0
        soma_tentativas = 0
        soma_notas = 0
        qtd_notas = 0
        sem_solucao = []

        for a in self.historico:
            if a["encontrou"]:
                encontrados += 1
                soma_tempo += a["tempo"]
            if a["ajudou"]:
                ajudaram += 1
            soma_tentativas += a["tentativas"]

            if "nota_facilidade" in a:
                soma_notas += a["nota_facilidade"]
                qtd_notas += 1

            if a["origem"] == "pergunta" and not a["ajudou"]:
                if a["pergunta"] not in sem_solucao:
                    sem_solucao.append(a["pergunta"])

        pct_encontrada = round(encontrados / total * 100, 1)
        pct_ajudou = round(ajudaram / total * 100, 1)
        tentativas_media = round(soma_tentativas / total, 1)
        if encontrados > 0:
            tempo_medio = round(soma_tempo / encontrados, 1)
        else:
            tempo_medio = 0

        print("\n----- Indicadores ----")
        print(f"Atendimentos registrados: {total}")
        print(f"Resposta encontrada: {pct_encontrada}%")
        print(f"Taxa de acerto (ajudou): {pct_ajudou}%")
        print(f"Tempo médio para encontrar: {tempo_medio} s")
        print(f"Tentativas por atendimento: {tentativas_media}")
        if qtd_notas > 0:
            print(f"Facilidade de uso (1 a 5): {round(soma_notas / qtd_notas, 1)}")
        else:
            print("Facilidade de uso (1 a 5): ainda sem notas")
        print("Dúvidas sem solução:")
        if len(sem_solucao) == 0:
            print("  (nenhuma)")
        for duvida in sem_solucao:
            print(f"  - {duvida}")

    # export do csv
    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo", "nota_facilidade"]

        try:
            with CSV_PATH.open("w", newline="", encoding="utf-8") as file_csv:
                writer = csv.DictWriter(file_csv, campos)
                writer.writeheader()
                for linha in self.historico:
                    writer.writerow(linha)
            return CSV_PATH
        except PermissionError:
            return None