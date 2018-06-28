#!/bin/bash

set -e

run_spider() {
	scrapy runspider "$1" \
		-s HTTPCACHE_ENABLED=True \
		-s HTTPCACHE_POLICY=scrapy.extensions.httpcache.RFC2616Policy \
		-s HTTPCACHE_STORAGE=scrapy.extensions.httpcache.FilesystemCacheStorage \
		--loglevel=INFO \
		-o "$2"
}

BOLETINS="data/output/boletins.csv"
BALNEABILIDADE="data/output/balneabilidade.csv"
DBNAME="data/output/balneabilidade-bahia.sqlite"

rm -rf data/output && mkdir -p data/output
time run_spider lista_boletins.py "$BOLETINS" && xz -z "$BOLETINS"
time run_spider extrai_boletins.py "$BALNEABILIDADE" && xz "$BALNEABILIDADE"
time rows csv2sqlite "$BOLETINS.xz" "$BALNEABILIDADE.xz" "$DBNAME"
