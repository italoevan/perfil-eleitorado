import pandas as pd
import plotly.express as px
from dash import Input, Output

def register_distribuicao_analfabetos_callback(app):
    @app.callback(
        Output('municipio-analfabetos-grafico', 'figure'),
        Input('tabs', 'value')  # Aciona o callback quando a aba é alterada
    )
    def update_map(selected_tab):
        # Verifica se a aba ativa é a de distribuição de analfabetos
        if selected_tab != 'tab-distribuicao-analfabetos':
            return px.choropleth(title='')

        # Ler os dados com a codificação correta
        df_rj = pd.read_csv('dados/perfil_eleitorado_2024.csv', sep=';', encoding='ISO-8859-1')
        
        # Filtrar os dados apenas para o Rio de Janeiro
        df_rj = df_rj[df_rj['SG_UF'] == 'RJ']

        # Calcular a quantidade de analfabetos por município
        df_rj['QT_ELEITORES_PERFIL'] = pd.to_numeric(df_rj['QT_ELEITORES_PERFIL'], errors='coerce')
        df_municipios = df_rj.groupby('NM_MUNICIPIO')['QT_ELEITORES_PERFIL'].sum().reset_index()
        df_municipios.columns = ['Municipio', 'Quantidade_Analfabetos']

        # Verificar se o DataFrame está vazio após o agrupamento
        if df_municipios.empty:
            return px.choropleth(title='Nenhum dado encontrado')
        
        geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-33-mun.json'
        
        # Criar um gráfico de mapa
        fig = px.choropleth(
                
                df_municipios,
                geojson=geojson_url,
                locations='Municipio',
                featureidkey='properties.name',  # Nome do município no GeoJSON
                color='Quantidade_Analfabetos',
                color_continuous_scale='Viridis',
                labels={'Quantidade_Analfabetos': 'Analfabetos'},
                title='Distribuição de Analfabetos no Estado do Rio de Janeiro'
            )

        fig.update_geos(fitbounds="locations", visible=False)

        return fig
