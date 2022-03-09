"""
MASTER FILE ASSIGNMENT 1 __GROUP11

Farouq El-Abass
Moritz Häckel
Dominik Trut
Moritz Güttersberger

"""
import requests
import pandas as pd
import os
import plotly_express as px
from datetime import datetime
import matplotlib.pyplot as plt



class Energy():

    def __init__(self, data=None):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        -----------
        data : panda dataframe
            Data for the Energy but will be affected later

        Returns
        --------
        Nothing, it's just a contructor
        """
        self.data = data

    def read_data(self, drop_continents: bool = False,
                  url="https://github.com/owid/energy-data/raw/" +
                  "master/owid-energy-data.csv"):
        """
        Downloads the data in the ´/downloads´ folder and reads data as well

        Parameters
        -----------
        url: string
            Link of the data from internet
        drop_continents: bool
            Drops continents and aggregated countries from dataset

        Returns
        --------
        df: pandas dataframe
            Dataframe of the data
        """
        path = os.getcwd()
        if os.path.exists(os.getcwd()+'/downloads') is False:
            os.mkdir(path+"/downloads")
        else:
            pass

        if os.path.isfile("./downloads/data.csv") is True:
            pass
        else:
            req = requests.get(url)
            url_content = req.content
            csv_file = open('./downloads/data.csv', 'wb')
            csv_file.write(url_content)
            csv_file.close()

        self.data = pd.read_csv("./downloads/data.csv")
        self.data = self.data[self.data["year"] >= 1970]
        if drop_continents is True:
            self.data = self.data.dropna(
                subset="iso_code")
            self.data = self.data.set_index("country").drop("World")
            self.data = self.data.reset_index()

        else:
            pass

        self.data["timestamp"] = pd.to_datetime(self.data["year"], format="%Y")
        self.data = self.data.set_index("timestamp")

        # enrich data with 'emissions'
        self.data['emissions'] = self.data[
            'carbon_intensity_elec']*10**(-6) / 10**(-9)

        return self.data

    def countries_list(self):
        """
        Returns the list of countries in the data

        Parameters
        ----------
        None

        Returns
        -------
        country_list : list

        """
        countries = self.data["country"].unique()
        return countries.tolist()

    def gdp_over_years(self, countries):
        """
        Receive a string or a list of strings -> Compare the "gdp" column of
        each received country over the years

        Parameters
        ----------
        countries : list of strings
            DESCRIPTION. Name of every country that is included

        Returns
        -------
        gdp_over_years_df: pandas Dataframe
            DESCRIPTION: GPD of countries over the years
                columns = Countries
                index = years
        """
        df = self.data
        cut = df[["year", "country", "gdp"]]
        gdp_over_years_df = cut.pivot(
            index="year", columns="country", values="gdp")
        

        return gdp_over_years_df[countries]

    def consumption_country(self, countries):
        """
        The method produces a dataframe with defined countries in columns and
        all years in rows. Values are the sum of the total energy consumption
        of the country.

        Parameters
        ----------
        countries : list of strings
            A list of countries that are included in the consumption per
            country dataframe

        Returns
        -------
        Bar Plot:
            Displays the bar plot of the total consumption for each
            country.

        """
        df = self.data[["country", "biofuel_consumption",
                        "coal_consumption",
                        "gas_consumption",
                        "hydro_consumption",
                        "nuclear_consumption",
                        "oil_consumption",
                        "solar_consumption",
                        "wind_consumption",
                        "emissions"]]

                        "wind_consumption", "emissions"]]
        df = df.groupby("country").sum()
        df["total_consumption"] = df.iloc[:, :8].sum(axis=1)
        df = df.loc[countries]
        return df.reset_index()[["total_consumption",
                               "emissions"]].plot.bar(ls = '-',
                                                      secondary_y="emissions",
                                                      )
        
        
        return df.reset_index().plot.bar(x = "country", 
                                         y = "total_consumption"),
        df['emissions'] = plt.subplots()
        

    def prepare_df(self, metric):
        """
        The method produces a dataframe of all countries and years for one
        transmitted metric (i.e. GDP or Population).

        Parameters
        ----------
        metric : string
            The name of the column from which values are extracted
            (i.e. "gdp" for values of gdp column).

        Returns
        -------
        metric_df: dataframe
            A dataframe that has all countries in columns and years in rows.
            Values are the defined metric
        """

        df = self.data
        cut = df[["year", "country", metric]]
        metric_df = cut.pivot(
            index="year", columns="country", values=metric)
        return metric_df

    def consumption_area_plot(self, country, normalize):
        """
        Returns an area chart of the '_consumption' columns
        for a selected country

        Parameters
        ----------
        country : string
            country you want to see the area chart for.
        normalize : boolean
            normalize the chart or not.

        Returns
        -------
        area_chart : chart

        """
        if country not in self.countries_list():  # hashing error here
            raise TypeError("ValueError")

        self.data = self.data.reset_index()
        df = self.data[["country", "year", "biofuel_consumption",
                        "coal_consumption",
                        "gas_consumption",
                        "hydro_consumption",
                        "nuclear_consumption",
                        "oil_consumption",
                        "solar_consumption",
                        "wind_consumption"]]
        dfcountry = df[df["country"] == country]

        if normalize is True:
            df_norm = pd.concat(
                [dfcountry[["country", "year"]],
                 dfcountry.iloc[:, 3:].apply(
                     lambda x: x / x.sum(), axis=1)], axis=1)
            return df_norm.plot.area('year', stacked=True)
        else:
            return dfcountry.plot.area('year', stacked=True)

    def gapminder(self, year):
        """
        This method shows the correlation between gpd, total engery
        consumption and the population per year.

        Parameters
        ----------
        year : TYPE
        """

        """try:
            isinstance(year, int)
                #or:  year = int()
        except TypeError:
            print("Type Error: the year is not an integer.")
         """

        df = self.data
        df["total_consumption"] = df[["biofuel_consumption",
                                      "coal_consumption",
                                      "gas_consumption",
                                      "hydro_consumption",
                                      "nuclear_consumption",
                                      "oil_consumption",
                                      "solar_consumption",
                                      "wind_consumption"]].sum(axis=1)

        gapminder_df = df[['country', 'year',
                           'gdp', 'population',
                           'total_consumption']].reset_index()
        gapminder_df = gapminder_df[gapminder_df['total_consumption'] != 0]

        px.scatter(
            gapminder_df.query("year == "+str(year)),
            x="gdp",
            y="total_consumption",
            animation_frame="year",
            animation_group="country",
            size="population",
            color="country",
            # hover_name="country",
            log_x=True,
            log_y=True,
            size_max=60).show(renderer="svg")
        
    def allcountries_scatter (self):
        df = self.data 
