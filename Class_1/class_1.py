import pandas as pd


data = pd.read_csv("data.csv", sep=',', encoding='latin-1')
# csvfile = pd.read_csv("https://gist.githubusercontent.com/tgcsantos/3bdb29eba6ce391e90df2b72205ba891/raw/22fa920e80c9fa209a9fccc8b52d74cc95d1599b/dados_imoveis.csv")

data.head()
data.sample(10)

type(data)  # pandas.core.frame.DataFrame
type(data["Bairro"])  # pandas.core.series.Series

data.info()

data["Bairro"]
data.Bairro
data["Bairro"][6552]
# data[6552]

data.Metragem.mean()
data.Metragem.median()

data["Bairro"] == "Vila Mariana"
has_property_vila = data["Bairro"] == "Vila Mariana"

data[has_property_vila].mean()
data[has_property_vila]["Metragem"].mean()

data["Bairro"].value_counts()
number_properties_by_district = data["Bairro"].value_counts()
number_properties_by_district.plot.hist()
number_properties_by_district.head(10).plot.bar()

# getgroup
# groupby
# sort_values
# describe
# agg

# Exercises

# n1 Realizar a média da metragem para cada um dos bairros.
data.groupby(["Bairro"]).mean()
data.groupby(["Bairro"])["Metragem"].mean()

# n2 Duas formas de selecionar os dados por bairro (consultar os métodos na documentação do Pandas)
data.groupby(["Bairro"]).mean()

# n3 Explorar alguns gráficos na documentação e aplicar nas demais colunas do DF, assim como tentar colocar alguma conclusão

# n4 Pegar outras estatísticas dos dados (como média, mediana, mim, max). (Proposto pela Vivian)
data.min()
data.max()
data.median()
data.mean()
data.std()
data.quantile(q=0.25)
data.count()
data.value_counts()
data.describe()

# n5 Descobrir quais são os bairros que não tem nome de rua. (Proposto pela Vivian)
data['Rua'].isnull()
has_null = data['Rua'].isnull()
data[has_null]['Bairro']
