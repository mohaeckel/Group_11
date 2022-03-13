from energy import Energy

test = Energy()
df = test.read_data(True)
# test.arima_forecast("China", 10)
test.consumption_country(["Czechia", "Morocco", "Bulgaria"])
