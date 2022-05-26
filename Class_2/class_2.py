import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("display.precision", 2)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

# sns.set()

original_data = pd.read_csv("data.csv", sep=',', encoding='latin-1')
# csvfile = pd.read_csv("https://gist.githubusercontent.com/tgcsantos/3bdb29eba6ce391e90df2b72205ba891/raw/22fa920e80c9fa209a9fccc8b52d74cc95d1599b/dados_imoveis.csv")

original_data.info()

original_data["Valor"][0].split()
original_data["Valor"].str.split()
df = original_data["Valor"].str.split(expand=True)
df[0].unique()
df[2].unique()

original_data[["Moeda", "Valor_anuncio", "Tipo_anuncio"]] = df
original_data.head()

original_data["Tipo_anuncio"].isnull()

data = original_data[original_data["Tipo_anuncio"].isnull()]
data["Tipo_anuncio"].unique()

data["Valor_anuncio"] = data["Valor_anuncio"].str.replace(
    ".", "").astype(float)

data.describe()
data.describe(include="all")
data["Valor_anuncio"].plot.hist(bins=50)

plt.figure(figsize=(10, 8))
ax = sns.histplot(data=data, x="Valor_anuncio", kde=True)
ax.set_title("Value Histogram")
plt.xlim((-50, 10000000))
plt.show()


# Challenges
# 1- Deixar o gráfico do histograma de valores legível (alterar labels, cores, título, escala)
# 2- Preço do metro quadrado por bairro e plotar em um gráfico ideal
data["price_per_meter"] = data["Valor_anuncio"]/data["Metragem"]
data[["Bairro", "price_per_meter"]].groupby("Bairro").describe()
data[["Bairro", "price_per_meter"]].groupby("Bairro").mean().sort_values("price_per_meter").plot.bar()
# 3- Explorar as bibliotecas de visualizações e colocar as suas conclusão
# 4- Pesquisar um visualização para analisar os quartis, mediana e outliers
data[["Bairro", "price_per_meter"]].groupby("Bairro").mean().sort_values("price_per_meter").boxplot()

data.sort_values("price_per_meter")
sns.boxplot(x="price_per_meter", y="Bairro", data=data.sort_values("price_per_meter"),
            whis=[0, 100], width=.6, palette="vlag")