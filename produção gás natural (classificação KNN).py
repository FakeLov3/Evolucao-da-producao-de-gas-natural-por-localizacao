import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from yellowbrick.classifier import ConfusionMatrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

'''Aqui vamos usar um método de classificação usando o KNN, para saber como o computador irá dizer qual grupo pertence localização das plataformas de gás natural. '''

#Carregamento da base de dados
dados = pd.read_csv('Anuário Estatístico 2019 - Evolução da produção de gás natural, por localização.csv', sep = ';', decimal = ',')

#Criação de uma variável com variáveis independentes(x)
previsores = dados.iloc[:, [0, 3]].values

#Criação de uma variável com variável de resposta(y)
classe = dados.iloc[:, 1].values

#Aqui iremos transformar as colunas categóricas em colunas numéricas
labelencoder = LabelEncoder()
previsores[:, 0] = labelencoder.fit_transform(previsores[:, 0])

#Fazendo a padronização dos atributos previsores
scaler = StandardScaler()
previsores = scaler.fit_transform(previsores)

#Aqui hávera a divisão dos dados para treinamento e teste passando como parâmetros(variavel independente, variável resposta, a amostra de teste[0 até 1] e divisao da base de dados igual)
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(previsores, classe, test_size = 0.3, random_state = 0)

#Faz a previsão do algoritmo knn usando a base de treinamento
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(X_treinamento, y_treinamento)

#Faz a previsão do algoritmo knn usando a base de teste
previsoes = knn.predict(X_teste)

#Cria uma matriz de confusão nessa variável
confusao = confusion_matrix(y_teste, previsoes)

#Cria variáveis com a taxa de acerto e erro
taxa_acerto = accuracy_score(y_teste, previsoes)
taxa_erro = 1 - taxa_acerto

#Aqui irá gerá a figura da matriz de confusão (executar os 4 comandos simultaneamente)
v = ConfusionMatrix(knn)
v.fit(X_treinamento, y_treinamento)
v.score(X_teste, y_teste)
v.poof()

''' A taxa de acerto do modelo foi de 91,7%, aproximadamente, com 30% dos dados para teste e knn = 5.'''
