# core/security.py
from passlib.context import CryptContext

# Configuração do CryptContext para usar bcrypt
CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função para verificar se a senha está correta comparando
    a senha em texto puro, informando pelo usuário, e o hash da senha
    que estará salvo no banco de dados durante a criação da conta.
    """
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Função que gera e retorna o hash da senha usando passlib
    """
    return CRIPTO.hash(senha)
