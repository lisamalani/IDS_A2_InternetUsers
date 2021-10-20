# IDS_A2_InternetUsers
An interactive application that enables the exploration of a dataset (here, internet users)


# assignment-2-lisamalani
assignment-2-lisamalani created by GitHub Classroom

Goals of the project:
To understand the current and predict the future increase in the internet users across the globe. The idea is to be able to create visual tools to analyse the internet usage growth per country while simultaneously be able to draw comparison between different countries.

Datasets used (procured from Kaggle, verified from ourworldindata.org): 
1.	Share of Individuals using the internet
2.	2. Broadband penetration by country
3.	Mobile cellular subscriptions per 100 people
4.	Number of internet users by country

ML Regression Models (using sklearn library):
1.	Linear 
2.	RBF
3.	Polynomial

Design decisions:
The broad idea is to visualize the data by showing clear patterns about the data and makes it easy for analysis.
Geo-plotting of the world data with a slider that shows the usage for the selected year.
Focus the internet usage growth for top 3 countries and a list of top 10.

A comparison table that lets user add countries they want to compare and draw their relevant charts.
1.	Geo-plotting – Allows us to plot out information on a global scale and see how a certain variable is distributed across a territory. This visually appealing plot style holds the ability to process a lot of information at one glance.  The 3D feature of geo-plotting allows us visually rank the data entities (here, country)
2.	 Line Graph – Fundamental chart type to track changes over a period of time. Line graphs are better for use when the changes are smaller with markers , which help to make a visual understanding of the difference between two values and easily draw inference in their change. Line graphs are also useful when the need is to plot multiple entities over the same period for comparison. 
 - Clear data for reading and comparison
- Ease to understand
- Fun to animate

Widgets:
1.	Radial Buttons – to plot different data and to select a regression model. 
As these options are mutually exclusive and the user must select exactly one choice, it is ideal to provide a radial button. Since the options are limited (only 3 in each case), there is no need to go for a dropdown list. Moreover, radial button display all the available options for user to make a decision from the get-go.

2.	Slider–Year
To provide a range of data that the user would want to visualize. It allows the user to smoothly move across the different years and visualize the growth in the projected data. This interaction help to read deeper into the data and analyse the progress more interactively.

3.	Colour picker – 3D Map polygons
Giving user the freedom to colour code the data as per their visual appeal. Default colour is set to blue – colour-blind friendly.

4.	Multiselect – Country list
Conserving screen space, the multiselect widget allows users to intuitively select the countries they want to compare. The widget also prevents users from entering erroneous data, since the widget shows only legal choices.

Development process:
1.	Procured relevant datasets from Kaggle.com and verified the same from ourworldindata.org.
2.	Analysed the data set manually to draw conclusions on data available and their respective quantities.
3.	Used pandas to clean and add values to dataframe wherever required
4.	Explored and used libraries such as folium ( choropleth maps), pydeck and geopandas to understand how to plot polygons on a world map; plotly for line graph and its animation.
5.	Used Python and Streamlit libraries to plot the data to a local hosted website emphasizing users ability to engage with the information using interaction techniques such as year slides, tooltips, animation , multiselect, panning etc. 
6.	Integrated ML regression models through sklearn library to predict the increase of internet usage.
