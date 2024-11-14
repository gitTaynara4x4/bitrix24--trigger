import requests

# URL do Webhook Bitrix24
WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg"

# ID do fluxo de trabalho que você quer disparar
WORKFLOW_ID = 1438  # Use o ID do fluxo de trabalho que você quer rodar

# O campo personalizado que você quer monitorar
CUSTOM_FIELD = "UF_CRM_1700661314351"

# Função para obter os negócios (deals) e verificar se o campo CEP foi alterado
def obter_deals():
    url = f"{WEBHOOK_URL}/crm.deal.list"
    
    # Fazendo a requisição GET para obter os negócios
    response = requests.get(url)

    # Verificando a resposta da API
    if response.status_code == 200:
        # Retorna os dados dos negócios em formato JSON
        return response.json()
    else:
        print(f"Erro ao obter os negócios: {response.text}")
        return None

# Função para disparar o fluxo de trabalho
def disparar_fluxo_trabalho(deal_id):
    url = f"{WEBHOOK_URL}/bizproc.workflow.start"
    
    # Dados para disparar o fluxo de trabalho
    payload = {
        'DOCUMENT_ID': ['CRM_DEAL', deal_id],  # Tipo e ID do documento (negócio)
        'TEMPLATE_ID': WORKFLOW_ID,  # ID do template do fluxo de trabalho
    }

    # Fazendo a requisição POST para disparar o fluxo de trabalho
    response = requests.post(url, data=payload)

    # Verificando a resposta da API
    if response.status_code == 200:
        print(f"Fluxo de trabalho {WORKFLOW_ID} disparado com sucesso para o deal {deal_id}")
    else:
        print(f"Erro ao disparar o fluxo de trabalho: {response.text}")

def monitorar_cep():
    # Obtém a lista de negócios
    deals = obter_deals()

    if deals:
        # Armazenando o valor anterior do campo
        # (Você pode armazenar isso em um banco de dados ou arquivo para persistência)
        # Vamos comparar o valor do campo "CEP" para detectar alterações

        for deal in deals['result']:
            deal_id = deal['ID']
            cep_atual = deal.get(CUSTOM_FIELD)

            if cep_atual:  # Verifica se o campo existe e tem valor
                # Aqui, você deve armazenar o valor anterior do CEP e comparar
                # Se houver diferença, aciona o fluxo de trabalho
                # Vamos simular isso com uma variável fictícia "cep_antigo"
                cep_antigo = "00000000"  # Armazenado anteriormente (exemplo)
                
                if cep_atual != cep_antigo:
                    print(f"CEP alterado para {cep_atual}. Disparando fluxo de trabalho...")
                    disparar_fluxo_trabalho(deal_id)
                    # Atualize o valor de "cep_antigo" para o novo valor (armazenar permanentemente)
                    cep_antigo = cep_atual
            else:
                print(f"Campo CEP não encontrado para o deal {deal_id}")

# Função principal
def main():
    monitorar_cep()

if __name__ == "__main__":
    main()
