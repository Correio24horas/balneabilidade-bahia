from scrapy import Request, Spider


URL_BOLETIM = 'http://balneabilidade.inema.ba.gov.br/index.php/relatoriodebalneabilidade/geraBoletim?idcampanha={id_campanha}'


class ListaBoletinsSpider(Spider):
    name = 'inema-balneabilidade-lista-boletins'
    start_urls = ['http://balneabilidade.inema.ba.gov.br/index.php/relatoriodebalneabilidade/boletim']

    def parse(self, response):
        for campanha in response.xpath('//select[@id="idcampanha"]/option'):
            id_campanha = campanha.xpath('./@value').extract()[0]
            if id_campanha == '-1':  # 'TODAS AS CAMPANHAS'
                continue
            partes = (campanha.xpath('./text()').extract()[0]
                              .strip()
                              .replace('CAMPANHA EMERG', 'CAMPANHA_EMERG')
                              .split())
            partes_data = [int(parte) for parte in partes[-1].split('/')]
            data = f'{partes_data[2]}-{partes_data[1]:02d}-{partes_data[0]:02d}'

            yield {
                'costa': partes[2],
                'data_emissao': data,
                'id_campanha': id_campanha,
                'numero_boletim': partes[1],
                'tipo_campanha': partes[0],
                'url': URL_BOLETIM.format(id_campanha=id_campanha),
            }
