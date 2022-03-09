from energy import Energy


test = Energy()
df = test.read_data(drop_continents=True)
test.consumption_area_plot("Morocco", True)
test.gapminder(2016)
