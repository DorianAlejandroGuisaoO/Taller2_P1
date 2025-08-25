import pandas as pd
import json
import os

if not os.path.exists('movies_initial.csv'):
    print("El archivo movies_initial.csv no existe en la carpeta actual.")
else:
    df = pd.read_csv('movies_initial.csv')
    df.to_json('movies.json', orient='records')
    print("Archivo movies.json creado")

    with open('movies.json', 'r') as file:
        movies = json.load(file)

    for i in range(100):
        movie = movies[i]
        print(movie)
        break