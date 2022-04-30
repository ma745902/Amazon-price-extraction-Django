from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.db import models
import datetime
from amazonapp.models import Product  # Reterieve model from App

'''
def index(request):
    return HttpResponse ("
    <h1><strong>Welcome to Amazon Price Extraction</strong></h1>
    
    ")


def show(request):
    return render(request, "index.html")


def upload(request):


    return render(request,"upload.html")
'''

# --------------------------
from django.shortcuts import  render
from django.core.files.storage import FileSystemStorage
import os
import json
import pandas as pd
import numpy as np
import csv
from django.conf import settings
import requests
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
# --------------------------

#    Amazon Price Extraction through URL
#    Amazon Extraction Price urls Python script.

import tests
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def extract_price(url):

    f = requests.get(url, headers=headers)
    soup = BeautifulSoup(f.content, features="html.parser")

    d = soup.find('span', {'class': 'a-button a-button-selected a-spacing-mini a-button-toggle format'})

    if not d.find('span', {'class': 'a-color-base'}):
        price = d.find('span', {'class': 'a-size-base a-color-price a-color-price'})
        price=str(price.text)
        return price

    else:

        price = d.find('span', {'class': 'a-color-base'})
        price = str(price.text)
        return price


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


def show(request):

    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, r'dataset.csv'), index_col=False)
    #  ------------------------------

    urls = df['Title'].tolist()
    list = []
    for i in range(1, 10):
        list.append(urls[i])

    old_price = df['Updated Price'].tolist()

    old_price = [old_price[i] for i in range(1, 10)]

    # Date

    date=df['Date'].tolist()

    date=[date[i] for i in range(1,10)]

    # ---------------------

    updated = []
    for item in list:
        updated.append(extract_price(item))

    final = []
    for item in updated:
        final.append(item.strip())
    # -------------------------------

    #  write price into Excel File

    # ---------------------------

    extracted_df = pd.DataFrame({'links': list, 'Old': old_price, 'latest': final, 'date':date})

    print(extracted_df)






    #-------------------------------------------
    json_records = extracted_df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}


    return render(request, 'index.html', context)


#-------  Upload File using This Function


#        Upload
# --------------------------
# --------------------------


def upload(request):

    if request.method == 'POST' and request.FILES['upload']:

        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        if "csv" in str(upload.name):

            df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, upload.name), index_col=False)
            urls = df['Title'].tolist()
            list = []
            for i in range(1, 10):
                list.append(urls[i])

            old_price = df['Updated Price'].tolist()

            old_price = [old_price[i] for i in range(1, 10)]

            # Date

            date = df['Date'].tolist()

            date = [date[i] for i in range(1, 10)]

            # ---------------------

            updated = []
            for item in list:
                updated.append(extract_price(item))

            final = []
            for item in updated:
                final.append(item.strip())
            # -------------------------------

            #  write price into Excel File

            # ---------------------------

            extracted_df = pd.DataFrame({'links': list, 'Old': old_price, 'latest': final, 'date': date})

            print(extracted_df)

            # Save data into DataBase
            # -----------------------

            for i in range(0, 5):
                obj = Product()

                obj.url = str(list[i])

                obj.old_price = str(old_price[i])
                obj.new_price = str(final[i])

                obj.date = datetime.datetime.now()

                obj.save()

            # ------------------------

            # -------------------------------------------
            """
            json_records = extracted_df.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
            """

            data = Product.objects.all()

            return render(request,'index.html',{'data':data})

        if "xlsx" in str(upload.name):

            df = pd.read_excel(os.path.join(settings.MEDIA_ROOT, upload.name), index_col=False)
            urls = df['Title'].tolist()
            list = []
            for i in range(1, 10):
                list.append(urls[i])

            old_price = df['Updated Price'].tolist()

            old_price = [old_price[i] for i in range(1, 10)]

            # Date

            date = df['Date'].tolist()

            date = [date[i] for i in range(1, 10)]

            # ---------------------

            updated = []
            for item in list:
                updated.append(extract_price(item))

            final = []
            for item in updated:
                final.append(item.strip())
            # -------------------------------

            #  write price into Excel File

            # ---------------------------

            extracted_df = pd.DataFrame({'links': list, 'Old': old_price, 'latest': final, 'date': date})

            print(extracted_df)

            # Save data into DataBase
            # -----------------------

            for i in range(0, 5):
                obj = Product()

                obj.url = str(list[i])

                obj.old_price = str(old_price[i])
                obj.new_price = str(final[i])

                obj.date = datetime.datetime.now()

                obj.save()

            # ------------------------

            # -------------------------------------------
            """
            json_records = extracted_df.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
            """

            data = Product.objects.all()

            return render(request, 'index.html',{'data':data})


        #  ------------------------------


    return render(request, 'upload.html')
        # Show Data of file
        #-----------------------------
        # ----------------------------


# --------------------------

#-------  Welcome Page using This Function

def welcome(request):
    data = Product.objects.all()
    return render(request, 'welcome.html',{'data':data})

# -----------------------------------------
#------------------------------------------

def fetch_data(request):

    data=Product.objects.all()

    return render(request, 'welcome.html',{'data':data})


def insert(request):


    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, r'input.csv'), index_col=False)

    #  ------------------------------

    # Date

    dd=df['Date'].tolist()

    date=[]

    for i in range(1,10):
        date.append(dd[i])



    #--------------------------------

    urls = df['Title'].tolist()
    list = []
    for i in range(1, 10):
        list.append(urls[i])

    old = df['Updated Price'].tolist()

    old = [old[i] for i in range(1, 10)]

    updated = []

    for item in list:
        updated.append(extract_price(item))

    final = []

    for item in updated:
        final.append(item.strip())




    extracted_df = pd.DataFrame({'links': list, 'Old': old, 'latest': final,'Date':date})



    # obj.url=json.dumps()
    for i in range(0,5):
        obj = Product()

        obj.url=str(list[i])

        obj.old_price =str(old[i])
        obj.new_price = str(final[i])

        obj.date = datetime.datetime.now()

        obj.save()

    # ----------------
    #  create Dictionary

    # -------------------

    print("Data Inserted Successfully")


    # store data into database

    # m=Product(**context)


    # m.save()




    return HttpResponse("""
        <br>
        <h1>Data Inserted Succesfully </h1>
        <br><br>
    
        """)