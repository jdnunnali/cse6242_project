import streamlit as st
import pandas as pd
import numpy as np
import time
import json

from SPARQLWrapper import SPARQLWrapper, JSON
from streamlit_agraph import agraph, Node, Edge, TripleStore, Config


st.title("Recipe Recommender Network")


testDf = pd.DataFrame({"a":[1,2,3,4,5],
                       "b":[11,12,13,14,15]})


nodes = []
edges = []
nodeSize = 500

recipe_images = {"Spicy Chicken": "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/37/21/1/picdx8xbY.jpg",
                 "Spicy Potatoes": "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/54/57/7/pic1IWdex.jpg",
                 "Pork Belly": "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/23/87/73/aeTvkKFkTuKUm5tv1PmH_porkbelly-1470.jpg",
                 "Jamaican Fish": "https://thatgirlcookshealthy.com/wp-content/uploads/2018/03/Jamaican-steam-fish.jpg",
                 "Pickles": "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/18/02/57/picA94k8p.jpg"}

nodes.extend([Node(id="Spicy Potatoes",label="Spicy Potatoes",size=nodeSize, svg="https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/54/57/7/pic1IWdex.jpg"),
             Node(id="Spicy Chicken",label="Spicy Chicken",size=nodeSize, svg= "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/37/21/1/picdx8xbY.jpg"),
             Node(id="Pork Belly",label="Pork Belly",size=nodeSize, svg="https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/23/87/73/aeTvkKFkTuKUm5tv1PmH_porkbelly-1470.jpg"),
             Node(id="Jamaican Fish",label="Jamaican Fish",size=nodeSize, svg= "https://thatgirlcookshealthy.com/wp-content/uploads/2018/03/Jamaican-steam-fish.jpg"),
             Node(id="Pickles",label="Pickles",size=nodeSize, svg= "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/18/02/57/picA94k8p.jpg")])


edges.extend([Edge(source="Spicy Potatoes",label ="spicy food", target="Spicy Chicken"),
              Edge(source="Jamaican Fish",label ="spicy food", target="Spicy Chicken"),
              Edge(source="Jamaican Fish",label ="spicy food", target="Spicy Potatoes"),
              Edge(source="Jamaican Fish", label="meats", target="Spicy Chicken"),
              Edge(source="Spicy Chicken", label="meats", target="Pork Belly"),
              Edge(source="Jamaican Fish", label="meats", target="Pork Belly"),
              Edge(source="Pickles", label="non-meats", target="Spicy Potatoes"),
              ])

def app():
  st.title("Related Recipes")

  sidebar = st.sidebar
  middle, rsidebar = st.beta_columns([3,1])
  sidebar.title("Choose meal type and ingredients")

  display_category = sidebar.selectbox("Cuisine Type: ",index=0, options = ["all","spicy food","meats","non-meats"]) # could add more stuff here later on or add other endpoints in the sidebar.
  mealType = sidebar.selectbox("Meal Type: ", index=0, options = ["Breakfast", "Lunch", "Dinner"]) # Just a place holder could be 'soup', 'salad', or 'italian', 'indian', etc
  userInput = sidebar.text_input("Input ingredients to search for: ", "potatoes, tomatoes")

  config = Config(height=300,
                  width=700,
                  nodeHighlightBehavior=True,
                  highlightColor="#F7A7A6",
                  directed=True,
                  collapsible=True,
                  node={'labelProperty': 'label'},
                  link={'labelProperty': 'label', 'renderLabel': True}
                  )


  if display_category=="all":
      viewEdges = edges
  else:
      viewEdges = [edge for edge in edges if edge.label==display_category]

  with middle:
      st.text("Displaying {} cuisine types".format(display_category))
      return_value = agraph(nodes=nodes,
                      edges=viewEdges,
                      config=config)



  #data_load_state = st.text("Loading Data...")

  with rsidebar:
      st.subheader("Selected recipe")
      st.image("https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/37/21/1/picdx8xbY.jpg")
      #st.write(testDf)

  #st.subheader("Graphing the Data")
  #st.bar_chart(testDf)

  #checkBox = st.checkbox("Label",value=True,key="on")

  #if checkBox == True:
      #st.subheader("Displaying text because checkbox is true")

  st.text("User selected the following ingredients: "+userInput)

if __name__=='__main__':
    app()
