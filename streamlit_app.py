import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothies :cup_with_straw:")
st.write(
  """choose fruits you want in custom smoothie
  """
)
# Get the current credentials
#session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()

#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("name of smoothie")
st.write("your name of smoothie will be", name_on_order)

ingredients_list = st.multiselect(
    'choose upto 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    
    
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruits_choosen in ingredients_list:
        ingredients_string+=fruits_choosen+" "
        st.subheader(fruits_choosen+' NUTRITION INFORMATION')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
  
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    st.write(my_insert_stmt)
    
    time_to_insert=st.button('submit order');
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    st.stop()





