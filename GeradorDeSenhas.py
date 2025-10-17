import string
import random

def gerar_senha(comprimento: int) -> str:
    """
    Gera uma senha aleatória contendo letras, dígitos e caracteres especiais.

    Args:
        comprimento (int): Tamanho desejado da senha.

    Returns:
        str: Senha gerada.
    """
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
    return senha

if __name__ == "__main__":
    comprimento_senha = 22
    senha_gerada = gerar_senha(comprimento_senha)
    print(f"Senha gerada: {senha_gerada}")
