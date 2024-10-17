from langchain_core.messages import HumanMessage, SystemMessage
from langchain_experimental.utilities import PythonREPL

from . import pacote_agentes as agentes


def main() -> None:
    """
    Executa o fluxo principal do assistente de programação.

    Este método inicializa um agente, coleta uma pergunta do usuário,
    configura as mensagens para o modelo de IA e invoca o modelo
    para obter uma resposta.

    Retorna:
        str: O conteúdo da resposta gerada pelo modelo de IA.
    """
    agente = agentes.Agente()
    repl = PythonREPL()

    pergunta = input("Seja bem-vindo! quantos crédito quer adicionar? ")

    mensagens = [
        SystemMessage(
            content=(
                "Você é um assistente que extrai a quantidade de créditos de uma frase. "
                "O usuário pode enviar a quantidade de créditos que deseja adicionar em qualquer formato de frase. "
                "Sua tarefa é identificar e retornar apenas o número de créditos mencionado. "
                "Se não houver número na frase, retorne '0'."
            )
        ),
        HumanMessage(content=pergunta),
    ]

    chat = agente.modelo.invoke(mensagens)
    resposta = chat.content.strip()

    print(f"O que a LLM interpretou? {resposta}\n")
    print(
        repl.run(
            f"""
saldo = 20
creditos = {resposta}
saldo += int(creditos)
print(f'foram adicionados {{creditos}} créditos, seu saldo atual é de {{saldo}}')
"""
        )
    )


if __name__ == "__main__":
    main()
