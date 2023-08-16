import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import json
from PIL import Image
import requests
# from streamlit_lottie import st_lottie

# making wider webpage
st.set_page_config(layout = "wide")
st.write("Hii, I am Abhisek. Welcome to my Website :wave:")

# for background color and font color
with open("colour.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>",unsafe_allow_html = True)
    
def local_css(filename):
	with open(filename) as f:
		st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("style.css")

# importing datasets for navigation bar
lap = pd.read_csv("lap_price2.csv")
carp = pd.read_csv("car_Price.csv")
bikep = pd.read_csv("bike_price.csv")

#laptop price label encoder pickles
company = pickle.load(open('com.pkl','rb'))
typeName = pickle.load(open('typen.pkl','rb'))
cpU = pickle.load(open('cpu.pkl','rb'))
gpU = pickle.load(open('gpu.pkl','rb'))
oss = pickle.load(open('os.pkl','rb'))

# car price label encoder pickles
cnm = pickle.load(open('name_car.pkl','rb'))
fuelType = pickle.load(open('fuel_car.pkl','rb'))
transMission = pickle.load(open('transmission.pkl','rb'))

# bike price label encoder pickles
bike = pickle.load(open("bname.pkl",'rb'))
owner1 = pickle.load(open("own.pkl",'rb'))

#Loading the models
model1 = pickle.load(open("rfr.pkl","rb"))

model2 = pickle.load(open("random_car.pkl",'rb'))

model3 = pickle.load(open("xgb.pkl",'rb'))

# Forming sidebar for navigation
with st.sidebar:
    selected = option_menu('Commodity Names',options=['Laptop','Car',
                    'Bike'],icons = ['laptop','car-front-fill','bicycle'],default_index=0,
                        orientation= "vertical",menu_icon=['bank'])
# making navigation bar contents

#for Laptop
if (selected == 'Laptop'):
    left_column,right_column = st.columns(2)
    with st.container():
        with left_column:
            st.title("Laptop Price Predictor")
            st.subheader("Get the Best Price of your Laptop")
        st.write('---')
        car_img = Image.open("lap_img.png")
    
        with right_column:
            st.image(car_img,width = 200)
    
        c1,c2,c3 = st.columns(3)
        with c1:
            n = lap['Company'].unique().tolist()
            n.sort()
            com = st.selectbox('Model Name',n)
            com = company.transform([com])[0]
        with c2:
            b = lap['TypeName'].unique().tolist()
            b.sort()
            typ = st.selectbox('Type',b)
            typ = typeName.transform([typ])[0]
        with c3:
            y = lap['Ram'].unique().tolist()
            y.sort()
            ram = st.selectbox('RAM(GB)',y)
        with c1:
            weit = st.number_input('Enter the Weight')
        with c2:
            ts = st.selectbox('Touchscreen',['Yes','No'])
            if ts == 'Yes':
                ts = 1
            else:
                ts = 0
        with c3:
            ips = st.selectbox('IPS Panel',['Yes','No'])
            if ips == 'Yes':
                ips = 1
            else:
                ips = 0
        with c1:
            ppi = st.number_input('Enter PPI value')
        with c2:
            e = lap['Cpu brand'].unique().tolist()
            e.sort()
            cpu = st.selectbox('CPU Name',e)
            cpu = cpU.transform([cpu])[0]
        with c3:
            p = lap['HDD'].unique().tolist()
            p.sort()
            hdd = st.selectbox('HDD size(GB)',p)
        with c1:
            g = lap['SSD'].unique().tolist()
            g.sort()
            ssd = st.selectbox('SSD size(GB)',g)
        with c2:
            j = lap['Gpu brand'].unique().tolist()
            j.sort()
            gpu = st.selectbox('GPU Name',j)
            gpu = gpU.transform([gpu])[0]
        with c3:
            v = lap['OS'].unique().tolist()
            v.sort()
            os = st.selectbox('OS Name',v)
            os = oss.transform([os])[0]
        
        if st.button('Click Here'):
            lap_pri = model1.predict([[com,typ,ram,weit,ts,ips,ppi,cpu,hdd,ssd,gpu,os]])
            price1 = lap_pri[0]
            st.header('The Estimated Price is ' + str(np.round(np.exp(price1),decimals=2)) + ' Rs.')
          

# for Car  
if (selected == 'Car'):
    left_column,right_column = st.columns(2)
    with st.container():
        with left_column:
            st.title("Car Price Predictor")
            st.subheader("Find Best Price of your Car")
        
        car_img = Image.open("car_img.png")
    
        with right_column:
            st.image(car_img,width = 250)
        st.write("___")
        
        c1,c2,c3 = st.columns(3)
        with c1:
            m = carp['name'].unique().tolist()
            m.sort()
            mn = st.selectbox('Model Name',m)
            mn = cnm.transform([mn])[0]
        with c2:
            r = carp['year'].unique().tolist()
            r.sort()
            by = st.selectbox('Bought Year',r)
        with c3:
            km = st.number_input('Km Driven')
        with c1:
            ft = st.selectbox('Fuel Type',carp['fuel'].unique().tolist())
            ft = fuelType.transform([ft])[0]
        with c2:
            tt = st.selectbox('Transmission Type',carp['transmission'].unique().tolist())
            tt = transMission.transform([tt])[0]
        with c3:
            f = carp['seats'].unique().tolist()
            f.sort()
            sit = st.selectbox('No. of Seats',f)
        with c1:
            php = st.number_input('Power(Horse Power)')
        with c2:
            trk = st.number_input('Torque(CC)')
        with c3:
            kml = st.number_input('Mileage(km/Ltr)')
        
        
        if st.button('Click Here'):
            input_value = (mn,by,km,ft,tt,sit,php,trk,kml)
            input_value = np.asarray(input_value)
            input_value = input_value.reshape(1,-1)
            car_pri = model2.predict(input_value)
            price1 = car_pri[0]
            st.header('The Estimated Price of your Car is '+ str(np.round(price1,decimals = 2)) + ' Rs.')


# for Bike
if (selected == 'Bike'):
    left_column,right_column = st.columns(2)
    with st.container():
        with left_column:
            st.title("Bike Price Predictor")
            st.subheader("Find the Best Value of your Bike")
        bike_img = Image.open("bike_img.png")
    
        with right_column:
            st.image(bike_img,width = 250)
        st.write("___")
        
        h = bikep['bike_name'].unique().tolist()
        h.sort()
        bn = st.selectbox('Model Name',h)
        bn = bike.transform([bn])[0]
        
        c1,c2 = st.columns(2)
        with c1:
            kmd = st.number_input('Km Driven')
        with c2:
            oon = st.selectbox('Owner',bikep['owner'].unique().tolist())
            oon = owner1.transform([oon])[0]
        with c1:
            pcc = st.number_input('Power(CC)')
        with c2:
            s = bikep['year'].unique().tolist()
            s.sort()
            yar = st.selectbox('Bought Year',s)
        
        if st.button('Click Here'):
            input_value = (bn,kmd,oon,pcc,yar)
            input_value = np.asarray(input_value)
            input_value = input_value.reshape(1,-1)
            pred = model3.predict(input_value)
            prediction = pred[0]
            st.header('The Estimated Price of your Bike is '+ str(np.round(prediction,decimals = 2)) + ' Rs.')
        

#st.write("[Contact with us >](https://mail.google.com/mail/u/0/#inbox)")
