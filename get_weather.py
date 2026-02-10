import requests
from datetime import datetime
from weather_mapping import WEATHER_MAP,WEATHER_ICON,WEATHER_NORMALIZE

def get_weather(area):


    # 引数で受け取った地域名から天気API用の地域コードを取得する
    pref_numbers = {"東京":"130000", "大阪":"270000", "愛知":"230000"}
    area_num = pref_numbers[area]


    # 気象庁の天気予報APIクリックした地域のURLを取得
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_num}.json"
    # URLにHTTPリクエストを送り、返ってきたJSONデータを取得する
    data = requests.get(url).json()


    #取得した天気情報から地域名は取得
    if area == "東京":
        area_name = data[0]["timeSeries"][2]["areas"][0]["area"]["name"]
    else:
        area = data[1]["timeSeries"][0]["areas"][0]["area"]["name"]
        area_name = area.replace("都","").replace("府","").replace("県","")


    #３日間最高・最低気温の内容を一覧で取得
    three_day_temps = data[0]["timeSeries"][2]["areas"][0]["temps"]

    # 最高・最低気温を取得するときにデータ数が時間帯で変わるため、エラー回避するためにif文で条件で取得する内容を変更
    if len(three_day_temps) == 4: 
        tomorrow_tempMax = data[0]["timeSeries"][2]["areas"][0]["temps"][3]
        tomorrow_tempMin = data[0]["timeSeries"][2]["areas"][0]["temps"][2]
    else:
        tomorrow_tempMax = data[0]["timeSeries"][2]["areas"][0]["temps"][1]
        tomorrow_tempMin = data[0]["timeSeries"][2]["areas"][0]["temps"][0]

    #３日間の最高・最低気温をリストごとに分ける
    three_day_temps[0] = "-"
    three_day_tempsMax = []
    three_day_tempsMin = []
    for i in range(len(three_day_temps)):
        if i == 0 or i == 2:
            three_day_tempsMin.append(three_day_temps[i])
        else:
            three_day_tempsMax.append(three_day_temps[i])



    #３日間の日付を取得
    WPEEKDAYS_JP = ["月", "火", "水", "木", "金", "土", "日"]
    three_day_dates = []

    for d in data[0]["timeSeries"][0]["timeDefines"]:
        if "T00:00:00+09:00" in d:
            three_day_dates.append(d.replace("T00:00:00+09:00", ""))
        elif "T11:00:00+09:00" in d:
            three_day_dates.append(d.replace("T11:00:00+09:00", ""))
        elif "T17:00:00+09:00" in d:
            three_day_dates.append(d.replace("T17:00:00+09:00", ""))
        else:
            three_day_dates.append(d)

    #取得した３日間の日付を曜日に変更してリストに追加
    three_day_list = [
        WPEEKDAYS_JP[datetime.strptime(data, "%Y-%m-%d").weekday()]
        for data in three_day_dates 
    ]

    # ３日間の天気コードを取得し、WEATHER_MAPから対応する天気情報を取得してリストに追加する（該当しない場合は天気不明）
    three_day_weather_codes = data[0]["timeSeries"][0]["areas"][0]["weatherCodes"]
    three_day_weather = [WEATHER_MAP.get(weather, "天気不明") for weather in three_day_weather_codes]

    # 天気表現を正規化して画像取得用の天気リストを作成
    three_day_weather_icon = [WEATHER_MAP.get(weather, "天気不明") for weather in three_day_weather_codes]
    image_three_day_weather_conditions = [WEATHER_NORMALIZE.get(icon_name, icon_name) for icon_name in three_day_weather_icon]

    # 画像取得用の天気リストから画像名を取得（未定義は unknown.png）
    image_three_day_weather = [WEATHER_ICON.get(icon_name, "unknown.png") for icon_name in image_three_day_weather_conditions]





    #週間の日付の天気情報を取得

    #週間の日付を取得
    week_dates = [
        d.replace("T00:00:00+09:00", "")
        for d in data[1]["timeSeries"][0]["timeDefines"]
    ]
 
    
    #取得した日付を曜日に変更してリストに追加
    weekdaysList = [
        WPEEKDAYS_JP[datetime.strptime(data, "%Y-%m-%d").weekday()]
        for data in week_dates 
    ]


    # 天気コードを取得し、WEATHER_MAPから対応する天気情報を取得してリストに追加する（該当しない場合は天気不明）
    week_weather_codes = data[1]["timeSeries"][0]["areas"][0]["weatherCodes"]
    week_weather = [WEATHER_MAP.get(weather, "天気不明") for weather in week_weather_codes]


    # 天気表現を正規化して画像取得用の天気リストを作成
    week_weather_icon = [WEATHER_MAP.get(weather, "天気不明") for weather in week_weather_codes]
    image_week_weather_conditions = [WEATHER_NORMALIZE.get(icon_name, icon_name) for icon_name in week_weather_icon]
    # 画像取得用の天気リストから画像名を取得（未定義は unknown.png）
    image_week_weather = [WEATHER_ICON.get(icon_name, "unknown.png") for icon_name in image_week_weather_conditions]


    #週間の最低・最高気温を取得
    week_tempsMax = [tempMax for tempMax in data[1]["timeSeries"][1]["areas"][0]["tempsMax"] if tempMax != '']
    week_tempsMin = [tempMin for tempMin in data[1]["timeSeries"][1]["areas"][0]["tempsMin"] if tempMin != '']


    #明日の最高・最低気温をリストに追加
    week_tempsMax.insert(0, tomorrow_tempMax)
    week_tempsMin.insert(0, tomorrow_tempMin)

    #明後日の最高・最低気温がないため週間の気温から取得
    three_day_tempsMax.append(week_tempsMax[1])
    three_day_tempsMin.append(week_tempsMin[1])

    #画面に表示しやすいようにデータをまとめる
    three_days_weather = [
        {"day": day, "date": date, "weather": weather,"image":image, "tempMax":tempMax, "tempMin":tempMin}
        for day, date, weather,image, tempMax, tempMin in zip(three_day_list, three_day_dates, three_day_weather,image_three_day_weather,three_day_tempsMax,three_day_tempsMin)
    ]


    weekly_weather = [
        {"day": day, "date": date, "weather": weather,"image":image, "tempMax":tempMax, "tempMin":tempMin}
        for day, date, weather,image, tempMax, tempMin in zip(weekdaysList, week_dates, week_weather,image_week_weather,week_tempsMax,week_tempsMin)
    ]

    
    return area_name,three_days_weather,weekly_weather

if __name__ == "__main__":
    get_weather()