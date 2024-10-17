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
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="pt", top_k_results=5))

# Instanciando a classe GoogleSerperAPIWrapper
google_serper = GoogleSerperAPIWrapper(location="Brazil", gl="br", hl="pt-br", search_type="search", k=2)


def pesquisa() -> str:
    pesquisa = input("Digite o que deseja pesquisar: ")
    return pesquisa


def main() -> str:
    pergunta = pesquisa()
    # Busca com DuckDuckGo
    resultado = duckduckgo.invoke(pergunta)
    print(f"\nResultado DuckDuckGo:\n {resultado}")

    # Busca com Wikipedia
    resultado = wikipedia.invoke(pergunta)
    print(f"\nResultado Wikipedia:\n {resultado}")

    # Busca com Google Serper
    resultado = google_serper.results(pergunta)
    print(f"\nResultado Google Serper:\n {resultado['organic']}")

    for item in resultado["organic"]:
        print(f"\n{item['title']}")
        print(f"{item['snippet']}")
        print(f"{item['link']}")
        print("\n")
