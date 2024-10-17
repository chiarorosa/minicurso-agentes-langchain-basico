from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Import com caminho relativo
from .agente import Agente


def main():
    """
    Executa o fluxo principal do assistente de programação com templates de chat.

    Este método inicializa um agente, configura os templates de chat,
    coleta as entradas do usuário para a pergunta e nível de programação,
    formata as mensagens, invoca o modelo para obter uma resposta
    e retorna o conteúdo da resposta.

    Retorna:
        str: O conteúdo da resposta gerada pelo modelo de IA.
    """
    agente = Agente()

    chat_templates = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="Você é um assistente especializado em ajudar alunos que estão aprendendo os conceitos básicos de programação"
            ),
            HumanMessagePromptTemplate.from_template(
                template="Acho que estou no nível {nivel} em programação",
            ),
            AIMessage(content="Entendi seu nível de conhecimento, você precisa de ajuda com o que?"),
            HumanMessagePromptTemplate.from_template(
                template="Quero aprender {pergunta}",
            ),
        ]
    )

    pergunta = input("Qual sua dúvida sobre programação? ")
    nivel = input("Qual seu nível em programação? ")

    prompt = chat_templates.format_messages(
        nivel=nivel,
        pergunta=pergunta,
    )

    chat = agente.modelo.invoke(prompt)
    return chat.content


if __name__ == "__main__":
    main()
