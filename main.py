import streamlit as st
import sqlite3
import plotly.express as px
import requests
import time
import selectorlib
import pandas as pd

filepath = "database.db"
URL = "http://programmer100.pythonanywhere.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractedinstance = selectorlib.Extractor.from_yaml_file("scrape.yaml")
    value = extractedinstance.extract(source)["source"]
    return value


def added_row(temp):
    date = time.asctime()
    row = [date,int(temp)]
    return row


def add_to_db(row):
    c = connection.cursor()
    c.execute("INSERT INTO temperatures VALUES(?,?)", (row))
    connection.commit()
    
def read_sql(filepath):
    c = connection.cursor()
    dt = pd.read_sql("SELECT * FROM temperatures", connection)
    return dt
    

if __name__=="__main__":
    connection = sqlite3.connect("database.db")
    st.title("Temperatures")    
    figure = read_sql(filepath)
    frame = px.line(figure, x="Date", y="Temperature")
    st.plotly_chart(frame)
    while True:
        source = scrape(URL)
        temperature = extract(source)
        row = added_row(temperature)
        add_to_db(row)
        print(row)
        time.sleep(5)