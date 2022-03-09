from energy import Energy


test = Energy()
df = test.read_data(drop_continents=True)


df1 = df[["country", "biofuel_consumption",
         "coal_consumption",
          "gas_consumption",
          "hydro_consumption",
          "nuclear_consumption",
          "oil_consumption",
          "solar_consumption",
          "wind_consumption",
          "emissions"]]
df1 = df1.groupby("country").sum()

df1["total_consumption"] = df1.iloc[:, :8].sum(axis=1)

test.consumption_country(["France", "Spain"])
