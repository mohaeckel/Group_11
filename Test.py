from energy import Energy


test = Energy()
df = test.read_data(drop_continents=True)


test.consumption_country(["France","Germany"])
