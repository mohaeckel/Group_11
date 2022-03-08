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
import datetime



class Energy():

    def __init__(self, data):
        self.data = data

    """

    Attributes
    ----------


    Methods
    --------

    """

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

    def read_data(self, url):
        """
        Downloads the data in the ´/downloads´ folder and reads data as well

        Parameters
        -----------
        url: string
            Link of the data from internet

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
            print("File exists")
        else:
            req = requests.get(url)
            url_content = req.content
            csv_file = open('./downloads/data.csv', 'wb')
            csv_file.write(url_content)
            csv_file.close()

        self.data = pd.read_csv("./downloads/data.csv")
        self.data = self.data[self.data["year"] >= 1970]

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
        df = pd.concat([self.data["country"], self.data.filter(
            regex="_consumption", axis=1)], axis=1)
        df = df.groupby("country").sum()
        to_drop = ["Africa", "Europe", "Asia Pacific", "World",
                   "North America", "CIS", "Middle East", "OPEC",
                   "South & Central America", "Other Asia & Pacific",
                   "Europe (other)", "Other Middle East",
                   "Other Caribbean"]
        df = df.drop(labels=to_drop, axis=0)
        df["total_consumption"] = df.sum(axis=1)
        df = df.loc[countries]
        return df.reset_index().plot.bar(x="country", y="total_consumption")

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
        to_drop = ["Africa", "Europe", "Asia Pacific", "World",
                   "North America", "CIS", "Middle East", "OPEC",
                   "South & Central America", "Other Asia & Pacific",
                   "Europe (other)", "Other Middle East",
                   "Other Caribbean"]
        metric_df = metric_df.drop(labels=to_drop, axis=1)

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

        df = pd.concat([self.data[["country", "year"]], self.data.filter(
            regex="_consumption", axis=1)], axis=1)
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
        only_countries = [e for e in self.countries_list() if e not in (
            "Africa", "Europe", "Asia Pacific", "World", "North America",
            "CIS", "Middle East", "OPEC", "South & Central America",
            "Other Asia & Pacific", "Europe (other)", "Other Middle East",
            "Other Caribbean")]
        df1 = df.query('country in @only_countries').fillna(0)
        gapminder_df = df1[['country', 'year',
                            'gdp', 'population']].reset_index()
        gapminder_df['total_energy_consumption'] = df1[[
            "biofuel_consumption", "coal_consumption",
            "fossil_fuel_consumption", "gas_consumption", "hydro_consumption",
            "low_carbon_consumption", "nuclear_consumption", "oil_consumption",
            "other_renewable_consumption", "primary_energy_consumption",
            "renewables_consumption", "solar_consumption",
            "wind_consumption"]].sum(axis=1)
        gapminder_df2 = gapminder_df.fillna(0)

        px.scatter(
            gapminder_df2.query("year =="+str(year)),
            x="gdp",
            y="total_energy_consumption",
            animation_frame="year",
            animation_group="country",
            size="population",
            color="country",
            log_x=True,
            log_y=True,
            size_max=60,
            # range_x=[100,100000],
            range_y=[-1500, 5000]).show(renderer="svg")

#Phase 2: Day 1
    def year_index (self):
        df = self.data
        
        
        
        