import os

from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI


class Agente:
    def __init__(self, modelo: str = "gemini-1.5-flash"):
        self._configurar_chave_api()
        self.modelo = self._instanciar(modelo)

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

    def _instanciar(self, modelo):
        """
        Inicializa o modelo Google Generative AI.
        """
        try:
            modelo = ChatGoogleGenerativeAI(model=modelo)
            return modelo
        except Exception as e:
            raise ValueError("Erro ao instanciar o modelo Google Generative AI: " + str(e))
