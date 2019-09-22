from bson import ObjectId, json_util
import json
from random import randint

from pyramid.view import (
    view_config,
    view_defaults
    )

# HomePage view, get all videos new to old.
@view_config(route_name='home', renderer='home.pt')
def home(request):
    try:
        videos = request.db.video.find().sort('_id', -1)
        return {'videos': videos}
    except Exception as e:
        print(e)
        return {'videos': []}


@view_config(route_name='video', renderer='video.pt')
@view_config(route_name='video_json', renderer='json')
def video(request):
    id = request.params['id']
    try:
        video = request.db.video.find_one({"_id": ObjectId(id)})

        if('type' in request.params and request.method == 'POST'):
            like = True if int(request.params['type']) == 1 else False
            if(like):
                video['likes'] += 1
                request.db.video.update_one({"_id": ObjectId(id)}, {"$set": {"likes": video['likes'], "highscore": video['likes']-(video['dislikes']/2)}})
            else:
                video['dislikes'] += 1
                request.db.video.update_one({"_id": ObjectId(id)}, {"$set": {"dislikes": video['dislikes'], "highscore": video['likes']-(video['dislikes']/2)}})
            return {'video': json.loads(json_util.dumps(video))}
        else:
            return {'video': video}
    except Exception as e:
        print(e)
        return {}

@view_config(route_name='trending', renderer='trending.pt')
def trending(request):
    try:
        pipeline = [
            {"$unwind": "$theme"},
            {"$group": {"_id": "$theme", "total_likes": {"$sum": "$likes"}, "total_dislikes": {"$sum": "$dislikes"}}}
        ]
        themes = request.db.video.aggregate(pipeline)

        scoredThemes = []
        themeScore = 0
            
        for theme in themes:
            likes = theme['total_likes']
            dislikes = theme['total_dislikes']
            themeScore = likes - (dislikes/2)
            scoredThemes.append({
                'name': theme['_id'],
                'score': themeScore,
                'total_likes': likes,
                'total_dislikes': dislikes
            })

        scoredThemes = sorted(scoredThemes, key=lambda x: x['score'], reverse=True)
        return {'themes': scoredThemes}

    except Exception as e:
        print(e)
        return {'themes': []}

@view_config(route_name='create', renderer='create.pt')
def create(request):

    inserting = False
    error = False
    themes = []

    if(request.method == 'POST'):
        name = request.params['name'] or 'Nameless Video ID:%d' %(randint(1, 999))
        src  = request.params['src'] or None
        theme = request.params['theme'] or 'Any'

        if src!=None: src = src.split("watch?v=")[-1]

        inserting = True
        try:
            request.db.video.insert_one({
                'name': name,
                'likes': 0,
                'dislikes': 0,
                'src_id': src,
                'theme': theme,
                'highscore': 0.0
            })
        except Exception as e:
            print(e)
            error = True
    else:
        try:
            themes = request.db.video.find().distinct('theme')
        except Exception as e:
            print(e)

    return {'themes': themes, 'error': error, 'inserting': inserting}
