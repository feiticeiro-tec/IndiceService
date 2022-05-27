from time import sleep
import scrapy
from indices.utils.errors import SeridNotIsNumberError,SeridNotInformedError


class CollectSpider(scrapy.Spider):
    name = 'collect'
    allowed_domains = ['www.ipeadata.gov.br']
    start_urls = ['http://www.ipeadata.gov.br/']

    def start_requests(self):
        """Start

        :required:
            :serid: number
        
        :raise:
            ValueError

        """

        serid: str = getattr(self, 'serid', None)#capture key serid
        if not serid:
            raise SeridNotInformedError()
        if not serid.isnumeric():
            raise SeridNotIsNumberError()

        yield scrapy.Request(url=f'http://www.ipeadata.gov.br/exibeserie.aspx?serid={serid}', callback=self.parse)

    def parse(self, response):
        for row in response.css('table#grd_DXMainTable'):
            for celula in row.css('tr')[3:]:
                year_month, indice = celula.css('td')
                year_month = year_month.css('::text').get()
                indice = indice.css('::text').get()
                yield {'date': year_month, 'indice': indice}
