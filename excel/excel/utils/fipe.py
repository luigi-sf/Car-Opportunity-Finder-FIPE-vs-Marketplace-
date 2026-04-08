import requests
import unicodedata

#URL_BASE

URL_BASE = "https://fipe.parallelum.com.br/api/v2/cars"

#NORMALIZACAO
def normalizar(texto):
    if not texto:
        return ""
    return unicodedata.normalize('NFKD', texto)\
        .encode('ASCII', 'ignore')\
        .decode('ASCII')\
        .lower()



#BUSCA FIPE
def buscar_fipe(marca, modelo, ano):
    try:
        marca_n = normalizar(marca)
        modelo_n = normalizar(modelo)

        
        #MARCAS
        marcas = requests.get(f"{URL_BASE}/brands").json()
        marca_id = next(
            (m["code"] for m in marcas if marca_n in normalizar(m["name"])),
            None
        )

        if not marca_id:
            print("Marca não encontrada:", marca)
            return None

        
        #MODELOS
        modelos = requests.get(f"{URL_BASE}/brands/{marca_id}/models").json()

        modelo_id = None
        ano_id = None

        for m in modelos:
            nome = normalizar(m["name"])

            if modelo_n in nome:
                anos = requests.get(
                    f"{URL_BASE}/brands/{marca_id}/models/{m['code']}/years"
                ).json()

                for a in anos:
                    if str(ano) in a["name"]:
                        modelo_id = m["code"]
                        ano_id = a["code"]
                        print(f"Modelo encontrado: {m['name']} | {a['name']}")
                        break

                if modelo_id:
                    break

        if not modelo_id or not ano_id:
            print("Nenhum modelo compatível com ano:", modelo, ano)
            return None

       #PRECO
        url = f"{URL_BASE}/brands/{marca_id}/models/{modelo_id}/years/{ano_id}"
        dados = requests.get(url).json()

        print("DEBUG dados:", dados)

        preco_str = dados.get("price")

        if not preco_str:
            print(" Preço não encontrado na API")
            return None

        preco_str = preco_str.replace("R$ ", "").replace(".", "").replace(",", ".")
        preco = float(preco_str)

        return preco

    except Exception as e:
        print("Erro:", e)
        return None



def analisar_carro(carro):
    fipe = buscar_fipe_cache(
        carro["marca"],
        carro["modelo"],
        carro["ano"]
    )

    if not fipe:
        return None

    desconto = (fipe - carro["preco"]) / fipe

    if (
        desconto >= 0.10 and
        carro["km"] <= 80000 and
        carro["ano"] >= 2018
    ):
        return {
            **carro,
            "fipe": fipe,
            "desconto": round(desconto * 100, 2)
        }

    return None
# CACHE
cache_fipe = {}

def buscar_fipe_cache(marca, modelo, ano):
    chave = f"{marca}-{modelo}-{ano}"

    if chave in cache_fipe:
        return cache_fipe[chave]

    preco = buscar_fipe(marca, modelo, ano)
    cache_fipe[chave] = preco

    return preco

