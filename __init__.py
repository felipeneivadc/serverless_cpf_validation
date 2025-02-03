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
