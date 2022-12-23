import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, title, instro, labels, texts, img):
    line_bot_api = LineBotApi(channel_access_token)

    acts = []
    for i, lab in enumerate(labels):
        acts.append(
            MessageTemplateAction(
                label=lab,
                text=texts[i]
            )
        )

    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url=img,
            title=title,
            text=instro,
            actions=acts
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_movie_details(reply_token, title, overview, release_date, score, img):
    line_bot_api = LineBotApi(channel_access_token)
    arr = []
    arr.append(TextSendMessage(text=title))
    arr.append(TextSendMessage(text=release_date))
    arr.append(TextSendMessage(text=score))
    arr.append(TextSendMessage(text=overview))
    arr.append(ImageSendMessage(original_content_url=img, preview_image_url=img))
    line_bot_api.reply_message(reply_token, arr)

def send_actor_details(reply_token, name, overview, popularity, img):
    line_bot_api = LineBotApi(channel_access_token)
    arr = []
    arr.append(TextSendMessage(text=name))
    arr.append(TextSendMessage(text=popularity))
    arr.append(TextSendMessage(text=overview))
    arr.append(ImageSendMessage(original_content_url=img, preview_image_url=img))
    line_bot_api.reply_message(reply_token, arr)

def send_series_details(reply_token, name, overview, score, episode, img):
    line_bot_api = LineBotApi(channel_access_token)
    arr = []
    arr.append(TextSendMessage(text=name))
    arr.append(TextSendMessage(text=score))
    arr.append(TextSendMessage(text=episode))
    arr.append(TextSendMessage(text=overview))
    arr.append(ImageSendMessage(original_content_url=img, preview_image_url=img))
    line_bot_api.reply_message(reply_token, arr)


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
