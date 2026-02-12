# 天気予報アプリ（Flask）

## 概要

気象庁の天気予報APIを使用して、選択した都道府県の天気情報を表示するWebアプリです。

## 機能

* 都道府県を選択して天気を表示
* 3日間の天気予報
* 週間天気
* 雨雲の動き（URL表示）

## 使用技術

* Python
* Flask
* HTML / CSS

## 起動方法

### 1. 必要なライブラリをインストール
```bash
pip install -r requirements.txt
```

### 2. アプリを起動
```bash
uv run app.py
```

### 3. ブラウザでアクセス

アプリ起動後、以下のURLにアクセスしてください。

http://127.0.0.1:5000

## フォルダ構成
```
weather-app/
├─ app.py
├─ get_weather.py
├─ weather_mapping.py
├─ README.md
├─ requirements.txt
├─ templates/
│   └─ index.html
│   └─ result.html
└─ static/
    └─ style.css
    └─ icons/
        ├─ sunny.png
        ├─ rainy.png
        └─ ...
```

