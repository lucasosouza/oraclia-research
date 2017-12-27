#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

def clean_stock_data(row):
	tipreg = row[:2]
	if tipreg == "02":
		nomerc = row[72:87]
		if nomerc[:5] == "VISTA":
			voltot = int(row[193:210]) / 100
			if voltot > 1000000:
				codneg = row[57:69]
				preult = float(row[134:145]) / 100
				return codneg[:5], voltot, preult
	return None, None, None

def retrieve_and_save(data_file):
	stock_data = {}
	with open(data_file) as f:
		for row in f:
			symbol, volume, price = clean_stock_data(row)
			if symbol:
				stock_data[symbol] = {
					"volume": volume,
					"price": price
				}
	df = pd.DataFrame.from_dict(stock_data, orient="index")
	df.to_csv("bovespa_data_df.csv")

if __name__ == "__main__":
	retrieve_and_save("bovespa_data.txt")


# 0202LOTE PADRAO                   PETROBRAS   ON        .PETR3       010VISTA          0000000000110100000001150000000011010000000113500000001139+005750000000113500000001139173320000000142011000000001612035260000000000000000000000MOEDA CORRENTE 00000010000000000000BRPETRACNOR91830               0000000575                                            

### DESCRIÇÃO DOS CAMPOS DO ARQUIVO POSICIONADO
# Tipo de Registro 02 - Resumo diário de negociações por papel-mercado

# 01-02 # 02 # TIPREG: Tipo de registro (No caso: resumo diário de negociações por papel-mercado)
# 03-04 # 02 # CODBDI: Código BDI: usado para classificar papéis, ver tabela associada NE001
# 05-34 # LOTE PADRAO                    # DESBDI: Descrição do Código de BDI
# 34-46 # PETROBRAS    # NOMRES: Nome resumido da emissora do papel
# 47-56 # ON         # ESPECI: Especificação do Papel. Para Novo Mercado, nas posições 9 e 10 está indicado N1, N2 ou NM
# 57-57 # . # INDCAR: Indicador de caraterística do papel. Ver tabela associada PA020
# 58-69 # PETR3        # CODNEG: Código de Negociação
# 70-72 # 010 # TPMERC: Código do mercado em que papel está cadastrado. Ver tabela associada PA003
# 73-87 # VISTA           # NOMERC: Descrição do Tipo de Mercado
# 88-90 # 000 # PRAZOT: Prazo em dias do mercado a termo
# 91-101  # 00000001101 # PREABE: Preço de abertura do papel (preço do primeiro negócio efetuado)
# 102-112 # 00000001150 # PREMAX: Preço máximo no pregão
# 113-123 # 00000001101 # PREMIN: Preço mínimo no pregão
# 124-134 # 00000001135 # PREMED: Preço médio no pregão
# 135-145 # 00000001139 # PREULT: Preço do último negócio efetuado
# 146-146 # + # SINOSC: Sinal da oscilação do preço em relação ao pregão anterior
# 147-151 # 00575 # OSCILA: Oscilação do preço em relação ao pregão anterior
# 152-162 # 00000001135 # PREOFC: Preço da melhor oferta de compra
# 163-173 # 00000001139 # PREOFV: Preço da melhor oferta de venda
# 174-178 # 17332 # TOTNEG: Número de negócios efetuados no pregão corrente
# 179-193 # 000000014201100 # QUATOT: Quantidade total de títulos negociados
# 194-210 # 00000016120352600 # VOLTOT: Volume total de títulos negociados
# 211-221 # 00000000000 # PREEXE: Preço exercício para mercado opções ou valor do contrato para mercado termo secundário
# 222-229 # 00000000 # DATVEN: Data do vencimento para mercados de opções, termo secundário ou futuro. Formato AAAAMMDD
# 230-230 # 0 # INDOPC: Indicador correção de preços exercícios ou valores de contrato opções, secundário ou futuro.Ver PA004
# 231-245 # MOEDA CORRENTE # NOMIND: descrição do indicador de correção de preços de exercícios (descrito acima)
# 246-252 # 0000001 # FATCOT: Fator de cotação do papel. Ver EM021
# 253-265 # 0000000000000 # PTOEXE - Preço de exercício em pontos para opções referenciadas em dólar, etc. 
# 266-277 # BRPETRACNOR9 # CODISI: Código do papel no sistema ISIN
# 278-280 # 183 # DISMES: Número de distribuição do papel 
# 281-281 # 0 # ESTILO: Estilo adotado para o exercício de opções de compra/venda
# 282-296 #                 # NOMEST: Descrição do estilo
# 297-299 # 000 # ICOATV - Indicador de correção de preços de exercícios o valores de contrato futuro etc...
# 300-306 # 0000575 # OSCPRE - Oscilação do preço em relação ao pregão anterior
# 307-350 #                                              # RESERVA: Em branco



# que dados eu preciso da bovespa

# Processo para filtrar:
# Todos os papéis com registro 02 - ignorar o restante por agora - TIPREG == 02
# Todos os papéis do mercado a vista - NOMERC == VISTA
# Todos os papéis com volume de negociação superior a 1 milhão - VOLTOT >= 100000000
# Pegar o código de negociação 
# Pegar o preço do último negócio efetuado
# Pegar o volume
# Jogar em um dataframe 
# Analisar

