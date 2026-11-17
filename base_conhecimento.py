import json
from pathlib import Path
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()-/":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []   # lista de objetos Orientacao

    def carregar(self):
        if not self.caminho.exists():
            print("Aviso: base de conhecimento não encontrada.")
            return False

        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        except json.JSONDecodeError:   # JSON corrompido
            print("Aviso: base de conhecimento corrompida.")
            return False

        if type(dados) != list:
            print("Aviso: a base deve ser uma lista de orientações.")
            return False

        self.orientacoes = []
        for item in dados:
            try:
                orientacao = Orientacao(
                    item["id"], item["categoria"], item["titulo"],
                    item["palavras_chave"], item["resposta"],
                    item["documentos"], item["onde"],
                    item["fonte"], item["verificado_em"]
                )
                self.orientacoes.append(orientacao)
            except (KeyError, TypeError):
                print("Aviso: uma orientação com campos faltando foi ignorada.")
        return True

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)
        return lista

    def pontuar(self, orientacao, pergunta_norm):

        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            if normalizar(palavra_chave) in pergunta_norm:
                pontos += 3

        titulo_norm = normalizar(orientacao.titulo)
        ja_contadas = []   # para não contar a mesma palavra duas vezes
        for palavra in pergunta_norm.split():
            if len(palavra) >= 4 and palavra not in ja_contadas:
                ja_contadas.append(palavra)
                if " " + palavra + " " in titulo_norm:
                    pontos += 1

        return pontos

    def buscar(self, pergunta):

        pergunta_norm = normalizar(pergunta)
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(orientacao, pergunta_norm)
            if pontos > 0:
                resultados.append((pontos, orientacao))


        ordenados = []
        while len(resultados) > 0:
            maior = resultados[0]
            for item in resultados:
                if item[0] > maior[0]:
                    maior = item
            ordenados.append(maior)
            resultados.remove(maior)
        return ordenados