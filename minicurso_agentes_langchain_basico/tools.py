import os

from decouple import config
from exa_py import Exa
from langchain_community.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    GoogleSerperAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_core.tools import tool

# Carregar a API do Serper
os.environ["SERPER_API_KEY"] = config("SERPER_API_KEY")

# Instanciando a classe DuckDuckGoSearchResults
duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(region="br-pt", time="y")
duckduckgo = DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper)

# Instanciando a classe WikipediaQueryRun
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="pt", top_k_results=5))

# Instanciando a classe GoogleSerperAPIWrapper
google_serper = GoogleSerperAPIWrapper(location="Brazil", gl="br", hl="pt-br", search_type="search", k=2)

# Instanciando a classe Exa
exa = Exa(api_key=config("EXA_API_KEY"))


def pesquisa() -> str:
    pesquisa = input("Digite o que deseja pesquisar: ")
    return pesquisa


def main() -> str:
    pergunta = pesquisa()
    # Busca com DuckDuckGo
    resultado = duckduckgo.invoke(pergunta)
    print(f"\n ======> Resultado DuckDuckGo:\n {resultado}")

    # Busca com Wikipedia
    resultado = wikipedia.invoke(pergunta)
    print(f"\n ======> Resultado Wikipedia:\n {resultado}")

    # Busca com Google Serper
    resultado = google_serper.results(pergunta)
    # print(f"\n ======> Resultado Google Serper:\n {resultado['organic']}")
    for item in resultado["organic"]:
        print(f"\n{item['title']}")
        print(f"{item['snippet']}")
        print(f"{item['link']}")
        print("\n")

    # Busca com Exa
    resultado = exa.search_and_contents(
        query=pergunta,
        num_results=2,
        exclude_domains=["wikipedia.org"],
        text=False,
        highlights=True,
        start_published_date="2024-01-01",
        category="personal site",
    )
    print(f"\n ======> Resultado Exa:\n {resultado}")
