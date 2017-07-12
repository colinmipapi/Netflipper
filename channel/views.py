from django.shortcuts import render, redirect

# Create your views here.
import simplejson as json
import wikipedia

from channel.backend import *
from channel.models import Channel, Series, Season, Video
from channel.serializers import VideoSerializer, ChannelSerializer
from rest_framework import viewsets

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

def create_channel(request):

    if request.method == 'POST':

        name = request.POST.get('channel_name','')
        user = request.user

        channel = Channel(name=name,user=user)

        channel.save()

        return redirect('home')

    return render(request, 'forms/create_channel.html')

def view_channel(request, channel_id):

    channel = Channel.objects.get(pk=channel_id)

    return render(request, 'channel/view_channel.html', {
        'channel' : channel,
    })

def create_series(request):

    if request.method == 'POST':

        value = request.POST.get('series_add_value','')
        search_type = request.POST.get('series_search_by')

        if search_type == 'series_name':

            try:

                showData = get_all_data(str(value))
                print (showData)
                show_id = showData['show_id']
                summary = showData['summary']
                series = Series(name=value, netflix_id=show_id,description=summary)
                series.save()



            except:

                print ("Could not find Netflix ID by Name")
                return redirect('home')

        elif search_type == 'series_id':

            try:

                show_info = get_netflix_show_data(str(value))
                title = show_info[0]
                summary = show_info[1]
                show_id = value
                series = Series(name=title,netflix_id=show_id)
                series.save()

            except:

                print ("Could not find Netflix ID by ID")
                return redirect('home')

        ep_json = get_netflix_episodes(show_id)


        for episode in ep_json:

            #[episodeTitle, episodeId, episodeNum, episodeDescription, year, runtime, seasonName, seasonNum, seasonId, seasonDescription]

            try:
                ep = get_netflix_ep_data(episode)

                episodeTitle = ep[0]
                episodeId = ep[1]
                episodeNum = int(ep[2])
                episodeDescription = ep[3]
                year = ep[8]
                runtime = int(ep[9])
                seasonName = ep[4]
                seasonNum = ep[5]
                seasonId = ep[6]
                seasonDescription = ep[7]

                try:
                    ep_season = Season.objects.get(series=series, season_number=seasonNum, netflix_id=seasonId)

                except Season.DoesNotExist:

                    ep_season = Season(series=series, name=seasonName, season_number=seasonNum, netflix_id=seasonId,description=seasonDescription)
                    ep_season.save()

                episode = Video(name=episodeTitle,
                    episodeNum=episodeNum,
                    season=ep_season,
                    media_type="T",
                    netflix_id=episodeId,
                    description=episodeDescription,
                    year=year,
                    runtime=runtime)

                episode.save()
            except:
                print('could not add episode')


        return redirect('home')


    return render(request, 'forms/create_series.html')

def view_series(request, series_id):

    series = Series.objects.get(pk=series_id)
    channels = Channel.objects.all()


    return render(request, 'series/view_series.html',{
        'series' : series,
    })

def view_season(request, series_id,season_id):

    season = Season.objects.get(pk=season_id)
    series = Series.objects.get(pk=series_id)
    episodes = Video.objects.filter(season_id=season.id)

    if request.user.is_authenticated :

        channels = Channel.objects.filter(user=request.user)

        if request.method == 'POST':

            channel = request.POST.get('channel_name','')
            channel_info = Channel.objects.get(pk=channel)

            season_add = request.POST.get('season_add','')

            if season_add == 'add':

                for episode in episodes :

                    ep = episode.id

                    ep_obj = Video.objects.get(pk=ep)

                    channel_info.content.add(ep_obj)

            episode_checked = request.POST.getlist('checks[]')

            for ep in episode_checked:

                ep_obj = Video.objects.get(pk=ep)

                channel_info.content.add(ep_obj)

            channel_info.save()

    else:

        channels = None


    return render(request, 'season/view_season.html',{
        'series' : series,
        'season' : season,
        'channels' : channels,
    })

def create_movie(request):

    if request.method == 'POST':

        value = request.POST.get('movie_add_value','')
        search_type = request.POST.get('movie_search_by')

        if search_type == 'movie_name':

            get_id_from_name(str(value))

            try:

                show_info = get_all_data(str(value))
                netflixId = show_info['show_id']
                movie = Video(name=value, netflix_id=netflixId,media_type="M")
                movie.save()

                print(show_info)

            except:

                print('could not add movie by id')

            return redirect('home')


        elif search_type == 'movie_id':

            try:
                show_info = get_netflix_show_data(str(value))
                title = show_info[0]
                show_id = str(value)
                synopsis = show_info[1]

                movie = Video(name=title,netflix_id=show_id,media_type="M",description=synopsis)

                movie.save()

            except:

                print('could not add movie by id')

            return redirect('home')

        return redirect('home')

    return render(request,'forms/create_movie.html')

def index(request):
    channels = Channel.objects.all()
    seriess = Series.objects.all().order_by('name')
    movies = Video.objects.filter(media_type='M')
    return render(request, 'index.html',{
        'channels' : channels,
        'seriess' : seriess,
        'movies' : movies,
    })
