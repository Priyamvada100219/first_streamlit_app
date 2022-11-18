import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('Hello ,My parents new healthy Dinner.')

streamlit.header('Breakfast Menu')
streamlit. text('🥣 Omega 3 & Bluberry oatmeal')
streamlit.text('🥗 Kale,Spinach & Rocket Smoothie')
streamlit.text('🍞 Hard-Boiled Free-Range Egg Sandwich ')
streamlit.text('🥑 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']) 
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the  table on the page
streamlit.dataframe(fruits_to_show)


# create the repeatable  code block (called function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # take the json version of the response and Normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
# New section to display fruityvice api response 
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not  fruit_choice:
        streamlit.error("please select a fruit to get information")
   else:
        back_from_function=get_fruityvice_data(fruit_choice)
        # output it the screen  as table 
        streamlit.dataframe(back_from_function)
except URLError as e:
      streamlit.error()

#dont run anything past here  while we troubleshoot
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load contains")
streamlit.dataframe(my_data_rows) 

#Allow the end user to add fruit list
add_my_fruit_list = streamlit.text_input('What fruit would you like to add?','banana')
streamlit.write('Thanks for adding', add_my_fruit_list)

#This will not work correctly but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
