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

    data: pandas dataframe
        Where data about energy is stored

    Methods
    --------

    """

    def __init__(self, data=None):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        -----------

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
            print("Downloads folder exists")

        if os.path.isfile("./downloads/data.csv") is True:
            print("File exists")
        else:
            req = requests.get(url)
            url_content = req.content
            csv_file = open('./downloads/data.csv', 'wb')
            csv_file.write(url_content)
            csv_file.close()

        df = pd.read_csv("./downloads/data.csv")

        return df


test = Energy()

a = test.read_data(("https://www.stats.govt.nz/assets/Uploads/Annual-enterpri" /
                    "se-survey/Annual-enterprise-survey-2020-financial-year-p" /
                    "rovisional/Download-data/annual-enterprise-survey-2020-f" /
                    "inancial-year-provisional-csv.csv"))
a.head()
