import scrapy
import re
from excel.utils.normalizador import normalizar_carro
class ExcelSpider(scrapy.Spider):
    name = "excel"
    
    #CARRO BOM
    def carro_bom(self, preco, km, ano):
        try:
            preco = int(re.sub(r"\D", "", preco))
            km = int(km.replace(".", "").replace(",", "").lower().replace("km", "").strip())
            ano = int(ano)

            return (
                preco <= 50000 and
                km <= 80000 and
                ano >= 2018
            )
        except:
            return False
    
    

    def start_requests(self):
        base_url = "https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/_HAS*HISTORIC*INFORMATION_242085_NoIndex_True_VEHICLE*TYPE_398351"

        for page in range(1, 42):
            if page == 1:
                url = base_url
                #PAGINACAO DO ML E DIFERENTE
            else:
                offset = (page - 1) * 48 + 1
                url = f"https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/_Desde_{offset}_HAS*HISTORIC*INFORMATION_242085_NoIndex_True_VEHICLE*TYPE_398351"

            yield scrapy.Request(
                url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
                callback=self.parse
            )

    async def parse(self, response):
        page = response.meta.get("playwright_page")

        if not page:
            return
        #AWAIT DIV PRINCIPAL
        await page.wait_for_selector('div.poly-card')

        vistos = {}
        ultimo_total = 0

        for _ in range(15):
            content = await page.content()
            new_response = response.replace(body=content)
            #DIV PRINCIPAL
            rows = new_response.css('div.poly-card')
            #ROWS
            for row in rows:
                titulo = row.css(".poly-component__title::text").get()
                link = row.css(".poly-component__title::attr(href)").get()

                preco_int = row.css(".andes-money-amount__fraction::text").get()
                preco_dec = row.css(".andes-money-amount__cents::text").get()

                infos = row.css(".poly-attributes_list__item::text").getall()

                ano = None
                km = None

                for info in infos:
                    info = info.strip()

                    # KM
                    km_match = re.search(r"([\d\.]+)\s*km", info.lower())
                    if km_match:
                        km = km_match.group(1)

                    # ANO
                    ano_match = re.search(r"\b(19|20)\d{2}\b", info)
                    if ano_match:
                        ano = ano_match.group(0)

                preco = None
                if preco_int:
                    preco = f"{preco_int},{preco_dec}" if preco_dec else preco_int

                if titulo and titulo not in vistos and self.carro_bom(preco, km, ano):
                    vistos[titulo] = {
                        "titulo": titulo,
                        "link": response.urljoin(link),
                        "preco": preco,
                        "km": km,
                        "ano": ano
                    }

            if len(vistos) == ultimo_total:
                print("Parando: não encontrou novos produtos")
                break

            ultimo_total = len(vistos)

            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1200)

        await page.close()

        for item in vistos.values():
            carro = normalizar_carro(item)
            yield carro