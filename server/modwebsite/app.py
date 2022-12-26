import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart
from quart_cors import cors

from modwebsite import auth, analytics
from modwebsite.books import books_blueprint
from modwebsite.config.configuration_reader import config
from modwebsite.config.database import database
from modwebsite.config.discord_instance import DiscordInstance
from modwebsite.config.reddit_instance import RedditInstance


def create(test_config=None):
    logging.basicConfig(
        level=logging.INFO,
        format='[%(name)s]: %(message)s'
    )

    app = Quart(__name__, static_folder='../../client/dist/spa', template_folder='../../client/dist/spa')
    app.modwebsite_config = config(app.env)

    app = cors(app,
               allow_origin=app.modwebsite_config['server']['allow_origin'],
               allow_credentials=app.modwebsite_config['server']['allow_credentials'])

    app.secret_key = app.modwebsite_config['server']['flask_secret_key'].encode()
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = app.modwebsite_config['server']['allow_insecure_transport_for_oauth']

    database(app)
    RedditInstance(app)
    DiscordInstance(app)

    @app.before_serving
    async def register_scheduler():
        scheduler_timezone = {}
        scheduler = AsyncIOScheduler(**scheduler_timezone)
        scheduler.start()
        app.scheduler = scheduler
        logging.getLogger('apscheduler').setLevel(logging.WARN)

    app.register_blueprint(auth.discord_bp)
    app.register_blueprint(books_blueprint)
    app.register_blueprint(analytics.mod_activity_bp)

    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    async def catch_all(path):
        print(f"fetching {path}")
        return await app.send_static_file(path)

    return app


app = create()


def run() -> None:
    app.run()
