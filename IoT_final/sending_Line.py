import requests

def sending(message):
    # LINE Notify 權杖
    token = 'YOVvCxxm1zlCP3dr3zTEl0brQTTFgFcfRi4oaHBR0MV'

    # 要發送的訊息

    # HTTP 標頭參數與資料
    headers = { "Authorization": "Bearer " + token }
    data = { 'message': message }

    # 以 requests 發送 POST 請求
    requests.post("https://notify-api.line.me/api/notify",
        headers = headers, data = data)
    return