from src.core.security import encrypt_xsalsa20, decrypt_xsalsa20

SENSITIVE_MAP = {
    "nombre_completo": "nombre_completo_cifrado",
    "telefono": "telefono_cifrado",
}

REVERSE_MAP = {v: k for k, v in SENSITIVE_MAP.items()}


def encrypt_fields(data: dict) -> dict:
    """Toma un dict con campos planos (nombre_completo, telefono)
    y devuelve uno con los campos cifrados (nombre_completo_cifrado, telefono_cifrado)."""
    result = {}
    for k, v in data.items():
        if k in SENSITIVE_MAP and v:
            result[SENSITIVE_MAP[k]] = encrypt_xsalsa20(v)
        else:
            result[k] = v
    return result


def decrypt_fields(data: dict) -> dict:
    """Toma un dict con campos cifrados (nombre_completo_cifrado, telefono_cifrado)
    y devuelve uno con los campos descifrados (nombre_completo, telefono)."""
    result = {}
    for k, v in data.items():
        if k in REVERSE_MAP and v:
            result[REVERSE_MAP[k]] = decrypt_xsalsa20(v)
        else:
            result[k] = v
    return result
