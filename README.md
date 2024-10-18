### Minicurso - Agentes com LangChain Básico

Bem-vindo ao repositório **minicurso-agentes-langchain-basico**! Este projeto foi desenvolvido para oferecer uma introdução prática e acessível ao desenvolvimento de agentes inteligentes utilizando a framework [LangChain](https://langchain.com/) em conjunto com a [Google Generative AI](https://ai.google/).

#### 📚 O que você encontrará aqui:

- **Conteúdo Estruturado**: Conteúdo dividido em etapas que abordam desde os conceitos fundamentais até a implementação de agentes avançados utilizando LangChain e Google Generative AI.
- **Exemplos de Código**: Scripts comentados e exemplos práticos que demonstram como integrar LangChain com as APIs da Google Generative AI para criar soluções inovadoras.
- **Recursos Complementares**: Links para documentação oficial, tutoriais adicionais e materiais de referência para aprofundar seus conhecimentos sobre LangChain e Google Generative AI.

#### 🎯 Objetivo do Minicurso:

Capacitar desenvolvedores, entusiastas de inteligência artificial e estudantes a construir e implementar agentes baseados em linguagem natural utilizando LangChain em conjunto com as ferramentas da Google Generative AI, promovendo uma compreensão sólida das ferramentas e técnicas envolvidas.

#### 🚀 Como Começar:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/minicurso-agentes-langchain-basico.git
   ```

2. **(Opcional) Configure o pyenv para gerenciar a versão do Python:**

   - **Instale o pyenv:**

     - **macOS/Linux:**
       Siga as instruções de instalação no [repositório oficial do pyenv](https://github.com/pyenv/pyenv#installation).
     - **Windows:**
       Utilize o [pyenv-win](https://github.com/pyenv-win/pyenv-win) seguindo as instruções fornecidas.

   - **Instale a versão específica do Python necessária:**

     ```bash
     pyenv install 3.11
     ```

     _(Substitua `3.11` pela versão requerida pelo projeto, se diferente.)_

   - **Defina a versão do Python para o projeto:**
     ```bash
     pyenv local 3.11
     ```
     Isso criará um arquivo `.python-version` na raiz do projeto, garantindo que todos utilizem a mesma versão do Python.

3. **Crie o arquivo `.env`:**

   - Renomeie o arquivo chamado `.env-modelo` na raiz do projeto para `.env`.
   - Adicione sua chave de API obtida diretamente no Google através do link: [Obter API Key](https://aistudio.google.com/app/apikey).
   - Adicione sua chave de API Google Serper: [Obter API Key](https://serper.dev/api-key).
   - Adicione sua chave de API Exa.ai: [Obter API Key](https://dashboard.exa.ai/api-keys).
   - O conteúdo do `.env` deve ser:
     ```env
     API_KEY=Sua_Chave_API_Aqui
     SERPER_API_KEY=Sua_Chave_API_Aqui
     EXA_API_KEY=Sua_Chave_API_Aqui
     ```

4. **Instale o Poetry:**

   - Certifique-se de ter o [Poetry](https://python-poetry.org/) instalado no seu ambiente. Caso não tenha, você pode instalá-lo seguindo as instruções na [documentação oficial](https://python-poetry.org/docs/#installation).

5. **Instale as dependências do projeto:**

   ```bash
   poetry install
   ```

6. **Teste a configuração do ambiente:**
   - Execute o comando abaixo para verificar se todo o ambiente está configurado corretamente:
     ```bash
     poetry run validar
     ```
   - Se tudo estiver configurado corretamente, você poderá perguntar algo para o Gemini.

#### 🤝 Contribuições:

Contribuições são bem-vindas! Se você deseja adicionar conteúdo, corrigir erros ou melhorar a estrutura do curso, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

#### 📄 Licença:

Este projeto está licenciado sob a [MIT License](LICENSE).
