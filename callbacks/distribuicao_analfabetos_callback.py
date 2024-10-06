import pandas as pd
from dash import Input, Output, html, dcc

def clean_column_values(df, col_name):
    """Função auxiliar para normalizar valores de colunas"""
    df[col_name] = df[col_name].str.strip().str.upper()
    return df

def register_distribuicao_analfabetos_callback(app):
    @app.callback(
        Output('municipio-list', 'children'),
        Input('municipio-search', 'value')  # Valor do campo de pesquisa
    )
    def update_municipio_list(search_value):
        # Ler os dados com a codificação correta
        df_rj = pd.read_csv('dados/perfil_eleitorado_2024.csv', sep=';', encoding='ISO-8859-1')
        
        # Filtrar os dados apenas para o Rio de Janeiro
        df_rj = df_rj[df_rj['SG_UF'] == 'RJ']
        
        # Limpar e normalizar o nome dos municípios
        df_rj = clean_column_values(df_rj, 'NM_MUNICIPIO')

        # Filtrar os analfabetos
        df_analfabetos = df_rj[df_rj['DS_GRAU_ESCOLARIDADE'].str.contains('ANALFABETO', case=False, na=False)]

        # Calcular a quantidade de analfabetos por município
        df_analfabetos['QT_ELEITORES_PERFIL'] = pd.to_numeric(df_analfabetos['QT_ELEITORES_PERFIL'], errors='coerce')
        df_municipios = df_analfabetos.groupby('NM_MUNICIPIO')['QT_ELEITORES_PERFIL'].sum().reset_index()
        df_municipios.columns = ['Municipio', 'Quantidade_Analfabetos']

        # Aplicar a pesquisa de município
        if search_value:
            df_municipios = df_municipios[df_municipios['Municipio'].str.contains(search_value.upper(), case=False, na=False)]

        # Verificar se o DataFrame está vazio após a pesquisa
        if df_municipios.empty:
            return [html.P('Nenhum município encontrado.')]

        # Criar a lista de municípios para exibição
        municipio_list = [
            html.Li([
                html.Span(municipio['Municipio'], style={'font-weight': 'bold'}),
                html.Span(f" - {municipio['Quantidade_Analfabetos']} analfabetos", style={'margin-left': '10px'})
            ])
            for _, municipio in df_municipios.iterrows()
        ]

        return municipio_list