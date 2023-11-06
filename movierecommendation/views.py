import os
import pandas as pd
from django.shortcuts import render
import pickle
from dotenv import load_dotenv
import requests

from movierecom.settings import BASE_DIR
# Create your views here.

load_dotenv()

def your_view(request):
    csv_file_path = os.path.join(BASE_DIR, 'movierecommendation/static/data.csv')
    selected_movie = request.GET.get('movie_select', '')
    data = pd.read_csv(csv_file_path)
    


    try:
        titles = data['title']

        if selected_movie:
            movie_list, movie_poster = recommend(selected_movie)                
        else:
            movie_list = []
            movie_poster = []
        context = {
            'titles' : titles,
            'movie_list' : movie_list,
            'movie_poster' : movie_poster
        }

    except FileNotFoundError:
        titles = "Error"

    return render(request, 'template.html',context)

def recommend(movie):
    csv_file_path = os.path.join(BASE_DIR, 'movierecommendation/static/data.csv')
    simialrity_path = os.path.join(BASE_DIR, 'movierecommendation/static/similarity.pkl')
    data = pd.read_csv(csv_file_path)
    similarity = pickle.load(open(simialrity_path, 'rb'))

    movie_index = data[data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:6]

    recommendation = []
    movie_posters = []
    for i in movies_list:
        movie_id = data.iloc[i[0]].movie_id


        recommendation.append(data.iloc[i[0]].title)
        movie_posters.append(fetch_poster(movie_id))

    return recommendation, movie_posters

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('API_KEY')}")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] 
