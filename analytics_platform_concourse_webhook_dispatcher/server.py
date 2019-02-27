import hmac
import asyncio
import aiohttp

from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json
from fly import Fly

from analytics_platform_concourse_webhook_dispatcher.config import Config
from analytics_platform_concourse_webhook_dispatcher import events
from .signature import make_digest

app = Sanic()
app.config.from_object(Config)

fly_lock = asyncio.Lock()


@app.listener("before_server_start")
async def aiohttp_setup(app, loop):
    # setup the session
    timeout = aiohttp.ClientTimeout(total=10)
    session = aiohttp.ClientSession(loop=loop, timeout=timeout)
    app.http = session


@app.listener("after_server_stop")
async def aiohttp_teardown(app, loop):
    await app.http.close()


async def dispatch(event: str, body: dict):
    """
    trigger the corresponding webhook in concourse and return 204
    """

    # try the default by seeing if event
    # is DEFAULT_EVENT and triggering a webhook on DEFAULT_TEAM
    route = events.get(app, event, body)
    if not route:
        return json({}, status=404)

    concourse_url = app.config.CONCOURSE_BASE_URL

    run_args = [
        "check-resource",
        "--resource", f"{route['pipeline']}/{route['resource']}"
    ]

    fly = Fly(
        concourse_url=concourse_url
    )
    with fly_lock:
        fly.get_fly()

    fly.login(
        app.config.CONCOURSE_USERNAME,
        app.config.CONCOURSE_PASSWORD,
        route["team"]
    )

    await asyncio.ensure_future(fly.run(*run_args))

    return json(route, status=204)


@app.middleware("request")
async def validateHook(request):
    secret = app.config.get("SECRET")

    if request.method == "POST":
        digest = make_digest(bytes(secret, encoding="utf8"), request.body)
        hook_signature = request.headers.get("x-hub-signature", "")
        match = hmac.compare_digest(digest, hook_signature)

        if not match:
            abort(400, "Invalid signature")


@app.route("/")
async def home(request):
    return json({})


@app.route("/", methods=["POST"])
@app.route("/<path:path>", methods=["POST"])
async def hook(request, path=None):
    event = request.headers.get("X-GitHub-Event", "ping")
    print(request)
    if event == "ping":
        return json({"msg": "pong"})
    else:
        return await dispatch(event, request.json)


def serve(routes=None):
    if routes:
        app.config.ROUTES_FILE = routes

    app.run(host="0.0.0.0", port=app.config.PORT, debug=app.config.DEBUG)
    loop = asyncio.get_event_loop()
    if not loop.is_closed():
        pending = asyncio.Task.all_tasks()
        loop.run_until_complete(asyncio.gather(*pending))


if __name__ == "__main__":
    serve()
