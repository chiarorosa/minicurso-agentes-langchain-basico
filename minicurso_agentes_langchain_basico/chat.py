from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from . import pacote_agentes as agentes


def main():
    """
    Executa o fluxo principal do assistente de programação.

    Este método inicializa um agente, coleta uma pergunta do usuário,
    configura as mensagens para o modelo de IA e invoca o modelo
    para obter uma resposta.

    Retorna:
        str: O conteúdo da resposta gerada pelo modelo de IA.
    """
    agente = agentes.Agente()

    pergunta = input("Olá aluno, tire sua dúvida comigo: ")

    mensagens = [
        SystemMessage(
            content="Você é um assistente que ajuda iniciantes em programação. Dê respostas claras e amigáveis, adaptando-se ao nível do aluno. Use exemplos simples e evite termos técnicos, a menos que os explique de forma acessível. Se a pergunta for ampla, ajude a focar no ponto certo. Estimule o raciocínio lógico e incentive a prática. Seu foco é em Python, JavaScript e lógica de programação, mas também em conceitos básicos como estruturas de dados e algoritmos"
        ),
        HumanMessage(content="Eu sou um programador iniciante"),
        AIMessage(content="Como posso te ajudar hoje?"),
        HumanMessage(content=pergunta),
    ]

    chat = agente.modelo.invoke(mensagens)
    return chat.content


if __name__ == "__main__":
    main()
