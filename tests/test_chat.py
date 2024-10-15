from unittest.mock import MagicMock, patch

import pytest

# Importa a função main do módulo chat dentro do pacote minicurso_agentes_langchain_basico
from minicurso_agentes_langchain_basico.chat import main


def test_main():
    """
    Testa a função main do chat.py.

    Este teste simula a entrada do usuário e mocka o método invoke
    do modelo para verificar se a função main retorna o conteúdo esperado.
    """
    # Valores simulados para as entradas e a resposta do modelo
    entrada_pergunta = "Como funcionam os loops em Python?"
    resposta_modelo = "Loops em Python são usados para iterar sobre sequências."

    with patch("builtins.input", return_value=entrada_pergunta):
        # Mock do Agente e do método invoke
        with patch("minicurso_agentes_langchain_basico.chat.Agente") as MockAgente:
            mock_agente_instance = MockAgente.return_value
            mock_model = MagicMock()
            mock_model.invoke.return_value.content = resposta_modelo
            mock_agente_instance.modelo = mock_model

            # Chama a função main e verifica a resposta
            resultado = main()
            assert resultado == resposta_modelo

            # Verifica se o método invoke foi chamado corretamente
            assert mock_model.invoke.called
            chamadas = mock_model.invoke.call_args[0][0]
            assert len(chamadas) == 4
            assert chamadas[3].content == entrada_pergunta
