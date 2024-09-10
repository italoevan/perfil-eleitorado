import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo CSV
arquivo_csv = 'perfil_eleitorado_2024.csv'

# Tentar ler o arquivo com o delimitador correto
try:
    df = pd.read_csv(arquivo_csv, delimiter=';', encoding='ISO-8859-1')  # ou encoding='latin1'
except UnicodeDecodeError as e:
    print(f"Erro ao ler o arquivo CSV: {e}")

# Verificar os nomes das colunas
print("Colunas disponíveis:")
print(df.columns)

# Limpar os nomes das colunas, removendo aspas e espaços extras
df.columns = df.columns.str.strip().str.replace('"', '')

# Verificar os nomes das colunas após limpeza
print("Colunas após limpeza:")
print(df.columns)

# Ajustar a lista de colunas conforme os nomes reais
colunas_relevantes = ['DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'SG_UF', 'CD_MUNICIPIO', 'NM_MUNICIPIO', 'NR_ZONA', 'CD_GENERO', 'DS_GENERO', 'CD_ESTADO_CIVIL', 'DS_ESTADO_CIVIL', 'CD_FAIXA_ETARIA', 'DS_FAIXA_ETARIA', 'CD_GRAU_ESCOLARIDADE', 'DS_GRAU_ESCOLARIDADE', 'CD_RACA_COR', 'DS_RACA_COR', 'CD_IDENTIDADE_GENERO', 'DS_IDENTIDADE_GENERO']

# Filtrar apenas as colunas relevantes se elas existirem no DataFrame
colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
df = df[colunas_existentes]

# Filtrar dados apenas para o Rio de Janeiro (RJ)
df_rj = df[df['SG_UF'] == 'RJ']

# Limpar e preparar dados
df_rj['DT_GERACAO'] = pd.to_datetime(df_rj['DT_GERACAO'], format='%d/%m/%Y')
df_rj['HH_GERACAO'] = pd.to_datetime(df_rj['HH_GERACAO'], format='%H:%M:%S').dt.time

# Insight 1: Distribuição de Faixa Etária dos Eleitores
faixa_etaria_counts = df_rj['DS_FAIXA_ETARIA'].value_counts()
plt.figure(figsize=(10, 6))
bars = faixa_etaria_counts.plot(kind='bar', color='skyblue')
plt.title('Distribuição de Faixa Etária dos Eleitores no Rio de Janeiro')
plt.xlabel('Faixa Etária')
plt.ylabel('Número de Eleitores')
plt.xticks(rotation=45)

# Adicionar número exato dentro de cada caixa
for bar in bars.patches:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height):,}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('faixa_etaria_rj.png')
plt.show()

# Insight 2: Distribuição do Nível de Escolaridade
nivel_escolaridade_counts = df_rj['DS_GRAU_ESCOLARIDADE'].value_counts()
plt.figure(figsize=(12, 8))
bars = nivel_escolaridade_counts.plot(kind='bar', color='lightgreen')
plt.title('Distribuição do Nível de Escolaridade dos Eleitores no Rio de Janeiro')
plt.xlabel('Nível de Escolaridade')
plt.ylabel('Número de Eleitores')
plt.xticks(rotation=45)

# Adicionar número exato dentro de cada caixa
for bar in bars.patches:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height):,}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('nivel_escolaridade_rj.png')
plt.show()

# Insight 3: Número de Eleitores Abaixo de 20 Anos Sem Ensino Médio
filtro_abaixo_20_anos_rj = df_rj[(df_rj['DS_FAIXA_ETARIA'].str.contains('a 19 anos|16 anos|17 anos')) & (~df_rj['DS_GRAU_ESCOLARIDADE'].str.contains('ENSINO MÉDIO'))]
numero_elet = len(filtro_abaixo_20_anos_rj)
plt.figure(figsize=(6, 6))
sizes = [numero_elet, len(df_rj) - numero_elet]
labels = ['Abaixo de 20 Anos Sem Ensino Médio', 'Outros']
plt.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%\n({int(p/100*sum(sizes)):,})', colors=['salmon', 'lightgrey'])
plt.title('Proporção de Eleitores Abaixo de 20 Anos Sem Ensino Médio no Rio de Janeiro')
plt.savefig('abaixo_20_sem_ensino_medio_rj.png')
plt.show()
