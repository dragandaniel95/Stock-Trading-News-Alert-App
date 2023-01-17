import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_KEY = "11AZ2XVGAKOTIOBK"
NEWS_KEY = "a8d98dcf97b94e00867b67151717aefb"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_params = {
    "function": "TIME_SERIES_WEEKLY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Weekly Time Series"]
data_list = [value for (key, value) in data.items()]
last_week_closing_price = float(data_list[0]["4. close"])
last_2weeks_closing_price = float(data_list[1]["4. close"])

difference = round(last_week_closing_price - last_2weeks_closing_price, 1)
absolute_difference = abs(difference)

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((absolute_difference / last_2weeks_closing_price) * 100, 1)

if diff_percent > 5:
    news_params = {
        "qInTitle": f"{COMPANY_NAME}&",
        "apiKey": NEWS_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    first_3_art = news_data[:3]
    formated_articles = [f"Headline:{article['title']}. \nBrief:{article['description']}" for article in first_3_art]
    account_sid = "AC07309b3dd56eead2c2b286fa0865eace"
    auth_token = "c539b944bf49ca1b399870e5ce3efa0e"
    client = Client(account_sid, auth_token)
    for article in formated_articles:
        message = client.messages.create(
            body=f"{COMPANY_NAME}:{up_down} {difference}% \n{article}",
            from_='+1 223 217 8563',
            to='+40728046203'
        )




