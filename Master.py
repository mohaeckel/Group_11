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


teste = Energy()

df = teste.read_data(
    "https://github.com/owid/energy-data/raw/master/owid-energy-data.csv")
df.head()

b = teste.countries_list()
