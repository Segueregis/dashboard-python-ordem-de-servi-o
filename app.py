import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import calendar

app = dash.Dash(__name__)



df = pd.read_excel("UT-020-PROJETOS.xlsx")
df = df.rename(columns={'Status': 'Status', 'Quantidade': 'Quantidade', 'Setor': 'Setor', 'Equipe': 'Equipe',
                        'Data de Inicio': 'DataInicio'})

# Adicione os prints para verificar os tipos de dados e valores ausentes
print(df.dtypes)
print(df.isnull().sum())

fig_bar = px.bar(df, x="Status", y="Quantidade", color="Setor", barmode="group")
fig_pie = px.pie(df, names='Equipe', values='Quantidade', title='Distribuição por Equipe')


def create_default_quantidade_figure():
    return px.line(df, x="DataInicio", y="Quantidade", color="Setor", title='Tendência Semanal de Ordens de Serviço')


def get_dropdown_options(column_name):
    options = list(df[column_name].unique())
    options.append(f"Lista por {column_name}")
    return options


opcoes_setor = get_dropdown_options('Setor')
opcoes_equipe = get_dropdown_options('Equipe')

meses_referencia = pd.DataFrame(index=range(1, 13), columns=['Mes'])
meses_referencia['Mes'] = meses_referencia.index.map(lambda x: calendar.month_abbr[x])

app.layout = html.Div([
    html.H1('Ordem de Serviço - UT - 020 Projetos', style={'color': 'orange', 'fontSize': 40}),

    html.H2('Gráfico por Setores '),
    dcc.Dropdown(options=opcoes_setor, value='Lista por Setor', id='lista_Setor_bar'),
    dcc.Graph(id='grafico_por_setor_bar', figure=fig_bar),

    html.H2('Gráfico por Equipe '),
    dcc.Dropdown(options=opcoes_equipe, value='Lista por Equipe', id='lista_Equipe_pie'),
    dcc.Graph(id='grafico_por_equipe_pie', figure=fig_pie),
])

@app.callback(
    Output('grafico_por_setor_bar', 'figure'),
    Input('lista_Setor_bar', 'value')
)
def update_output_bar(valor):
    if valor == 'Lista por Setor':
        fig = px.bar(df, x="Status", y="Quantidade", color="Setor", barmode="group")
    else:
        tabela_filtrada = df[df['Setor'] == valor].groupby(['Status', 'Setor'], as_index=False).sum()
        fig = px.bar(tabela_filtrada, x="Status", y="Quantidade", color="Setor", barmode="group")
    return fig

@app.callback(
    Output('grafico_por_equipe_pie', 'figure'),
    Input('lista_Equipe_pie', 'value')
)
def update_output_pie(valor):
    if valor == 'Lista por Equipe':
        fig = px.pie(df, names='Equipe', values='Quantidade', title='Distribuição por Equipe')
    else:
        tabela_filtrada = df[df['Equipe'] == valor].groupby(['Equipe'], as_index=False).sum()
        fig = px.pie(tabela_filtrada, names='Equipe', values='Quantidade', title=f'Distribuição por Equipe - {valor}')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
