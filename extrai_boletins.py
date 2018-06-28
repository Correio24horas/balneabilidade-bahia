import csv
import io
import logging
import lzma
import re
from pathlib import Path

import rows
from scrapy import Request, Spider


logging.getLogger("pdfminer").setLevel(logging.ERROR)
regexp_costa = re.compile('[ -]([A-Z]{3,4})[ -]')


def clean(text):
    return text.replace('\n', ' ').strip()


def extrai_costa(ponto):
    """
    >>> extrai_costa('2ª. Praia de Morro de São Paulo - CDD- SP 200')
    'CDD'
    >>> extrai_costa('Costa - Canavieiras - CCA CN 100')
    'CCA'
    >>> extrai_costa('Madre de Deus - BTS MD 100')
    'BTS'
    >>> extrai_costa('Nativos - CDES NT 100')
    'CDES'
    """

    return regexp_costa.findall(ponto)[0]


class ExtraiBoletins(Spider):
    name = 'inema-balneabilidade-extrai-boletins'

    def start_requests(self):
        download_path = Path('./download')
        if not download_path.exists():
            download_path.mkdir()

        fobj = io.TextIOWrapper(
            lzma.open('data/output/boletins.csv.xz'),
            encoding='utf8'
        )
        for row in csv.DictReader(fobj):
            filename = download_path / f'{row["id_campanha"]}.pdf'
            row['filename'] = filename
            if filename.exists():
                url = 'file://' + str(filename.absolute())
            else:
                url = row['url']

            yield Request(url=url, meta=row)

    def parse(self, response):
        meta = response.request.meta.copy()
        filename = meta['filename']
        meta['costa_menu'] = meta['costa']
        del_keys = [key for key in meta.keys()
                    if key.startswith('download_')
                    or key in ('url', 'filename', 'depth', 'costa')]
        for key in del_keys:
            del meta[key]
        with open(filename, mode='wb') as fobj:
            fobj.write(response.body)

        for row in rows.import_from_pdf(io.BytesIO(response.body)):
            row = row._asdict()
            row['local_da_coleta'] = clean(row['local_da_coleta'])
            row['ponto_codigo'] = clean(row['ponto_codigo'])
            row['costa_ponto'] = extrai_costa(row['ponto_codigo'])
            row.update(meta)
            yield row
