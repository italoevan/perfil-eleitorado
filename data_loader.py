import pandas as pd

def load_data(arquivo_csv):
    df = pd.read_csv(arquivo_csv, delimiter=';', encoding='ISO-8859-1')

    # Limpar os nomes das colunas
    df.columns = df.columns.str.strip().str.replace('"', '')

    # Definir as colunas relevantes
    colunas_relevantes = [
        'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'SG_UF', 'CD_MUNICIPIO',
        'NM_MUNICIPIO', 'NR_ZONA', 'DS_GRAU_ESCOLARIDADE', 'DS_FAIXA_ETARIA'
    ]

    # Filtrar as colunas relevantes
    df = df[colunas_relevantes]

    # Filtrar apenas os dados do Rio de Janeiro
    df_rj = df[df['SG_UF'] == 'RJ'].copy()  # Use .copy() para evitar o SettingWithCopyWarning

    # Normalizar colunas necessárias
    df_rj.loc[:, 'DS_GRAU_ESCOLARIDADE'] = df_rj['DS_GRAU_ESCOLARIDADE'].str.strip().str.upper()
    df_rj.loc[:, 'DS_FAIXA_ETARIA'] = df_rj['DS_FAIXA_ETARIA'].str.strip().str.upper()

    return df_rj
