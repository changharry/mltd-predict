import json

from flask import render_template

from app import app


@app.route('/')
def index():
    with open('data/data.json') as f:
        data = json.load(f)
        if data["meta"]["type"] == 4:
            return render_template('anniversary.html')
        else:
            reg = data["regression"]
            meta = data["meta"]
            return render_template('default.html', para=[reg, meta, len(reg)])


@app.route('/idol/<idol_id>')
def idol(idol_id):
    with open('data/data.json') as f:
        data = json.load(f)
        if data["meta"]["type"] == 5:
            reg = data["regression_all"][int(idol_id) - 1]
            meta = data["meta"]
            return render_template('idol.html', para=[idol_index[int(idol_id) - 1], reg, len(reg), meta])
        else:
            return "null"


idol_index = ["天海 春香", "如月 千早", "星井 美希", "萩原 雪歩", "高槻 やよい",
              "菊地 真", "水瀬 伊織", "四条 貴音", "秋月 律子", "三浦 あずさ",
              "双海 亜美", "双海 真美", "我那覇 響", "春日 未来", "最上 静香",
              "伊吹 翼", "田中 琴葉", "島原 エレナ", "佐竹 美奈子", "所 恵美",
              "徳川 まつり", "箱崎 星梨花", "野々原 茜", "望月 杏奈", "ロコ",
              "七尾 百合子", "高山 紗代子", "松田 亜利沙", "高坂 海美", "中谷 育",
              "天空橋 朋花", "エミリー", "北沢 志保", "舞浜 歩", "木下 ひなた",
              "矢吹 可奈", "横山 奈緒", "二階堂 千鶴", '馬場 このみ', "大神 環",
              "豊川 風花", "宮尾 美也", "福田 のり子", "真壁 瑞希", "篠宮 可憐",
              "百瀬 莉緒", "永吉 昴", "北上 麗花", "周防 桃子", "ジュリア",
              "白石 紬", "桜守 歌織"]
