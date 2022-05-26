import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("display.precision", 2)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

# sns.set()

original_data = pd.read_csv("data.csv", sep=',', encoding='latin-1')
# csvfile = pd.read_csv("https://gist.githubusercontent.com/tgcsantos/3bdb29eba6ce391e90df2b72205ba891/raw/22fa920e80c9fa209a9fccc8b52d74cc95d1599b/dados_imoveis.csv")

df = original_data["Valor"].str.split(expand=True)
original_data[["Moeda", "Valor_anuncio", "Tipo_anuncio"]] = df
data = original_data[original_data["Tipo_anuncio"].isnull()]
data["Valor_anuncio"] = data["Valor_anuncio"].str.replace(".", "").astype(float)


data["price_per_meter"] = data["Valor_anuncio"]/data["Metragem"]

data_district = data.groupby("Bairro").sum()
data_district["price_per_meter_district"] = data_district["Valor_anuncio"]/data_district["Metragem"]

top_districts = data["Bairro"].value_counts()[:10].index
data_district.reset_index(inplace = True)

data_district.query("Bairro in @top_districts")

plt.figure(figsize=(10, 8))
ax = sns.barplot(x="Bairro", y="price_per_meter_district", data=data_district.query("Bairro in @top_districts"))
ax.tick_params(axis='x', rotation=45)

plt.figure(figsize=(10, 8))
ax = sns.boxplot(data = data.query("Bairro in @top_districts"), x="Bairro", y="price_per_meter")
ax.tick_params(axis='x', rotation=45)
plt.show()

plt.figure(figsize=(10, 8))
ax = sns.boxplot(data = data.query("Bairro in @top_districts & Metragem < 30000"), x="Bairro", y="Metragem")
ax.tick_params(axis='x', rotation=45)
plt.show()

ibge = pd.read_csv("ibge.csv", sep=";")


# Desafio Aula 3
# Tentar vincular dados do IBGE com os dados de imóveis.
# Tratar os outliers e comparar com os resultados.
# Agrupar por mais de uma categoria e realizar as análises.
# Organize o colab para deixar com cara de projeto.
