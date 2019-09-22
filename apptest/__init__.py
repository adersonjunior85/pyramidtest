from pyramid.config import Configurator

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from pymongo import MongoClient


def main(global_config, **settings):
    config = Configurator(settings=settings)

    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
       host=db_url.hostname,
       port=db_url.port,
    )
    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db
    config.add_request_method(add_db, 'db', reify=True)

    config.include('pyramid_chameleon')

    config.add_route('home', '/')
    config.add_route('video', '/video')
    config.add_route('video_json', '/video.json')
    config.add_route('create', '/create')
    config.add_route('trending', '/trending')

    config.add_static_view(name='assets', path='apptest:assets')

    config.scan('.views')
    return config.make_wsgi_app()
