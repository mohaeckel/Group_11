from energy import Energy

test = Energy()
test.read_data(True)
test.arima_forecast("China", 10)
