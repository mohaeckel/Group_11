from energy import Energy


test = Energy()
test.read_data(
    "https://github.com/owid/energy-data/raw/master/owid-energy-data.csv")
test.gapminder(2010)


test.year_index()
