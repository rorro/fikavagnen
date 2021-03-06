from flask import Flask, request, jsonify, render_template
import dbhelper
import constants
from commands import metric_to_emoji, is_meetup
import datetime

KEY = '/etc/letsencrypt/live/bestapi.nu/privkey.pem'
CRT = '/etc/letsencrypt/live/bestapi.nu/fullchain.pem'

app = Flask(__name__)

@app.route("/fikavagn", methods=['GET'])
def serve_fikavagn():
    return render_template("index.html")

@app.route("/fikavagnen", methods=['GET'])
def serve_inner_fika():
    temp = dbhelper.get_total_data()

    f = open('fikatimeteller', 'r')
    message = f.readline().rstrip()
    f.close()

    total_data = {}
    for metric, score in temp:
        total_data[metric_to_emoji(metric)] = str(score)

    top_tens = {}
    for metric in constants.METRICS:
        top = dbhelper.get_top10(metric)

        emoji_metric = metric_to_emoji(metric)
        top_ten_this_metric = []
        for user, score in top:
            top_ten_this_metric.append([str(user), str(score)])
        top_tens[emoji_metric] = top_ten_this_metric

    return render_template("fika_serving.html", totals=total_data, top=top_tens, fikadags=message)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=False, host="192.168.1.161", port=443, ssl_context=(CRT, KEY))
