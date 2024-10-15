from unittest.mock import MagicMock, patch

import pytest

# Importa a função main do módulo templates dentro do pacote minicurso_agentes_langchain_basico
from minicurso_agentes_langchain_basico.templates import main


def test_main():
    """
    Testa a função main do templates.py.

    Este teste simula as entradas do usuário para a dúvida e o nível de programação,
    mocka o método invoke do modelo e verifica se a função main retorna o conteúdo esperado.
    """
    # Valores simulados para as entradas e a resposta do modelo
    entrada_pergunta = "Entender listas em Python"
    entrada_nivel = "Iniciante"
    resposta_modelo = "Listas em Python são usadas para armazenar múltiplos itens em uma única variável."

    with patch("builtins.input", side_effect=[entrada_pergunta, entrada_nivel]):
        # Mock do Agente e do método invoke
        with patch("minicurso_agentes_langchain_basico.templates.Agente") as MockAgente:
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
            # Verifica se as mensagens formatadas contêm os valores de entrada
            assert chamadas[1].content == f"Acho que estou no nível {entrada_nivel} em programação"
            assert chamadas[3].content == f"Quero aprender {entrada_pergunta}"
