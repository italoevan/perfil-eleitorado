import pandas as pd
from dash import Input, Output, State, html, dash_table

def clean_column_values(df, col_name):
    """Função auxiliar para normalizar valores de colunas"""
    df[col_name] = df[col_name].str.strip().str.upper()
    return df

def register_distribuicao_analfabetos_callback(app):
    @app.callback(
        Output('municipio-list', 'children'),
        Input('search-button', 'n_clicks'),
        State('municipio-search', 'value')
    )
    def update_municipio_list(n_clicks, search_value):
        # Ler os dados com a codificação correta
        df_rj = pd.read_csv('dados/perfil_eleitorado_2024.csv', sep=';', encoding='ISO-8859-1')
        
        # Filtrar os dados apenas para o Rio de Janeiro
        df_rj = df_rj[df_rj['SG_UF'] == 'RJ']
        
        # Limpar e normalizar o nome dos municípios
        df_rj = clean_column_values(df_rj, 'NM_MUNICIPIO')

        # Filtrar os analfabetos
        df_analfabetos = df_rj[df_rj['DS_GRAU_ESCOLARIDADE'].str.contains('ANALFABETO', na=False)]

        # Calcular a quantidade de analfabetos por município
        df_analfabetos['QT_ELEITORES_PERFIL'] = pd.to_numeric(df_analfabetos['QT_ELEITORES_PERFIL'], errors='coerce')
        df_municipios = df_analfabetos.groupby('NM_MUNICIPIO')['QT_ELEITORES_PERFIL'].sum().reset_index()
        df_municipios.columns = ['Município', 'Quantidade de Analfabetos']

        # Aplicar a pesquisa de município
        if search_value:
            search_value = search_value.strip().upper()
            df_municipios = df_municipios[df_municipios['Município'].str.contains(search_value, na=False)]

        # Verificar se o DataFrame está vazio após a pesquisa
        if df_municipios.empty:
            return [html.P('Nenhum município encontrado.', style={'color': 'red', 'font-style': 'italic'})]

        # Ordenar os dados
        df_municipios = df_municipios.sort_values(by='Quantidade de Analfabetos', ascending=False)

        # Criar a tabela para exibição
        return dash_table.DataTable(
            data=df_municipios.to_dict('records'),
            columns=[
                {'name': 'Município', 'id': 'Município'},
                {'name': 'Quantidade de Analfabetos', 'id': 'Quantidade de Analfabetos', 'type': 'numeric'}
            ],
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={
                'backgroundColor': '#f2f2f2',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_table={'overflowX': 'auto'},
            page_size=10,
            sort_action='native',
            filter_action='native',
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9'
                }
            ]
        )
