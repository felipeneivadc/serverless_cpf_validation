# Aplicação Serverless Azure de Validação de CPF

## 1. Criando o Recurso Azure Function App

<div align="center"> <img src="https://github.com/devcaiada/serveless-cpf-validation/blob/main/assets/serverless.png?raw=true" alt="Descrição da Imagem"> </div>

### Passo 1: Criar um Novo Recurso no Azure

1. Acesse o portal do [**Azure**](https://portal.azure.com/):

2. No menu lateral esquerdo, clique em “**Create a resource**” e procure por “**Function App**”.

3. Clique em “**Create**” e preencha os seguintes detalhes:

   - **Subscription**: Selecione sua assinatura do Azure.

   - **Resource Group**: Crie um novo grupo de recursos ou selecione um existente.

   - **Function App name**: Escolha um nome único para sua Function App.

   - **Publish**: Selecione “Code”.

   - **Runtime stack**: Selecione “Python”.

   - **Version**: Selecione a versão do Python que deseja utilizar (por exemplo, 3.9).

   - **Region**: Selecione a região mais próxima de você.

4. Clique em “Next: Hosting” e configure o armazenamento:

- Storage Account: Crie uma nova conta de armazenamento ou selecione uma existente.

5. Clique em “Next: Monitoring” e desative o Application Insights se não for necessário.

6. Clique em “Review + create” e, em seguida, “Create” para finalizar a criação do recurso.

## 2. Configurando o Projeto Azure Functions Localmente

### Passo 2: Instalar as Ferramentas Necessárias

- Azure CLI: [Instalação da Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)

- Func Core Tools: [Instalação do Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local)

### Passo 3: Criar um Novo Projeto de Azure Functions

Abra o terminal e execute os seguintes comandos:

```Sh
func init serveless-cpf-validation --python
cd serveless-cpf-validation
func new --name ValidateCPF --template "HTTP trigger" --authlevel "function"
```

## 3. Código da Função para Validação de CPF

### Passo 4: Adicionar o Código no Arquivo `__init__.py`

No arquivo `ValidateCPF/__init__.py`, adicione o seguinte código:

```python
import logging
import azure.functions as func
import re

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais (CPFs inválidos comuns)
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito_verificador = 11 - (soma % 11)
    if primeiro_digito_verificador >= 10:
        primeiro_digito_verificador = 0

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito_verificador = 11 - (soma % 11)
    if segundo_digito_verificador >= 10:
        segundo_digito_verificador = 0

    # Verifica se os dígitos verificadores são válidos
    return (int(cpf[9]) == primeiro_digito_verificador and
            int(cpf[10]) == segundo_digito_verificador)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Recebendo requisição para validação de CPF.')

    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            cpf = req_body.get('cpf')

    if cpf:
        valido = validar_cpf(cpf)
        return func.HttpResponse(f"O CPF {cpf} é {'válido' if valido else 'inválido'}.")
    else:
        return func.HttpResponse(
             "Por favor, passe o CPF na query string ou no corpo da requisição.",
             status_code=400
        )
```

## 4. Configurando o Arquivo `function.json`

### Passo 5: Atualizar o Arquivo `function.json`

No arquivo `ValidateCPF/function.json`, adicione o seguinte conteúdo:

```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

## 5. Publicando o Projeto no Azure

### Passo 6: Fazer o Deploy do Projeto no Azure

Execute os seguintes comandos no terminal para fazer o deploy do projeto:

```sh
az login
az account set --subscription "<seu-id-de-assinatura>"
func azure functionapp publish <nome-da-sua-function-app>
```

## Contribuição <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Rocket.png" alt="Rocket" width="25" height="25" />

Sinta-se à vontade para contribuir com melhorias neste projeto. Envie um pull request ou abra uma issue para discussão.
