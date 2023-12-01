import streamlit as st
import requests
import matplotlib.pyplot as plt

#Start
def main_section():
    st.header("Welcome to the Pokemon Searcher!")
    st.subheader("Search through all 1017 Pokemon using generation and type!")
    st.write("Please use dark theme or some graphs may break!")
    st.write("---")
main_section()

#Inputs
def input_section():
    col1, col2 = st.columns(2)
    genEndpoint = "https://pokeapi.co/api/v2/generation/"
    generation = col1.multiselect( #NEW
        "Which generation(s) would you like to filter by? If no generation is specified, all will be chosen.",
        ["Generation 1",
         "Generation 2",
         "Generation 3",
         "Generation 4",
         "Generation 5",
         "Generation 6",
         "Generation 7",
         "Generation 8",
         "Generation 9"]
        )
    typeEndpoint = "https://pokeapi.co/api/v2/type/"
    typing = col1.radio( #NEW
        "What type would you like to filter by?",
        ["Normal :rice_ball:",
         "Water :droplet:",
         "Fire :fire:",
         "Grass :seedling:",
         "Electric :zap:",
         "Ice :ice_cube:",
         "Poison :biohazard_sign:",
         "Flying :bird:",
         "Ghost :ghost:",
         "Fighting :punch:",
         "Psychic :eye:",
         "Dark :black_circle:",
         "Bug :bug:",
         "Ground :desert:",
         "Rock :mountain:",
         "Steel :robot_face:",
         "Dragon :dragon:",
         "Fairy :fairy:"
                ])
    typing = typing.split()[0].lower()

    colorDict = {"normal":"navajowhite", "water":"dodgerblue", "fire":"orangered", "grass":"seagreen", "electric":"gold", "ice":"paleturquoise", "poison":"purple", "flying":"slateblue", "ghost":"darkslateblue", "fighting":"salmon", "psychic":"fuchsia", "dark":"darkslategray", "bug":"darkseagreen", "ground":"sandybrown", "rock":"sienna", "steel":"gainsboro", "dragon":"darkorchid", "fairy":"thistle"}
    typeColor = colorDict[typing]
    
    data = requests.get(typeEndpoint + typing)
    typeData = data.json()
    typeNum = len(typeData["pokemon"])

    plt.rcParams["text.color"] = "white"
    labels = typing[0].upper() + typing[1:], "Other Pokemon"
    ratio = (typeNum/1017)*100
    sizes = [ratio, 100-ratio]
    fig1, ax1 = plt.subplots()
    fig1.patch.set_alpha(0)

    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', radius=0.4, textprops={'fontsize': 4}, colors=[typeColor, "gray"])
    col2.pyplot(fig1, use_container_width=False) #NEW

    run = col1.button("Run!") #NEW

    col1, col2 = st.columns(2)
    
    if run: 
        col2.subheader("Fun data!")
        with st.spinner("Please wait..."): #NEW
            if not generation:
                generation = "123456789"
            for gen in generation:
                gen = gen[-1]
                col1.subheader("Generation " + gen)
                data = requests.get(genEndpoint + gen)
                genData = data.json()
                monList = genData["pokemon_species"]
                numMon = int(len(monList))
                numType = 0
                for mon in monList:
                    monId = mon["url"][42:-1]
                    data = requests.get("https://pokeapi.co/api/v2/pokemon/" + monId)
                    monData = data.json()
                    typeList = monData["types"]
                    for typeDict in typeList:
                        if typing in typeDict["type"].values():
                            numType += 1
                            monName = mon["name"][0].upper() + mon["name"][1:]
                            col1.write(f"{monName} [more info](https://bulbapedia.bulbagarden.net/wiki/{monName}_(Pokémon))")
                ratio = (numType/numMon)*100
                labels = "Number of Type", "Rest of Pokemon in Generation"
                sizes = [ratio, 100-ratio]
                explode = (0.1, 0)
                plt.rcParams["text.color"] = "white"

                fig, ax = plt.subplots(figsize=(5,1))
                fig.patch.set_alpha(0)
                ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', radius=1, textprops={'fontsize': 5}, colors=[typeColor, "gray"])
                col2.write(f"Percent of specified type in Generation {gen}:")
    
                col2.pyplot(fig, use_container_width=False)
        col1.success("Done searching!") #NEW
        
input_section()

