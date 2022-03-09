from energy import Energy
import plotly_express as px
import pandas as pd
import numpy as np


test = Energy()
df = test.read_data(
    "https://github.com/owid/energy-data/raw/master/owid-energy-data.csv")


test.gapminder(2016)