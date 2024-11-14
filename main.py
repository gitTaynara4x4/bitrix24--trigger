import requests

# URL do Webhook Bitrix24
WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg"

# O campo personalizado que você quer monitorar
CUSTOM_FIELD = "UF_CRM_1700661314351"

def obter_deals():
    url = f"{WEBHOOK_URL}/crm.deal.list"
    
    # Fazendo a requisição GET para obter os negócios
    response = requests.get(url)

    # Verificando a resposta da API
    if response.status_code == 200:
        return response.json()  # Retorna os negócios no formato JSON
    else:
        print(f"Erro ao obter os negócios. Código de resposta: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None

def disparar_fluxo_trabalho(deal_id):
    url = f"{WEBHOOK_URL}/bizproc.workflow.start"
    
    # Dados para disparar o fluxo de trabalho
    payload = {
        'DOCUMENT_ID': ['CRM_DEAL', deal_id],  # Tipo e ID do documento (negócio)
        'TEMPLATE_ID': 1438,  # ID do template do fluxo de trabalho
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print(f"Fluxo de trabalho disparado com sucesso para o deal {deal_id}")
    else:
        print(f"Erro ao disparar o fluxo de trabalho. Código de resposta: {response.status_code}")
        print(f"Resposta: {response.text}")

def monitorar_cep():
    deals = obter_deals()
    if deals:
        for deal in deals['result']:
            deal_id = deal['ID']
            cep_atual = deal.get(CUSTOM_FIELD)

            if cep_atual:  # Verifica se o campo existe e tem valor
                print(f"Campo CEP encontrado para o deal {deal_id}: {cep_atual}")
                # Aqui você pode comparar e disparar o fluxo de trabalho
                # Exemplo: Comparar com valor anterior e disparar o fluxo
                disparar_fluxo_trabalho(deal_id)
            else:
                print(f"Campo CEP não encontrado ou está vazio para o deal {deal_id}")

# Função principal
def main():
    monitorar_cep()

if __name__ == "__main__":
    main()
