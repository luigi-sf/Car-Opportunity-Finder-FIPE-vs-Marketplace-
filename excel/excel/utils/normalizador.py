def limpar_numero(valor):
    if not valor:
        return None
    return int(valor.replace(".", "").replace(",", ""))


def extrair_marca_modelo(titulo):
    palavras = titulo.split()

    marca = palavras[0]
    modelo = palavras[1] if len(palavras) > 1 else None

    return marca, modelo


def normalizar_carro(carro):
    marca, modelo = extrair_marca_modelo(carro["titulo"])

    return {
        "titulo": carro.get("titulo"),
        "link": carro.get("link"),
        "preco": limpar_numero(carro.get("preco")),
        "km": limpar_numero(carro.get("km")),
        "ano": int(carro.get("ano")),
        "marca": marca,
        "modelo": modelo
    }