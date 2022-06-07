from asyncio.windows_events import NULL
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("display.precision", 2)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

# address = pd.read_csv("enderecos.csv")
# address_sp = address.query("sigla_uf == 'SP'")
# address_sp.to_csv('address_sp.csv', index=False, na_rep='Unknown')

original_data = pd.read_csv("data.csv", sep=',', encoding='latin-1')
address_sp = pd.read_csv("address_sp.csv")
ibge = pd.read_csv("ibge.csv", sep=";", encoding="UTF-8", thousands=".", decimal=",")
setor_censo = gpd.read_file('/content/drive/MyDrive/imersao_dados_5/35SEE250GC_SIR.shp')

setor_censo_sp = setor_censo[setor_censo.NM_MUNICIP == "SÃO PAULO"]
setor_censo = None

ibge.dropna(how = "all", axis=1, inplace=True)


df = original_data["Valor"].str.split(expand=True)
original_data[["Moeda", "Valor_anuncio", "Tipo_anuncio"]] = df
data = original_data[original_data["Tipo_anuncio"].isnull()]
data["Valor_anuncio"] = data["Valor_anuncio"].str.replace(
    ".", "").astype(float)
data["price_per_meter"] = data["Valor_anuncio"]/data["Metragem"]

data_district = data.groupby("Bairro").sum()
data_district["price_per_meter_district"] = data_district["Valor_anuncio"]/data_district["Metragem"]

top_districts = data["Bairro"].value_counts()[:10].index
data_district.reset_index(inplace=True)


address_sp["rua"] = address_sp["tipo_logr"] + " " + address_sp["logr_nome"]
address_sp["rua"] = address_sp["rua"].str.lower().str.strip()

data["apenas_rua"] = data["Rua"].str.extract(r'(^[\w ]+)')
data["apenas_rua"] = data["apenas_rua"].str.lower().str.strip()


dados_geo = pd.merge(left = data, right = address_sp[["rua", "cep", "latitude", "longitude"]], how = "left", left_on = "apenas_rua", right_on = "rua").drop_duplicates(subset=data.columns).query("cep > 0")

dados_geo["Point"] = ""
for i in dados_geo.index:
    dados_geo["Point"][i] = Point(dados_geo["longitude"][i], dados_geo["latitude"][i])

# dados_geo['setor_censo'] = dados_geo["Point"][:10].map(lambda x: setor_censo_sp.loc[setor_censo_sp.contains(x), 'CD_GEOCODI'].values).str[0]
dados_geo['setor_censo'] = dados_geo["Point"].map(lambda x: setor_censo_sp.loc[setor_censo_sp.contains(x), 'CD_GEOCODI'].values).str[0]

dados_vendas_censo = pd.merge(left = dados_geo, right = ibge, how = "left", left_on = "setor_censo", right_on = "Cod_setor")
dados_vendas_censo

dados_vendas_censo = pd.read_csv("dados_vendas_censo.csv")

plt.figure(figsize=(10, 10))
sns.scatterplot(data = dados_vendas_censo, x="V005", y="Valor_m2")

# Desafios desta aula
# 1 - Realizar uma análise dos dados do IBGE por mapa, analisando a distribuição de renda.
# 2 - Repassar a aula para entender melhor o que foi realizado.
# 3 - Aprofundar a análise entre dados de vendas e renda.
# 4 - Realizar a análise exploratória e encontrar variáveis relevantes para solução do problema.
