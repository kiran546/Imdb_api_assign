from django.shortcuts import render
import imdb
import requests
from django.http import HttpResponse, Http404
import json
from rest_framework.response import Response
from django.conf import settings


from django.conf import settings

from rest_framework.response import Response

from django.shortcuts import render, redirect



# Create your views here.


def movie_search(request):
    context = {}
    if request.method == 'POST':
        try:
            url = settings.RAPID_API_BASE_URL + \
                f"?s={ request.POST['search'] }&page=1&r=json"
            name = request.POST['search']
            print(request.POST['search'])
            print(url)

            headers = {
                'x-rapidapi-key': settings.X_RAPIDAPI_KEY,
                'x-rapidapi-host': settings.X_RAPIDAPI_HOST_NAME,
                'useQueryString': 'true',
                'Content-Type': 'application/json'
            }

            payload = json.dumps({
                "upload_date": "",
                "read": "True"
            })

            response = requests.request("GET", url, headers=headers, data=payload)

            print(type(response.json()), response.json())  # json

            context = {
                'movie_data': response.json()['Search']
            }
        except Exception as e:
            return render(request, "Error.html")

    return render(request, 'index.html', context)


def get_trailer(request):

    imdb = request.GET.get('imdb', -1)

    title = request.GET.get('title', -1)

    context = {}

    print(type(title), title, type(imdb), imdb)

    trailerUrl = ""

    try:

        params = {

            'part': "snippet",

            'q': title + " official trailer",

            'key':  "AIzaSyCRjI5KKaZwFTXI9OQXfN5gaaOOR_fHkTg"
        }

        result = requests.get(settings.YOUTUBE_API_BASE_URL, params=params)

        data = result.json()
        print(data,'data')

        trailerUrl = settings.YOUTUBE_BASE_URL + result.json()['items'][0]['id']['videoId']

    except Exception as e:

        print("Trailer does not exist")

    try:

        url = "https://movies-tvshows-data-imdb.p.rapidapi.com/"

        querystring = {"type": "get-movie-details", "imdb": imdb}

        headers = {

            'x-rapidapi-key': '35185625ffmshae485834fdadb9ap1948bajsn1bbdee7db0ae',

            'x-rapidapi-host': 'movies-tvshows-data-imdb.p.rapidapi.com',
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.json())
    except Exception as e:

        print("oops not found")

        return render(request, 'Error.html')
    print(trailerUrl,"hello")

    context = {

        'trailerUrl': trailerUrl,
        'movieDetails': response.json(),
        'title': title
    }
    print(trailerUrl,'comment')

    return render(request, 'trailer.html', context)
