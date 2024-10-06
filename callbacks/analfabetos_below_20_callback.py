from dash import Input, Output, html
import plotly.express as px
import pandas as pd
from data_loader import load_data

# Carregar os dados
df_rj_2024 = load_data('dados/perfil_eleitorado_2024.csv')

def filter_by_rj(df):
    """Função auxiliar para filtrar dados do Rio de Janeiro"""
    return df[df['SG_UF'] == 'RJ'].copy()  # Use .copy() para evitar SettingWithCopyWarning

def clean_column_values(df, col_name):
    """Função auxiliar para normalizar valores de colunas"""
    df[col_name] = df[col_name].str.strip().str.upper()
    return df

def register_analfabetos_below_20_callback(app):
    @app.callback(
        Output('analfabetos-below-20-grafico', 'figure'),
        Output('variacao-percentual-below-20-text', 'children'),
        Input('analfabetos-below-20-grafico', 'id')  
    )
    def update_analfabetos_below_20_grafico(_):
        try:
            # Criar uma cópia do DataFrame original para evitar SettingWithCopyWarning
            df_rj_2024_filtered = df_rj_2024.copy()

            # Limpar e normalizar os dados
            df_rj_2024_filtered = clean_column_values(df_rj_2024_filtered, 'DS_GRAU_ESCOLARIDADE')
            df_rj_2024_filtered = clean_column_values(df_rj_2024_filtered, 'DS_FAIXA_ETARIA')
            
            # Filtrar os jovens de 20 anos ou menos
            jovens_below_20 = filter_by_rj(df_rj_2024_filtered)[
                df_rj_2024_filtered['DS_FAIXA_ETARIA'].isin(['16 ANOS', '17 ANOS', '18 ANOS', '19 ANOS', '20 ANOS'])
            ]
            total_jovens_below_20 = jovens_below_20.shape[0]

            # Filtrar os analfabetos de 20 anos ou menos
            analfabetos_below_20 = jovens_below_20[
                jovens_below_20['DS_GRAU_ESCOLARIDADE'] == 'ANALFABETO'
            ]
            total_analfabetos_below_20 = analfabetos_below_20.shape[0]

            # Verifique se os totais são válidos antes de criar o gráfico
            if total_jovens_below_20 == 0:
                return {}, "Não há dados suficientes para calcular a variação percentual."
            
            # Criar o gráfico de barras
            fig = px.bar(
                x=['Jovens de 20 Anos ou Menos', 'Analfabetos de 20 Anos ou Menos'],
                y=[total_jovens_below_20, total_analfabetos_below_20],
                title="Total de Jovens de 20 Anos ou Menos e Analfabetos no RJ (2024)",
                labels={'x': 'Categoria', 'y': 'Número de Indivíduos'},
            )

            # Calcular a porcentagem de analfabetos de 20 anos ou menos
            porcentagem_analfabetos = (total_analfabetos_below_20 / total_jovens_below_20 * 100)
            texto_variacao = f"Analfabetos de 20 anos ou menos representam {porcentagem_analfabetos:.2f}% da quantidade total de jovens."

            return fig, texto_variacao

        except Exception as e:
            print(f"Erro no callback 'analfabetos_below_20': {e}")
            return {}, 'Erro ao calcular a variação percentual.'
