import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "search", "search_movie", "search_actor", "search_series", "movie_result", "actor_result", "series_result", "chose_list", "popular_movies", "movie_details", "popular_actor", "actor_details", "popular_series", "series_details"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "chose_list",
            "conditions": "is_going_to_chose_list",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "search",
            "conditions": "is_going_to_search",
        },
        {
            "trigger": "advance",
            "source": "chose_list",
            "dest": "popular_movies",
            "conditions": "is_going_to_popular_movies",
        },
        {
            "trigger": "advance",
            "source": "popular_movies",
            "dest": "movie_details",
            "conditions": "is_going_to_movie_details",
        },
        {
            "trigger": "advance",
            "source": "chose_list",
            "dest": "popular_actor",
            "conditions": "is_going_to_popular_actor",
        },
        {
            "trigger": "advance",
            "source": "popular_actor",
            "dest": "actor_details",
            "conditions": "is_going_to_actor_details",
        },
        {
            "trigger": "advance",
            "source": "chose_list",
            "dest": "popular_series",
            "conditions": "is_going_to_popular_series",
        },
        {
            "trigger": "advance",
            "source": "popular_series",
            "dest": "series_details",
            "conditions": "is_going_to_series_details",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "search_movie",
            "conditions": "is_going_to_search_movie",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "search_actor",
            "conditions": "is_going_to_search_actor",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "search_series",
            "conditions": "is_going_to_search_series",
        },
        {
            "trigger": "advance",
            "source": "search_movie",
            "dest": "movie_result",
            "conditions": "is_going_to_movie_result",
        },
        {
            "trigger": "advance",
            "source": "search_actor",
            "dest": "actor_result",
            "conditions": "is_going_to_actor_result",
        },
        {
            "trigger": "advance",
            "source": "search_series",
            "dest": "series_result",
            "conditions": "is_going_to_series_result",
        },
        {
            "trigger": "advance",
            "source": "movie_result",
            "dest": "movie_details",
            "conditions": "is_going_to_movie_details",
        },
        {
            "trigger": "advance",
            "source": "series_result",
            "dest": "series_details",
            "conditions": "is_going_to_series_details",
        },
        {
            "trigger": "advance",
            "source": "movie_details",
            "dest": "movie_details",
            "conditions": "is_going_to_movie_details",
        },
        {
            "trigger": "advance",
            "source": "actor_result",
            "dest": "actor_details",
            "conditions": "is_going_to_actor_details",
        },
        {
            "trigger": "advance",
            "source": "actor_details",
            "dest": "actor_details",
            "conditions": "is_going_to_actor_details",
        },
        {
            "trigger": "advance",
            "source": "series_details",
            "dest": "series_details",
            "conditions": "is_going_to_series_details",
        },
        {
            "trigger": "go_back", 
            "source": ["chose_list", "popular_movies", "movie_details", "popular_actor", "actor_details", "popular_series", "series_details", "search", "search_movie", "search_actor", "search_series", "movie_result", "actor_result", "series_result"], 
            "dest": "user",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        if machine.state != "user" and event.message.text.lower() == 'menu':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage('歡迎回到主頁面!\n\n輸入 [搜尋] 即可進入搜尋模式，尋找自己喜愛的電影、影集或演員!\n\n輸入 [熱門清單] 即可查看今日Top4的熱門電影、影集或演員!\n\n輸入menu即可隨時回到主頁面!')
            )
            machine.go_back()
        else:
            response = machine.advance(event)
            if response == False:
                if machine.state == "user":
                    send_text_message(event.reply_token, "請輸入 [搜尋] 即可進入搜尋模式，尋找自己喜愛的電影、影集或演員!\n或是輸入 [熱門清單] 即可查看今日Top4的熱門電影、影集或演員!")
                elif machine.state == "chose_list" or machine.state == "search" or machine.state == "movie_result" or machine.state == "actor_result" or machine.state == "series_result" or machine.state == "popular_movies" or machine.state == "popular_series" or machine.state == "popular_actor":
                    send_text_message(event.reply_token, "請乖乖按按鈕!")
                elif machine.state == "search_movie" or machine.state == "search_actor" or machine.state == "search_series":
                    send_text_message(event.reply_token, "抱歉，我找不到你要的資料QQ，請你重新輸入一次!")
                elif machine.state == "actor_details" or machine.state == "movie_details" or machine.state == "series_details":
                    send_text_message(event.reply_token, "可以查看其他搜尋結果，或是輸入menu就可以回到主選單囉!")
                
                

    return "OK"


@app.route("/show-fsm", methods=["POST"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
