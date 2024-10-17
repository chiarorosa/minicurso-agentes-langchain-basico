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

    pergunta = input("Olá aluno, tire sua dúvida comigo...")

    mensagens = [
        SystemMessage(
            content="Você é um assistente especializado em ajudar alunos que estão aprendendo os conceitos básicos de programação. Seu objetivo é responder de forma clara, amigável e didática, adaptando-se ao nível de entendimento de cada estudante. Sempre que possível, forneça exemplos simples e evite jargões técnicos complexos, a menos que seja necessário explicá-los de maneira acessível. Se o aluno fizer uma pergunta muito ampla, ajude-o a focar no problema específico. Encorage o raciocínio lógico e incentive a prática, oferecendo dicas e sugestões úteis. Lembre-se de que os alunos estão no começo da jornada e podem precisar de paciência e explicações detalhadas. Seu foco está em linguagens como Python, JavaScript e lógica de programação, mas você pode ajudar em outros tópicos básicos também, como estruturas de dados simples e controle de fluxo."
        ),
        HumanMessage(content="Eu sou um programador iniciante"),
        AIMessage(content="Como posso te ajudar hoje?"),
        HumanMessage(content=pergunta),
    ]

    chat = agente.modelo.invoke(mensagens)
    return chat.content


if __name__ == "__main__":
    main()
