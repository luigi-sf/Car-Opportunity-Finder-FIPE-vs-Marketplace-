from openpyxl import Workbook

class ExcelPipeline:

    def open_spider(self, spider):
        
        #EVITA REPETICAO
        self.vistos = set()
        
        #CRIAR EXCEL
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Carros"

        #CABECALHO
        self.ws.append([
            "Titulo",
            "Preco",
            "Ano",
            "KM",
            "Link"
        ])

    def process_item(self, item, spider):
        
        if item["link"] in self.vistos:
            return item

        self.vistos.add(item["link"])
         
        #SALVA NO EXCEL
        self.ws.append([
            item.get("titulo"),
            item.get("preco"),
            item.get("ano"),
            item.get("km"),
            item.get("link"),
        ])
        return item

    def close_spider(self, spider):
        
        #EXCEL SAVE - NAME
        self.wb.save("carros.xlsx")
        
        #EVIO DE EMAIL
        from excel.utils.email_sender import enviar_email
        enviar_email()