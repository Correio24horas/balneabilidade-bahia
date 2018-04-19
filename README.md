# Praias Bahia

Programa que baixa todos os relatórios de balneabilidade do INEMA (em PDF),
converte um por um e extrai os dados completos em uma planilha.


## Dados

[**Acesse diretamente os dados já
extraídos**](https://drive.google.com/open?id=1muf_9bG9xqwJPIz_g4Bui2ZCTsmOA8EZ).


## Rodando

Esse script depende de Python 3.6 e de algumas bibliotecas. Instale-as
executando:

```bash
pip install -r requirements.txt
```

Daí, basta executar (testado em sistema GNU/Linux - talvez precise de alteração
em Mac OS X e Windows):

```bash
./run.sh
```

Os arquivos `boletins.csv` e `balneabilidade.csv` serão criados (além de
versões deles em `xls` dos mesmos). Divirta-se! :)
