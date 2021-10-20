import streamlit as st
import pandas as pd
import copy
import pydeck as pdk
import geopandas as gpd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


# Reference for data and information - 
# https://ourworldindata.org/internet#internet-access

# SETTING PAGE STYLE
# st.set_page_config(layout="wide")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)


# 1 - SHARE OF PEOPLE ONLINE
# BROADBAND + CELLULAR


# Information
st.markdown("<h4><b>Hello Internet!</b></h4>", unsafe_allow_html=True)
st.markdown(''' The Internet’s history goes back some decades by now – 
email has been around since the 1960s, file sharing since at least the 1970s, 
and TCP/IP was standardized in 1982. But it was the creation of the world wide 
web in 1989 that revolutionized our history of communication. The inventor of 
the world wide web was the English scientist Tim Berners-Lee who created a system 
to share information through a network of computers.''')

st.markdown(''' Here, I want to look at the global expansion of the internet since
            then and predict the increase in number of internet users the world 
            should expect.<br>''', unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center'; color: blue;'><b><i>How many internet users are there in the world?</i></b></h2><br>", unsafe_allow_html=True)

st.markdown("<h5><b><br><br>What share of people are online?</b></h5>", unsafe_allow_html=True)
st.markdown(''' The map shows the share of the population that is accessing the 
internet for all countries of the world. Internet users are individuals who have 
used the Internet (from any location) in the last 3 months. The Internet can be 
used via a computer, mobile phone, personal digital assistant, games machine, 
digital TV etc.''')
st.markdown('''In richer countries more than two thirds of the population are 
typically online. And although usage rates are much lower in the developing world, 
they are increasing.<br>''', unsafe_allow_html=True)

st.markdown(''' <b>Broadband access </b>refers to fixed subscriptions to high-speed 
                access to the public Internet (a TCP/IP connection), at downstream 
                speeds equal to, or greater than, 256 kbit/s.''', unsafe_allow_html=True)
st.markdown(''' <b>Cellular access </b>refers to mobile data subscriptions to the internet. 
                By changing to the chart view you can see that globally we only 
                saw a very slow rise until the late 1990s and then a dramatically 
                faster increase in mobile device subscriptions since the beginning 
                of the 21st century.<br><br>''', unsafe_allow_html=True)


# 3D MAP - Current users

# geojson file
worldJSON = f"world.geojson"

# CSV Files
fileBroadband = "broadband-penetration-by-country.csv"
fileCellular = "mobile-cellular-subscriptions-per-100-people.csv"
fileUserShare = "share-of-individuals-using-the-internet.csv"

# Read CSV files
def load_data_Br():
    data = pd.read_csv(fileBroadband)
    return data

def load_data_Cell():
    data = pd.read_csv(fileCellular)
    return data

def load_data_Share():
    data = pd.read_csv(fileUserShare)
    return data

# Function calls
dataBroadband = load_data_Br()
dataCellular = load_data_Cell()
dataShare = load_data_Share()


# Select data to display
choices = ("% Population using internet", "Broadband Users", "Cellular Users")
choice = st.radio("Select type of data to be visualized", choices, 0)
yearSlider = st.slider('Year', 1990, 2019, value=2010)

def loadYearwise(df, year):
    return df[df["Year"] == year]

data = None
selector = None
if choice == "Broadband Users":
    data = dataBroadband
    selector = "Fixed broadband subscriptions"
    data["visualizer"] = copy.deepcopy(data[selector]*5)
    multiplier = 100000
elif choice == "Cellular Users":
    data = dataCellular
    selector = "Mobile cellular subscriptions"
    data["visualizer"] = copy.deepcopy(data[selector])
    multiplier = 100000
elif choice == "% Population using internet":
    data = dataShare
    selector = "Individuals"
    multiplier = 50000
    data["visualizer"] = copy.deepcopy(data[selector])


# New dataframe to plot on map
world = gpd.read_file(worldJSON)
df_merged = pd.merge(world, loadYearwise(data, yearSlider), left_on='ISO_A3', 
                        right_on='Code', how='inner')
# print(df_merged.head)


# Color picker - Visualizer
color = st.color_picker('Pick a color shader', '#6ec9f0')
def hex_to_rgb(value):
     # Source: 
     # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
rgb = hex_to_rgb(color)
max_val = df_merged[selector].max()
df_merged["color_index"] = pd.Series([[(rgb[0]/max_val)*i,(rgb[1]/max_val)*i,(rgb[2]/max_val)*i] for i in df_merged[selector]])


initial_view_state = pdk.ViewState(latitude=40.52, longitude=0, zoom=0.35)
df_merged[selector] = df_merged[selector].round(2)
tooltip = {"html": "<b>Country:</b> {Entity}<br> <b>Year:</b> {Year}<br> <b>Value:</b> {" + selector + "}<br>"}


# Country polygon display on map
geojson = pdk.Layer(
    "GeoJsonLayer",
    df_merged,
    pickable=True,
    opacity=0.5,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe= False,
    get_elevation="visualizer",
    elevation_scale=multiplier,
    get_fill_color="color_index",
    get_line_color=[155, 10, 0],
    # get_line_width=2,
    # line_width_min_pixels=1,
)

layers = [geojson]
r = pdk.Deck(
        layers=layers,
        initial_view_state=initial_view_state,
        map_style="light",
        tooltip=tooltip,
    )
st.write(r)
st.caption("Data source: ourworldindata.org")




# 2 - NO. OF USERS - Current + Future

st.markdown("<h2 style='text-align: center'; color: blue;'><b><i><br>How many more are coming?</i></b></h2><br>", unsafe_allow_html=True)
st.markdown("<h5><b><br>Quantifying internet users</b></h5>", unsafe_allow_html=True)
st.markdown('''The overarching trend globally – and, as the chart shows, in all world 
            regions – is clear: more and more people are online every year. The speed 
            with which the world is changing is incredibly fast. On any day in the 
            last 5 years there were on average 640,000 people online for the first time.<br><br>''', unsafe_allow_html=True)


# Prediction Model - Linear/RBF/Polynomial Regression
def prediction_model(type, country):
    # Source - https://scikit-learn.org/stable/auto_examples/svm/plot_svm_regression.html
    temp_df = pd.DataFrame()
    for c in country:
        data = dataUser[dataUser["Entity"] == c]
        years = np.array(data["Year"].tolist()).reshape(-1,1)
        values = np.array(data["Number of internet users (OWID based on WB & UN)"].tolist()).reshape(-1,1)
        
        # Train
        svr_type = None
        # print(type)
        if type == "RBF":
            svr_type= SVR(kernel="rbf", C=1, gamma=0.1, epsilon=.1)
        elif type == "Linear":
            svr_type= SVR(kernel="linear", C=1, gamma='auto')
        elif type == "Polynomial":
            svr_type= SVR(kernel="poly", C=1, gamma='auto', degree=3, epsilon=.1)
    
        sc_X = StandardScaler()
        sc_y = StandardScaler()
        X = sc_X.fit_transform(years)
        y = sc_y.fit_transform(values)
        
        svr = svr_type.fit(X,y)

        # Generate predicted values
        predYears = []
        for i in range(2017,2036):
            predYears.append(i)
            y_pred = sc_y.inverse_transform((svr.predict(sc_X.transform(np.array([[i]]))).reshape(1, -1) ))
            temp_df = temp_df.append({"Entity": c, "Code": data["Code"].values[0], 
                                    "Year": i, "Number of internet users (OWID based on WB & UN)" : y_pred[0][0]}, 
                                    ignore_index = True)
    return temp_df


# CSV file path
fileUserNumber = "number-of-internet-users-by-country.csv"
# Function to read CSV file
def load_data_User():
    data = pd.read_csv(fileUserNumber)
    return data
dataUser = load_data_User()


# Variables for interaction
prediction_types = ["Linear", "RBF", "Polynomial"]
prediction_option = st.radio("Select type of Machine Learning model you want to apply to predict the future increase in internet users:", 
                                prediction_types, 0)
country_options = dataUser["Entity"].unique().tolist()
country = st.multiselect('Choose countries for comparison:', country_options, 
                        ['World', 'United States', 'India', 'Canada', 'Singapore', 
                        'China', 'Bangladesh'])
# year_option  = st.slider('Year', 1990, 2035, value=2012)


# Add new data
predict_data = prediction_model(prediction_option, country)
dataUser = dataUser.append(predict_data)

# Data filtering
user = dataUser[dataUser['Entity'].isin(country)]
user_history = []

for y in user["Year"].unique():
    df1 = user[user["Year"] <= y]
    df1["year_upto"] = y
    user_history.append(df1)

user_animation = pd.concat(user_history)
max_y = user_animation["Number of internet users (OWID based on WB & UN)"].max()
user_animation = user_animation.sort_values(["year_upto", "Year"], ascending=(True, True))
fig2 = px.line(user_animation, x="Year", y="Number of internet users (OWID based on WB & UN)", color="Entity",
                title='No. of internet users (OWID based on WB & UN)', labels={"Entity": "Country:", 
                        "Number of internet users (OWID based on WB & UN)":"No. of internet users"}, 
                        hover_name='Entity', markers=True,
                        log_x=True, range_x=[1990,2035], range_y=[0,max_y], animation_frame="year_upto")
fig2.update_layout(height=600)
fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 10


st.plotly_chart(fig2, use_container_width=True)
st.caption("Data source: ourworldindata.org")
