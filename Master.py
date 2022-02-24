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


class Energy():
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

    def new_function(self):
        return print("Hey")

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

        Parameters
        ----------
        countries : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

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


teste = Energy()

df = teste.read_data(
    "https://github.com/owid/energy-data/raw/master/owid-energy-data.csv")
df.head()

b = teste.countries_list()

c = teste.gdp_over_years(["Albania", "Afghanistan", "Morocco"])

teste.consumption_country(["Albania", "Afghanistan", "Morocco"])
