import os
from unittest.mock import MagicMock, patch

import pytest

# Importa a classe Agente do módulo agente dentro do pacote minicurso_agentes_langchain_basico
from minicurso_agentes_langchain_basico.pacote_agentes.agente import Agente


def test_agente_init_success():
    """
    Testa a inicialização bem-sucedida da classe Agente.

    Este teste verifica se a classe Agente é inicializada corretamente quando a chave da API está configurada.
    Ele mocka a função config para retornar uma chave de API válida e mocka a classe ChatGoogleGenerativeAI.
    """
    api_key = "fake_api_key"
    modelo_nome = "gemini-1.5-flash"

    with patch("minicurso_agentes_langchain_basico.agente.config", return_value=api_key):
        with patch("minicurso_agentes_langchain_basico.agente.ChatGoogleGenerativeAI") as MockChat:
            mock_model_instance = MockChat.return_value
            agente = Agente(modelo=modelo_nome)

            # Verifica se a variável de ambiente foi configurada corretamente
            assert os.environ["GOOGLE_API_KEY"] == api_key

            # Verifica se o modelo foi instanciado com o nome correto
            MockChat.assert_called_once_with(model=modelo_nome)
            assert agente.modelo == mock_model_instance


def test_agente_init_missing_api_key():
    """
    Testa a inicialização da classe Agente quando a chave da API está ausente.

    Este teste verifica se a classe Agente lança um ValueError quando a chave da API não está configurada.
    Ele mocka a função config para lançar uma exceção, simulando a ausência da chave da API.
    """
    with patch("minicurso_agentes_langchain_basico.agente.config", side_effect=Exception("Config not found")):
        with pytest.raises(ValueError) as exc_info:
            Agente()

        assert str(exc_info.value) == "Chave da API não configurada. Configure a chave da API no arquivo .env."


def test_agente_instanciar_modelo_failure():
    """
    Testa a inicialização da classe Agente quando a instanciação do modelo falha.

    Este teste verifica se a classe Agente lança um ValueError quando ocorre uma exceção durante a instanciação do modelo.
    Ele mocka a classe ChatGoogleGenerativeAI para lançar uma exceção.
    """
    api_key = "fake_api_key"
    modelo_nome = "gemini-1.5-flash"

    with patch("minicurso_agentes_langchain_basico.agente.config", return_value=api_key):
        with patch(
            "minicurso_agentes_langchain_basico.agente.ChatGoogleGenerativeAI",
            side_effect=Exception("Instantiation Error"),
        ):
            with pytest.raises(ValueError) as exc_info:
                Agente(modelo=modelo_nome)

            assert str(exc_info.value) == "Erro ao instanciar o modelo Google Generative AI: Instantiation Error"


def test_agente_modelo_attribute():
    """
    Testa se o atributo 'modelo' da classe Agente é corretamente atribuído.

    Este teste verifica se, após a inicialização, o atributo 'modelo' da instância de Agente
    está corretamente atribuído ao objeto retornado por ChatGoogleGenerativeAI.
    """
    api_key = "fake_api_key"
    modelo_nome = "gemini-1.5-flash"

    with patch("minicurso_agentes_langchain_basico.agente.config", return_value=api_key):
        with patch("minicurso_agentes_langchain_basico.agente.ChatGoogleGenerativeAI") as MockChat:
            mock_model_instance = MockChat.return_value
            agente = Agente(modelo=modelo_nome)

            assert agente.modelo == mock_model_instance
