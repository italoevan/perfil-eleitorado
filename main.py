import pandas as pd # Para processar a planilha


arquivo_excel = 'eleitores2024.csv' # Aqui a gente ta carregando a planilha, caso de erro podemos usar uma LIB de csv
df = pd.read_excel(arquivo_excel)


print(df.head()) # vamos remover essa linha depois, ela serve para printar no console o header da planilha (as primeiras linhas e colunas)


#Sobre os filtros acredito que temos que entender primeiro o escopo, depois só se basear nele.
#Uma ideia interessante seria se basear nos eleitores abaixo de 20 anos que não tem ensino medio ou que ainda estão concluindo.
