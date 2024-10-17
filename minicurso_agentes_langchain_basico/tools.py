import os

from decouple import config
from langchain_community.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    GoogleSerperAPIWrapper,
    WikipediaAPIWrapper,
)

# Carregar a API do Serper
os.environ["SERPER_API_KEY"] = config("SERPER_API_KEY")

# Instanciando a classe DuckDuckGoSearchResults
duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(region="br-pt", time="y")
duckduckgo = DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper)

# Instanciando a classe WikipediaQueryRun
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="pt"))

# Instanciando a classe GoogleSerperAPIWrapper
google_serper = GoogleSerperAPIWrapper(
    gl="br",
    hl="pt-br",
)


def pesquisa() -> str:
    pesquisa = input("Digite o que deseja pesquisar: ")
    return pesquisa


def main() -> str:
    # Busca com DuckDuckGo
    resultado = duckduckgo.invoke(pesquisa())
    print(f"Resultado DuckDuckGo: {resultado}")
