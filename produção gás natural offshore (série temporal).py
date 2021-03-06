import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima_model import ARIMA

''' Aqui faremos um histograma com a produção total de gás natural (onshore/offshore) no Brasil
    entre 2009 a 2018, e a sua previsão para 2019 e 2020.'''

#Carregamento da base de dados
dados = pd.read_csv('Anuário Estatístico 2019 - Evolução da produção de gás natural, por localização.csv', sep = ';', decimal = ',') 

#Conversão de milhôes m³ para m³
dados['Produção de gás natural (milhões m3)'] = dados['Produção de gás natural (milhões m3)'].mul(1000000)

#Renomeação da coluna
dados = dados.rename(columns = {'Produção de gás natural (milhões m3)' : 'Produção de gás natural (m³)'})

#Soma de toda a produção de cada ano
dados = dados.groupby(['Ano'])['Produção de gás natural (m³)'].sum()

#Reset do index do dataframe
dados = dados.reset_index()

#Vamos exportar esse novo dataframe para transforma-lo em arquivo CSV
dados.to_csv(r'D:\Meus Documentos\Desktop\Projetos Cientista de Dados\G2.08 - Evolução da produção de gás natural, por localização (terra e mar) – 2009 a 2018\Produção_gas_natural_total_serie_temporal.csv')

#Novo banco de dados com os estados produtores de gás natural onshore de 2009 a 2018
dados2 = pd.read_csv('Produção_gas_natural_total_serie_temporal.csv')

print(dados2.dtypes)

#Precisamos transformar o ano do tipo 'object' para o ano tipo data para ser aplicada na série temporal
dateparse = lambda dates:pd.datetime.strptime(dates, '%Y')
dados2 = pd.read_csv('Produção_gas_natural_total_serie_temporal.csv', parse_dates = ['Ano'], index_col = 'Ano', date_parser = dateparse)

#Remover a primeira coluna do dataframe
dados2 = dados2.drop('Unnamed: 0', axis = 1)

#cria o gráfico da série temporal original
plt.plot(dados2)

#cria um modelo para determinar o ARIMA
modelo_auto = auto_arima(dados2, m = 2, seasonal = False, trace = True)

#detalha todos os parâmetros do ARIMA
modelo_auto.summary()

#Fazer uma previsao com auto ARIMA com o número de previsões
proximo_ano = modelo_auto.predict(n_periods = 2)

'''Criar uma variavel com o parâmetros do ARIMA adquiridos com o auto arima, passando o banco de dados e ajustando no modelo
   Lembrando que o auto ARIMA determina varios parâmetros, e maquina escolhe o mais apropriado para ela, entretanto é importante
   testar outros parâmetros para ver como se sai o gráfico da série temporal.'''
   
modelo = ARIMA(dados2, order = [1, 1, 1])
modelo_treinado = modelo.fit()

#visualizar os detalhes/parâmetros do modelo
modelo_treinado.summary()

#Cria uma previsão da série temporal, passando quantas previsoes que queremos adiante (steps)
previsoes = modelo_treinado.forecast(steps = 2)[0]

#Gera um gráfico com as previsoes, comparando com a série original
eixo = dados2.plot()
modelo_treinado.plot_predict('2009-01-01', '2020-01-01', ax = eixo, plot_insample = False)

''' Obs¹: tanto a váriavel 'proximo_ano' e 'previsoes' irao fazer as previsoes posteriores
    e poderão dar valores diferentes, em virtude do AUTO ARIMA já utilizar algumas configurações
    extras para utilizar no seu modelo.
    
    Obs²: no gráfico há a linha do gráfico real e da previsão da máquina, e como a base de dados
    tem poucos dados, é normal as linhas ficarem um pouco distantes.'''
