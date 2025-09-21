# Agente-para-deteccao-de-vulnerabilidades-em-arquitetura

# 🛡️ Threat Model Generator (STRIDE)

Este projeto permite analisar ameaças de segurança em aplicações utilizando a metodologia **STRIDE**, combinando descrição técnica e diagramas de arquitetura.  
O backend foi desenvolvido em **FastAPI** com integração ao **Azure OpenAI**, e o frontend é um formulário simples em **HTML + CSS** em tons de laranja e preto.

---

## 🚀 Como rodar o backend

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo


2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` com suas credenciais do **Azure OpenAI**:

   ```env
   AZURE_OPENAI_API_KEY=xxxx
   AZURE_OPENAI_ENDPOINT=https://seu-endpoint.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-06-01
   AZURE_OPENAI_DEPLOYMENT_NAME=seu-deployment
   ```

5. Rode o servidor:

   ```bash
   uvicorn main:app --reload
   ```

O backend estará rodando em:

```
http://127.0.0.1:8000
```

---

## 🎨 Como rodar o frontend

1. Abra o arquivo `index.html` na sua máquina (clique duas vezes ou use `Open With Browser`).
2. Se necessário, edite a URL da API no código:

   ```javascript
   const endpoint = "http://127.0.0.1:8000/analisar_ameacas";
   ```
3. Preencha o formulário, envie os dados e veja o resultado aparecer no painel.

---

## 📂 Estrutura do projeto

```
.
├── backend/
│   ├── main.py          # Código FastAPI
│   ├── requirements.txt # Dependências
│   └── .env.example     # Exemplo de variáveis de ambiente
├── frontend/
│   └── index.html       # Formulário HTML + CSS
└── README.md
```

---

## ⚙️ Tecnologias utilizadas

* **Python 3.10+**
* **FastAPI**
* **Azure OpenAI**
* **HTML5 + CSS3 (Frontend simples)**

---

## 📌 Observações

* O backend precisa de uma conta no **Azure OpenAI** para funcionar corretamente.
* O frontend pode ser aberto localmente em qualquer navegador moderno.
* Para hospedar o projeto, pode-se usar serviços como **Vercel/Netlify (frontend)** e **Render/Azure/Heroku (backend)**.



---

