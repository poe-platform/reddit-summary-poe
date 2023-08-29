import os

from fastapi_poe import make_app
from modal import Image, Secret, Stub, asgi_app

from reddit_summary_bot import RedditSummaryBot

image = Image.debian_slim().pip_install_from_requirements("requirements.txt")
stub = Stub("reddit-summary-app")


@stub.function(image=image, secret=Secret.from_name("reddit-summary-secret"))
@asgi_app()
def fastapi_app():
    bot = RedditSummaryBot(
        reddit_client_id=os.environ["REDDIT_CLIENT_ID"],
        reddit_client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    )
    app = make_app(bot, access_key=os.environ["POE_ACCESS_KEY"])
    return app
