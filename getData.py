# https://finance.yahoo.com/quote/PETR4.SA?p=PETR4.SA&.tsrc=fin-srch
# https://finance.yahoo.com/
# https://finance.yahoo.com/quote/EGIE3.SA?p=EGIE3.SA&.tsrc=fin-srch
# To search for a specific stock, use this template: https://finance.yahoo.com/quote/$stockname.SA?p=$stockname.SA&.tsrc=fin-srch
# Financial data: https://finance.yahoo.com/quote/HGRE11.SA/financials?p=HGRE11.SA

import bs4
import requests
import pandas as pd

# codigo_acoes = input("Digite os códigos das ações, separados por vírgulas: ")
# lista_acoes = codigo_acoes.split(',')
    

def get_via_file():
    cells = []
    planilha = pd.read_excel('acoes.xlsx')
    acoes = planilha['EMPRESA']
# print(acoes[0]) # acoes é interpretada como uma lista, cujos índices representam as linhas da coluna selecionada

    for each_item in acoes:
        res = requests.get('https://finance.yahoo.com/quote/' + each_item  + '.SA/key-statistics?p=' + each_item + '.SA')
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.content, 'lxml')
        price = soup.select('.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)')
        enterprise_value = soup.select('.Fw\(500\).Ta\(end\).Pstart\(10px\).Miw\(60px\)')
        info = []
        info.append(each_item)
        info.append(price[0].string)
        info.append(enterprise_value[0].string)
        cells.append(info)



    headers = ['EMPRESA','PREÇO','EV']

    tabela = pd.DataFrame(cells, columns = headers)

    tabela.to_excel("acoes_info.xlsx", index=False)

    planilha_2 = pd.read_excel('acoes_info.xlsx')

    planilha_3 = pd.merge(planilha, planilha_2, how='left',on='EMPRESA')

    planilha_3.to_excel('Planilha_Acoes.xlsx', index=False)



def get_via_input():
    cells = []
    codigos = input("Digite os códigos das ações, separando-os com vírgulas e sem espaço, ex: \nWEGE3,HGRE11\n")
    lista_acoes = codigos.split(",")
    print(lista_acoes)
    for each_item in lista_acoes:
        res = requests.get('https://finance.yahoo.com/quote/' + each_item  + '.SA/key-statistics?p=' + each_item + '.SA')
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.content, 'lxml')
        price = soup.select('.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)')
        enterprise_value = soup.select('.Fw\(500\).Ta\(end\).Pstart\(10px\).Miw\(60px\)')
        info = []
        info.append(each_item)
        info.append(price[0].string)
        info.append(enterprise_value[0].string)
        cells.append(info)
    
    headers = ['EMPRESA','PREÇO','EV']
    tabela = pd.DataFrame(cells, columns = headers)
    print(tabela)

def main():
    method = input("Como você deseja inserir as ações: \n1-Por arquivo\n2-Digitando os códigos\n3-Sair\n> ")
    if (int(method) == 1):
        get_via_file()
    elif (int(method) == 2):
        get_via_input()
    else:
        print("Goodbye")



    
main()
