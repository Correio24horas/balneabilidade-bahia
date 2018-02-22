#!/bin/bash

function run_spider() {
	scrapy runspider "$1" \
		-s HTTPCACHE_ENABLED=True \
		-s HTTPCACHE_POLICY=scrapy.extensions.httpcache.RFC2616Policy \
		-s HTTPCACHE_STORAGE=scrapy.extensions.httpcache.FilesystemCacheStorage \
		--loglevel=INFO \
		-o "$2"
}

rm -rf output && mkdir output
time run_spider lista_boletins.py output/boletins.csv
time run_spider extrai_boletins.py output/balneabilidade.csv
rows convert output/boletins.{csv,xls}
rows convert output/balneabilidade.{csv,xls}
