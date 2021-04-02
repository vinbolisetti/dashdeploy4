import pathlib

from django.shortcuts import render
import pandas as pd
import numpy as np

# importing libraries
# from ipywidgets import interact, interactive, fixed, interact_manual
# from IPython.core.display import display, HTML

# import matplotlib.pyplot as plt
# import plotly.express as px
# import seaborn as sns


# Create your views here.

def index(request):
    return render(request, 'index.html')


def app1(request):

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../data").resolve()

    df = pd.read_csv(DATA_PATH.joinpath("RFx_Recd1.csv"))
    countries_df = pd.read_excel(DATA_PATH.joinpath("Country_Code.xlsx"))

    df.loc[(df['Division__c'] == 'CEM Sales'), 'Division__c'] = 'CEM'
    df.loc[(df['Division__c'] == 'Indirect Sales'), 'Division__c'] = 'Indirect'
    df.loc[(df['Division__c'] == 'Enterprise Content Services'), 'Division__c'] = 'ECS'
    df.loc[(df['Division__c'] == 'Professional Services'), 'Division__c'] = 'PS'
    df.loc[(df['Division__c'] == 'Indirect Sales'), 'Division__c'] = 'Indirect'
    df.loc[(df['Division__c'] == 'Business Network'), 'Division__c'] = 'BN'
    df.loc[(df['Division__c'] == 'APAC Sales'), 'Division__c'] = 'APAC'
    df.loc[(df['Division__c'] == 'US Public Sector Sales'), 'Division__c'] = 'US Public Sector'
    df.loc[(df['Division__c'] == 'Security Sales'), 'Division__c'] = 'Security'
    df.loc[(df['Division__c'] == 'LegalTech Sales'), 'Division__c'] = 'LegalTech'
    df.loc[(df['Division__c'] == 'Analytics & AI Sales'), 'Division__c'] = 'Analytics & AI'
    df.loc[(df['Division__c'] == 'Indirect Sales'), 'Division__c'] = 'Indirect'
    df.loc[(df['Division__c'] == 'LATAM Sales'), 'Division__c'] = 'LATAM'

    df.loc[df['USD_Price__c'].isnull(), 'USD_Price__c'] = 0
    df['USD_Price__c'] = df['USD_Price__c'].mask(df['USD_Price__c'] > 0, df['USD_Price__c'] / 1000000).round(decimals=2)

    df['RFx_Received_Date__c'] = pd.to_datetime(df['RFx_Received_Date__c'])
    df['RFx_Received_Date__c'] = df['RFx_Received_Date__c'].apply(lambda x: pd.Timestamp(x).strftime('%d-%B'))

    df.loc[(df['RFx_Type__c'] == 'RFQ (Request for Quote)'), 'RFx_Type__c'] = 'RFQ'
    df.loc[(df['RFx_Type__c'] == 'RFP (Request for Proposal)'), 'RFx_Type__c'] = 'RFP'
    df.loc[(df['RFx_Type__c'] == 'RFI (Request for Information)'), 'RFx_Type__c'] = 'RFI'
    df.loc[(df['RFx_Type__c'] == 'EOI (Expression of Interest)'), 'RFx_Type__c'] = 'EOI'
    df.loc[(df['RFx_Type__c'] == 'ITT (Invitation to Tender)'), 'RFx_Type__c'] = 'ITT'

    df['Industry__c'] = df['Industry__c'].fillna(0)
    df['Industry__c'] = np.where(df['Industry__c'] == 0, df['Industry_x__c'], df['Industry__c'])

    df = df.rename(columns={"Account_Country__c": "Country Code"})
    df = df.merge(countries_df, on='Country Code', how='left')

    df = df[['RFxName', 'AccountName', 'USD_Price__c', 'Division__c', 'Country', 'Industry__c']]
    df = df.rename(
        columns={"RFxName": "RFx Name", "AccountName": "Customer Name", "USD_Price__c": "Proposal Quoted Pricing ($M)",
                 "Division__c": "Business Unit", "Industry__c": "Industry"})

    df.drop(df[df['Proposal Quoted Pricing ($M)'] < 0].index, inplace=True)
    df.dropna(subset=["Business Unit"], inplace=True)
    df.dropna(subset=["Industry"], inplace=True)

    df1 = df.groupby(['Business Unit'])['Proposal Quoted Pricing ($M)'].sum().sort_values(ascending=False).reset_index()

    df1 = df1.sort_values(by='Proposal Quoted Pricing ($M)', ascending=False)

    buVals = df1['Business Unit'].values.tolist()
    amtVals = df1['Proposal Quoted Pricing ($M)'].values.tolist()

    context = {
        'buVals': buVals,
        'amtVals': amtVals,
    }

    return render(request, 'base.html', context)
