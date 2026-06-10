import re
import html


def sanitizar(texto: str, max_len: int = 200) -> str:
    if not texto:
        return ""
    texto = html.escape(texto.strip())
    texto = re.sub(r"[<>{};`]", "", texto)
    return texto[:max_len]


def _apenas_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def validar_cpf(cpf: str) -> tuple[bool, str]:
    digitos = _apenas_digitos(cpf)

    if len(digitos) != 11:
        return False, "CPF deve ter 11 dígitos."

    if len(set(digitos)) == 1:
        return False, "CPF inválido."

    def _digito(d, pesos):
        soma = sum(int(d[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = list(range(10, 1, -1))
    pesos2 = list(range(11, 1, -1))

    d1 = _digito(digitos, pesos1)
    d2 = _digito(digitos, pesos2)

    if int(digitos[9]) != d1 or int(digitos[10]) != d2:
        return False, "CPF inválido — dígitos verificadores incorretos."

    return True, ""


def validar_cartao_sus(cartao: str) -> tuple[bool, str]:
    digitos = _apenas_digitos(cartao)
    if len(digitos) != 15:
        return False, "Cartão SUS deve ter 15 dígitos."
    return True, ""


def validar_campo_sus(valor: str) -> tuple[bool, str]:
    limpo = _apenas_digitos(valor)
    if len(limpo) == 11:
        return validar_cpf(valor)
    if len(limpo) == 15:
        return validar_cartao_sus(valor)
    return False, "Digite um CPF válido (11 dígitos) ou Cartão SUS (15 dígitos)."


def validar_nome(nome: str) -> tuple[bool, str]:
    nome = nome.strip()
    if len(nome) < 3:
        return False, "Nome deve ter ao menos 3 caracteres."
    if not re.match(r"^[A-Za-zÀ-ÿ\s'\-]+$", nome):
        return False, "Nome deve conter apenas letras e espaços."
    return True, ""


def validar_telefone(telefone: str) -> tuple[bool, str]:
    digitos = _apenas_digitos(telefone)
    if len(digitos) < 10 or len(digitos) > 11:
        return False, "Telefone inválido. Use o formato (DD) 9XXXX-XXXX ou (DD) XXXX-XXXX."
    dd = int(digitos[:2])
    if dd < 11 or dd > 99:
        return False, "DDD inválido. Informe um DDD válido (ex: 11, 21, 31)."
    return True, ""


def formatar_telefone(telefone: str) -> str:
    digitos = _apenas_digitos(telefone)
    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2]}{digitos[3:7]}-{digitos[7:]}"
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    return telefone
