from flask import Flask, request,render_template
from get_weather import get_weather


# Flaskアプリを作成
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


# クリックされた都道府県名に応じて、気象庁の天気予報データを取得する
@app.route("/weather")
def weather():
    area = request.args.get("area")

    if area is not None:
        area_name,three_days_weather,weekly_weather = get_weather(area)
        return render_template("result.html", area_name=area_name, three_days_weather=three_days_weather, weekly_weather=weekly_weather)
    
    else:
        return "未対応の地域です。", 404




# アプリを起動
if __name__=="__main__":
    app.run(debug=True)