# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

df = pd.read_csv("../Daten/swissvotes-dataset.csv", delimiter=";", na_values=".")
# Exclude data from votes with missing values (very first and of the last)
df = df.iloc[1:-12, :]
# Extract some data rows for comparison and verification
volk = df["volk"].iloc[:]
stand = df["stand"].iloc[:]
kt_ja = df["kt-ja"].iloc[:]
kt_nein = df["kt-nein"].iloc[:]
ktjaproz = df["ktjaproz"].iloc[:]

c_ja = df.iloc[:, df.columns.str.endswith("-ja")]
c_ja = c_ja.drop(columns=["inserate-ja", "kt-ja"])
c_ja.columns = c_ja.columns.str.replace("-ja", "")
c_nein = df.iloc[:, df.columns.str.endswith("-nein")]
c_nein = c_nein.drop(columns=["inserate-nein", "kt-nein"])
c_nein.columns = c_nein.columns.str.replace("-nein", "")
c_gultig = df.iloc[:, df.columns.str.endswith("-gultig")]
c_gultig.columns = c_gultig.columns.str.replace("-gultig", "")

# Do some sanity checks on the data
staende = kt_ja + kt_nein
invalid_results = (staende > 23).sum() + (staende < 22).sum()
print("Number of invalid staende results: {}".format(invalid_results))
print("Number of times the popular count and staende disagree: {}".format((volk != stand).sum()))


# %%
#df = df.set_index('anr').transpose()
#df_results = df[df.index.str.endswith("-japroz")]
number_cantons = c_ja.count(axis=1)
weights = c_ja.loc[1].copy()
weights[:] = 1.0
weights.loc[['ar','ai','ow','nw','bl','bs']] = 0.5

cantonal_data = pd.concat([c_ja, c_nein, c_gultig, c_ja/c_gultig], keys=["ja", "nein", "gultig", "japroz"])

# %%
cantons_yes = (cantonal_data.loc["japroz"] > 50.0).sum() > number_cantons
cantons_yes = cantons_yes.reset_index(drop=True)
stand = stand.reset_index(drop=True)
disagreements = (cantons_yes == (stand > 0.4)).sum()
print("Number of times the popular count and staende disagree: {}".format(disagreements))


# %%
reference_decision = (kt_ja > (number_cantons-3.0)/2)

results_b_w = (cantonal_data.loc["japroz"] > 0.5).multiply(weights, axis=1)
results_b_u = (cantonal_data.loc["japroz"] > 0.5)
my_kt_ja_b_w = results_b_w.sum(axis=1) > (number_cantons-3.0)/2
my_kt_ja_b_u = results_b_u.sum(axis=1) > number_cantons/2

results_p_w = cantonal_data.loc["japroz"].multiply(weights, axis=1).sum(axis=1)
results_p_u = cantonal_data.loc["japroz"].sum(axis=1)
my_kt_ja_p_w = results_p_w > 0.5*(number_cantons-3.0)
my_kt_ja_p_u = results_p_u > 0.5*number_cantons

same_b_w = (my_kt_ja_b_w == reference_decision)
same_b_u = (my_kt_ja_b_u == reference_decision)
same_p_w = (my_kt_ja_p_w == reference_decision)
same_p_u = (my_kt_ja_p_u == reference_decision)

