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

def create_from_id(request):

    if request.method == 'POST':

        show_id = request.POST.get('show_id','')

        try:

            show_info = get_netflix_show_data(str(show_id))
            title = show_info[0]
            num_of_seasons = show_info[1]
            series = Series(name=title,netflix_id=show_id,seasons_total=num_of_seasons)
            series.save()

        except:

            print('could not find show by that id')
            return redirect('home')

        create_seasons(series, num_of_seasons)


        ep_json = get_netflix_episodes(str(show_id))

        for episode in ep_json:

            try:
                ep = get_netflix_ep_data(episode)

                name = ep[2]
                episodeNum = int(ep[1])
                season_num = ep[0]
                netflixID = ep[3]
                year = ep[4]
                runtime = int(ep[5])
                ep_season = Season.objects.get(series=series, season_number=season_num)

                episode = Video(name=name,
                    episodeNum=episodeNum,
                    season=ep_season,
                    media_type="T",
                    netflix_id=netflixID,
                    year=year,
                    runtime=runtime)

                episode.save()

            except:

                print (episode)

        return redirect('home')


    return (request, 'forms/create_from_id.html')


def create_series(request):

    if request.method == 'POST':

        name = request.POST.get('series_name','')

        try:

            showData = get_all_data(name)
            netflixId = showData['show_id']
            series = Series(name=name, netflix_id=netflixId)
            series.save()

        except:

            showData = None
            print ("Could not find Netflix ID")
            return redirect('home')


        wiki_search = 'List of %s episodes' % (series.name)

        wiki_raw_results = json.dumps(wikipedia.search(wiki_search))

        wiki_results = json.loads(wiki_raw_results)


        for result in wiki_results:

            if result == wiki_search:

                wiki_url = wikipedia.page(result).url

                series.wikipedia_url = wiki_url

                series.save()

                span_list= get_season_list(wiki_url)

                for item in span_list:

                    name = 'Season ' + str(item[0])

                    season = Season(name=name, series=series, season_number=item[0])

                    season.save()

                series.seasons_total = len(span_list)

                series.save()

                return redirect('find_add_episodes', series_id=series.id)

        return redirect('select_show_name',series_id=series.id)

    return render(request, 'forms/create_series.html')


def select_show_name(request,series_id):

    series = Series.objects.get(pk=series_id)

    in_put = 'List of %s' % (series.name)

    results = wikipedia.search(in_put)

    if request.method == 'POST':

        name = request.POST.get('ep_select','')

        wiki_page = wikipedia.page(name)

        wiki_url = wiki_page.url

        series.wikipedia_url = wiki_url

        series.save()

        span_list= get_season_list(wiki_url)

        for item in span_list:

            name = 'Season ' + str(item[0])

            season = Season(name=name, series=series, season_number=item[0])

            season.save()

        series.seasons_total = len(span_list)


        return redirect('find_add_episodes',series_id=series.id)

    else:

        return render(request, 'forms/select_show_name.html', {
        'results': results,
        })


def find_add_episodes(request, series_id):

    try:

        series = Series.objects.get(pk=series_id)

        ep_json_list = get_netflix_episodes(series.netflix_id)

        for episode in ep_json_list:

            try:
                ep = get_netflix_ep_data(episode)

                name = ep[2]
                episodeNum = int(ep[1])
                season_num = ep[0]
                netflixID = ep[3]
                year = ep[4]
                runtime = int(ep[5])
                ep_season = Season.objects.get(series=series, season_number=season_num)

                episode = Video(name=name,
                    episodeNum=episodeNum,
                    season=ep_season,
                    media_type="T",
                    netflix_id=netflixID,
                    year=year,
                    runtime=runtime)

                episode.save()

            except:

                print (episode)

        return redirect('home')

    except:

        print('cound not add episodes')

    return render(request, 'index.html')


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


    return render(request, 'season/view_season.html',{
        'series' : series,
        'season' : season,
        'channels' : channels,
    })


def view_series(request, series_id):

    series = Series.objects.get(pk=series_id)
    channels = Channel.objects.all()


    return render(request, 'series/view_series.html',{
        'series' : series,
    })

def create_movie(request):

    if request.method == 'POST':

        value = request.POST.get('movie_add_value','')
        search_type = request.POST.get('movie_search_by')

        if search_type == 'movie_name':

            try:

                show_info = get_all_data(str(value))
                netflixId = show_info['show_id']
                movie = video(name=value, netflix_id=netflixId,media_type="M")
                series.save()

                print(show_info)

            except:

                print('could not add movie by id')

            return redirect('home')


        elif search_type == 'movie_id':

            try:
                show_info = get_netflix_show_data(str(value))
                title = show_info[0]
                show_id = str(value)

                movie = Video(name=title,netflix_id=show_id,media_type="M")

                movie.save()

            except:

                print('could not add movie by id')

            return redirect('home')

        return redirect('home')

    return render(request,'create_movie.html')


def index(request):
    channels = Channel.objects.all()
    seriess = Series.objects.all().order_by('name')
    movies = Video.objects.filter(media_type='M')
    return render(request, 'index.html',{
        'channels' : channels,
        'seriess' : seriess,
        'movies' : movies,
    })
