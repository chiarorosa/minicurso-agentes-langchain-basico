# Recomendado levar para a Classe de Agente após a construção deste script
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from . import pacote_agentes as agentes

"""
=>toolkits inclusos:
InfoSQLDatabaseTool,
ListSQLDatabaseTool,
QuerySQLCheckerTool,
QuerySQLDataBaseTool,
"""


def main():
    # Instanciar o modelo de agente
    llm = agentes.Agente()

    # Conexão com Database relacional
    DATABASE_PATH = "books.db"
    DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    db = SQLDatabase.from_uri(DATABASE_URI)

    # Criar um toolkit para manipuar a Database
    toolkit = SQLDatabaseToolkit(db=db, llm=llm.modelo)

    # Langchain Hub [https://smith.langchain.com/hub]
    system_message = hub.pull("mikechan/gemini")
    # system_message = hub.pull("hwchase17/react")
    # print(system_message)

    # Criar um agente executor (reação)
    agente = create_react_agent(llm=llm.modelo, tools=toolkit.get_tools(), prompt=system_message)

    # Executar o agente
    executor = AgentExecutor(
        agent=agente,
        tools=toolkit.get_tools(),
        prompt=system_message,
        max_iterations=20,
        handle_parsing_errors=True,
        verbose=True,
    )

    prompt = """
    1. Traduza a seguinte pergunta para o Inglês.
    2. Utilize as ferramentas adequadas para responder a pergunta.
    3. Forneça a resposta final em Português do Brasil.

    Pergunta: {query}
    """

    pergunta = input("\n\nOlá, sou um consultor virtual de sua loja de livros. Como posso ajudar você hoje? ")

    try:
        prompt_template = PromptTemplate.from_template(prompt)
        resultado = executor.invoke(
            {
                "chat_history": "",
                "input": prompt_template.format(query=pergunta),
            }
        )
    except Exception as e:
        print(f"Ocorreu um erro ao invocar o agente: {e}")

    print(resultado.get("output"))


if __name__ == "__main__":
    main()
