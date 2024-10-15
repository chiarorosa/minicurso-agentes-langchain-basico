"""
Módulo para interagir com o modelo Google Generative AI usando LangChain.

Este módulo define a classe Agente que configura a chave da API, 
solicita perguntas ao usuário e obtém respostas do modelo de IA.
"""

import os

from decouple import config
from langchain_google_genai import GoogleGenerativeAI


class Agente:
    """
    Classe que representa um agente para interagir com o modelo Google Generative AI.

    A classe configura a chave da API, inicializa o modelo e fornece métodos para solicitar perguntas ao usuário e obter respostas do modelo.
    """

    def __init__(self, modelo: str = "gemini-1.5-flash"):
        """
        Inicializa uma instância da classe Agente.

        Parâmetros:
            modelo (str): O nome do modelo do Google Generative AI a ser utilizado. O padrão é "gemini-1.5-flash".
        """
        self._configurar_chave_api()
        self.model = GoogleGenerativeAI(model=modelo)

    def _configurar_chave_api(self):
        """
        Configura a chave da API do Google Generative AI como uma variável de ambiente.

        Lança:
            ValueError: Se a chave da API não estiver configurada no arquivo .env.
        """
        try:
            os.environ["GOOGLE_API_KEY"] = config("API_KEY")
        except:
            raise ValueError("Chave da API não configurada. Configure a chave da API no arquivo .env.")

    def pergunta(self) -> str:
        """
        Solicita uma pergunta ao usuário.

        Retorna:
            str: A pergunta fornecida pelo usuário.
        """
        return input("Faça uma pergunta: ")

    def resposta(self, pergunta: str) -> str:
        """
        Envia a pergunta para o modelo Google Generative AI e retorna a resposta gerada pelo modelo.

        Parâmetros:
            pergunta (str): A pergunta a ser enviada para o modelo.

        Retorna:
            str: A resposta gerada pelo modelo.
        """
        return self.model.invoke(pergunta)


def main():
    """
    Função principal que executa o fluxo do programa.

    Instancia o agente, solicita uma pergunta ao usuário e imprime a resposta gerada pelo modelo.
    """
    agente = Agente()
    pergunta = agente.pergunta()
    print(agente.resposta(pergunta))


if __name__ == "__main__":
    main()
