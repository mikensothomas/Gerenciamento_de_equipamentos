from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_password(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)