from energy import Energy

test = Energy()
df = test.read_data(True)
test.arima_forecast("France", 10)
# test.consumption_country(["Czechia", "Morocco", "Bulgaria"])
# test.allcountries_scatter(2016)
# ch = df[df["country"] == "France"]
# ch.plot(y="emissions")
