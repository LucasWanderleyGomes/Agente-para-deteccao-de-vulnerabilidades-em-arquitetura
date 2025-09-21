import os
import base64
import tempfile


from openai import AzureOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

env_path = Path(__file__).resolve(strict=True).parent / '.env'
load_dotenv(dotenv_path=env_path)


#carregar variaveis de ambiente do .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")



#configurar cliente do Azure OpenAI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME)




def criar_prompt_modelo_ameacas(tipo_aplicacao,
                                 autenticacao,
                                acesso_internet,
                                dados_sesiveis,
                                descricao_aplicacao):
    
    prompt = f""" Aja como um especialista em ciberseguranca com mais de 20 anos de experiência utilizando a metodologia de 
    ameaças STRIDE para produzir modelos de ameaças abrangentes para uma ampla gama de aplicações. Sua tarefa é analizar o resumo 
    do código, o conteúdo do README e a descrição da aplicação fornecida e gerar um modelo de ameaças detalhado que identifique 
    potenciais ameaças e vulnerabilidades associadas a aplicação.

    Preste atenção na descrição da aplicação e nos detalhes tecnicos fornecidos.

    Para cada uma das categorias do STRIDE (Falsificação de identidade - Spoofing,
     Violação de integridade - Tampering, 
     repúdio - Repudiation, 
     divulgação de informações - Information Disclosure, 
     negação de serviço - Denial of Service e 
     elevação de privilégio - Elevation of Privilege), liste múltiplas (3 a 4) ameaças crediveis que se aplicavel. Cada cenário de ameaça
     deve apresentar uma situação plausível em que a ameaça poderia ocorrer no contexto da aplicação.


    A lista de ameaças deve ser apresentada em formato de tabela, com as seguintes colunas:
    Ao fornecer o modelo de ameaças, utilize uma resposta formato JSON com as chaves "threat_model" e "improvement_suggestions". 
    Em "threat_model", inclua um array de objetos com chaves "Threat Type" (tipo de ameaça), "Scenario" (cenário), "Potential Impact" (impacto potencial).


    Ao fornecer o modelo de ameaças, utilize uma resposta formato JSON com as chaves "threat_model" e "improvement_suggestions".
    Em "threat_model", inclua um array de objetos com chaves "Threat Type" (tipo de ameaça), "Scenario" (cenário), "Potential Impact" (impacto potencial).


    Em "improvement_suggestions", inclua um array de strings que sugerem quais informações adicionais poderiam ser fornecidas para
    tornar o modelo de ameaças mais completo e preciso na proxima iteração.
    Foque em identificar lacunas na descrição da aplicação que, se preenchidas, permitiriam uma análise mais detalhada e precisa, como por exemplo:
        -Detalhes arquiteturais ausentes que ajudariam a identificar ameaças mais específicas.
        -Fluxos de autenticação pouco claros que precisam de mais detalhes.
        -Descrição incompleta dos fluxos de dados
        -Informações técnicas da stack não informadas
        -Fronteiras ou zonas de confiança do sistema não especificadas
        -Descrição incompleta do tratamento de dados sensíveis

    Não fornecça recomendações de segurança genéricas - foque apenas no que ajudaria a criar um modelo de ameaças mais eficientes.


    TIPOS DE APLICAÇÃO: {tipo_aplicacao}
    METODOS DE AUTENTICAÇÃO: {autenticacao}
    EXPOSTA A INTERNET: {acesso_internet}
    DADOS SENSIVEIS: {dados_sesiveis}

    RESUMO DE CODIGO, CONTEUDO DO README E DESCRIÇÃO DA APLICAÇÃO:
    {descricao_aplicacao}





    Exemplo de formato esperado em JSON:
    {{
        "threat_model": [
            {{
                "Threat Type": "Spoofing",
                "Scenario": "Cenario ex1",
                "Potential Impact": "Unauthorized access to user accounts and sensitive data."
            }},
            {{
                "Threat Type": "Tampering",
                "Scenario": "Cenario ex2",
                "Potential Impact": "Data integrity issues and potential data breaches."
            }},
            ...
        ],
        "improvement_suggestions": [
            "Por favor, forneça mais detalhes sobre o fluxo de autenticação entre os componentes.",
            "Considere adicionar informações sobre dados sensíveis são armazenados e trasmitidos.",
            // ... mais sugestões para melhorar o modelo de ameaças
        ]
    }}


    """
    return prompt 




@app.post("/analisar_ameacas")
async def analisar_ameacas(
    Imagem: UploadFile = File(),
    tipo_aplicacao: str = Form(...),
    autenticacao: str = Form(...),
    acesso_internet: str = Form(...),
    dados_sesiveis: str = Form(...),
    descricao_aplicacao: str = Form(...),
):
    try:
        # Criar o prompt para o modelo de ameaças
        prompt = criar_prompt_modelo_ameacas(tipo_aplicacao,
                                             autenticacao,
                                             acesso_internet,
                                             dados_sesiveis,
                                             descricao_aplicacao)
        
        #Salvar a imagem temporariamente

        content = await Imagem.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(Imagem.filename).suffix) as temp_file:
            temp_file.write(content)
            temp_image_path = temp_file.name

        #convert imagem para base64
        with open(temp_image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('ascii')


        # Adicionar a imagem codificada ao prompt
        chat_prompt = [
            {"role": "system", "content": "Você é um especialista em cibersegurança, que analisa desenhos de arquitetura"},
            {"role": "user", 
             "content": [
                {"type": "text",
                  "text": prompt
                  },

                {"type": "image_url", 
                 "image_url": {"url": f"data:image/png;base64,{encoded_string}"}
                 },

                {"type": "text", 
                 "text": "Por favor, analise a imagem e o texto acima e forneça um modelo de ameaças detalhado"
                 }

                   ]},
        ]


        # Chamar a API do Azure OpenAI com o prompt
        response = client.chat.completions.create(
            messages= chat_prompt,
            max_tokens=1500,
            temperature=0.2,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            string=False,
            model = AZURE_OPENAI_DEPLOYMENT_NAME
        )

        os.remove(temp_image_path)  # Remover o arquivo temporário
        # Tentar converter a resposta em JSON
        return JSONResponse(content=response.to_dict(), status_code=200)

        return JSONResponse(content=resposta_json)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Erro ao processar a solicitação", "details": str(e)}, status="500 Internal Server Error")