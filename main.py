import requests
import time

# URL do Webhook Bitrix24
WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg"

# O campo personalizado que você quer monitorar
CUSTOM_FIELD = "UF_CRM_1700661314351"

def obter_deals():
    url = f"{WEBHOOK_URL}/crm.deal.list"
    start = 0  # Variável de controle para paginação
    all_deals = []

    while True:
        params = {
            'select': ['ID', CUSTOM_FIELD],  # Selecionando o campo personalizado
            'start': start,  # Página atual
            'limit': 50  # Limite de 50 negócios por vez (ajuste conforme necessário)
        }

        try:
            # Fazendo a requisição GET para obter os negócios
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                all_deals.extend(data['result'])  # Adiciona os negócios retornados à lista

                # Se houver mais negócios, atualiza o start com o ID do último negócio
                if 'next' in data:
                    start = data['next']
                else:
                    break  # Não há mais negócios, sai do loop

            else:
                print(f"Erro ao obter os negócios. Código de resposta: {response.status_code}")
                print(f"Resposta: {response.text}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição: {e}")
            break

    return all_deals

def disparar_fluxo_trabalho(deal_id):
    url = f"{WEBHOOK_URL}/bizproc.workflow.start"
    
    # Dados para disparar o fluxo de trabalho
    payload = {
        'DOCUMENT_ID': ['CRM_DEAL', deal_id],  # Tipo e ID do documento (negócio)
        'TEMPLATE_ID': 1438,  # ID do template do fluxo de trabalho
    }

    try:
        # Fazendo a requisição POST para disparar o fluxo de trabalho
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print(f"Fluxo de trabalho disparado com sucesso para o deal {deal_id}")
        else:
            print(f"Erro ao disparar o fluxo de trabalho. Código de resposta: {response.status_code}")
            print(f"Resposta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao disparar o fluxo: {e}")

def monitorar_cep():
    deals = obter_deals()
    if deals:
        for deal in deals:
            deal_id = deal['ID']
            # Verificando se o campo personalizado 'UF_CRM_1700661314351' está presente
            cep_atual = deal.get(CUSTOM_FIELD)
            
            if cep_atual:  # Se o campo tiver valor, dispara o fluxo de trabalho
                print(f"Campo CEP encontrado para o deal {deal_id}: {cep_atual}")
                disparar_fluxo_trabalho(deal_id)
            else:
                # Caso o campo não exista ou esteja vazio, apenas registra o erro e continua
                print(f"Campo CEP não encontrado ou está vazio para o deal {deal_id}")
            
            # Adiciona delay entre requisições para evitar bloqueios
            time.sleep(2)  # Delay de 1 segundo entre as requisições (ajuste conforme necessário)

def main():
    monitorar_cep()

if __name__ == "__main__":
    main()
