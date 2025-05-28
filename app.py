import json
import uuid
import os
import sys
import time
from pathlib import Path
import datetime as dt
from datetime import datetime, timedelta
from flask import Flask, request, abort, send_from_directory, render_template, jsonify
from markupsafe import escape
from typing import Optional
from countrys import Countrys
from collections import Counter
import argparse
import shutil
import threading

app = Flask(__name__)
secret_key = str(uuid.uuid4())
log_initial_text = f"[1ST LINE] Initial Text"

def log_reset(filepath: str = './logs/latest.log'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        f.write(log_initial_text + '\n')

def log_text(content, filepath: str = './logs/latest.log'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(content, list):
        lines = [str(line) + '\n' for line in content]
    else:
        lines = [str(content) + '\n']

    with path.open('a', encoding='utf-8') as f:
        f.writelines(lines)
    
    if content != "":
        print(content)

def log_access(headers: dict, url, request_obj, date: Optional[datetime] = None, filepath: str = './logs/access.json'):
    if date is None:
        date = datetime.now(dt.timezone.utc)

    path = Path(filepath)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    cf_ray = headers.get("Cf-Ray")
    if not cf_ray:
        cf_ray = str(uuid.uuid4())

    iso_datetime = date.isoformat()

    analytics = get_analytics()
    access_number = analytics["totalCount"]

    new_entry = {
        "id": headers.get("Cf-Ray"),
        "ip": request_obj.remote_addr,
        "number": access_number,
        "datetime": iso_datetime,
        "url": url,
        "headers": headers
    }

    data[cf_ray] = new_entry

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
def log_error(headers, error_str: str, error_e, url, request_obj, date: Optional[datetime] = None, filepath: str = './logs/error.json'):
    if date is None:
        date = datetime.now(dt.timezone.utc)

    path = Path(filepath)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    reqid = str(uuid.uuid4())

    iso_datetime = date.isoformat()

    analytics = get_analytics()
    access_number = analytics["totalCount"]

    new_entry = {
        "id": headers.get("Cf-Ray"),
        "ip": request_obj.remote_addr,
        "number": access_number,
        "error": str(error_e),
        "code": error_str,
        "url": url,
        "datetime": iso_datetime,
        "header": headers,
    }

    data[reqid] = new_entry

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def access_logs_to_pages(filepath="./logs/access.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    url_counter = Counter()

    for entry in data.values():
        url = entry.get("url")
        if url:
            url_counter[url] += 1

    return dict(url_counter)

def access_logs_to_referers(filepath="./logs/access.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    referer_counter = Counter()
    
    for entry in data.values():
        headers = entry.get("headers", {})
        referer = headers.get("Referer")
        if referer:
            referer_counter[referer] += 1

    return dict(referer_counter)

def update_analytics(country: str = "XX", date: str = None, amount: int = 1, filepath: str = './data/analytics.json'):
    if date is None:
        now = datetime.now(dt.timezone.utc)
        rounded = now.replace(minute=0, second=0, microsecond=0)
        date_str = rounded.strftime("%Y-%m-%d %H:00")
    else:
        now = datetime.strptime(date, "%Y-%m-%d %H:%M")
        date_str = now.strftime("%Y-%m-%d %H:00")

    path = Path(filepath)
    if path.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            "counter-total": 0,
            "counter": {},
            "country-total": {},
            "country": {}
        }

    data["counter-total"] = data.get("counter-total", 0) + amount
    data["counter"][date_str] = data["counter"].get(date_str, 0) + amount
    data["country-total"][country] = data["country-total"].get(country, 0) + amount

    if date_str not in data["country"]:
        data["country"][date_str] = {}
    data["country"][date_str][country] = data["country"][date_str].get(country, 0) + amount

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_analytics(filepath="./data/analytics.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "totalCount": 0,
            "monthlyCount": 0,
            "weeklyCount": 0,
            "dailyCount": 0,
            "counter-total": 0,
            "counter": {},
            "country-total": {},
            "country": {}
        }

    now = datetime.now(dt.timezone.utc)

    total_count = data.get("counter-total", 0)
    daily_data = data.get("counter", {})

    monthly_count = 0
    weekly_count = 0
    daily_count = 0

    for timestamp_str, count in daily_data.items():
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:00").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue

        if timestamp.date() == now.date():
            daily_count += count
        if timestamp >= now - timedelta(days=7):
            weekly_count += count
        if timestamp.year == now.year and timestamp.month == now.month:
            monthly_count += count

    return {
        "totalCount": total_count,
        "monthlyCount": monthly_count,
        "weeklyCount": weekly_count,
        "dailyCount": daily_count,
        "counter-total": data.get("counter-total", 0),
        "counter": data.get("counter", {}),
        "country-total": data.get("country-total", {}),
        "country": data.get("country", {})
    }

def add_to_blacklist(ip):
    if os.path.isfile("./data/blacklist.json"):
        with open("./data/blacklist.json", 'r', encoding='utf-8') as file:
            blacklist: list = json.load(file)
    else:
        blacklist = []
    new_blacklist = blacklist
    new_blacklist.append(ip)
    with open('./data/blacklist.json', 'w', encoding='utf-8') as f:
        json.dump(new_blacklist, f, ensure_ascii=False, indent=4)

@app.before_request
def limit_host_header():
    host = request.host.split(':')[0]
    headers = dict(request.headers)
    if os.path.isfile("./data/blacklist.json"):
        with open("./data/blacklist.json", 'r', encoding='utf-8') as file:
            blacklist: list = json.load(file)
        with open("./data/domains.json", 'r', encoding='utf-8') as file:
            domains: list = json.load(file)
        current_time = str(datetime.now(dt.timezone.utc))
        x_forwarded_for = headers.get("X-Forwarded-For", "NOT_PROXY")
        x_forwarded_for_arrow = (f"{x_forwarded_for} -> " if x_forwarded_for != "NOT_PROXY" else "")

        if request.remote_addr in blacklist:
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow}(FOUND IN BLACKLIST) {request.remote_addr} -> {host}{request.full_path}")
            return render_template('error.html', enumber="403", ename=f"Found in Blacklist: {request.remote_addr}"), 403

        elif x_forwarded_for in blacklist:
            log_text(f"[BLOCKED] {current_time} (FOUND IN BLACKLIST) {x_forwarded_for_arrow}{request.remote_addr} -> {host}{request.full_path}")
            return render_template('error.html', enumber="403", ename=f"Found in Blacklist: {x_forwarded_for}"), 403

        elif (not any(host.endswith(allowed) for allowed in domains)) and ("NOT_OFFICIAL_DOMAIN" in blacklist):
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow}{request.remote_addr} -> (FOUND IN BLACKLIST) {host}{request.full_path}")
            log_error(headers, "NOT_OFFICIAL_DOMAIN", "Special Error: NOT_OFFICIAL_DOMAIN", request.url, request)

            if x_forwarded_for == "NOT_PROXY":
                add_to_blacklist(request.remote_addr)
                log_text(f"[BLACKLIST] Added to Blacklist: {request.remote_addr}")
            else:
                add_to_blacklist(x_forwarded_for)
                log_text(f"[BLACKLIST] Added to Blacklist: {x_forwarded_for}")

            return render_template('error.html', enumber="403", ename=f"ERROR ID: NOT_OFFICIAL_DOMAIN"), 403
        
        else:
            log_text(f"[PASSED] {current_time} {x_forwarded_for_arrow}{request.remote_addr} -> {host}{request.full_path}")

@app.errorhandler(400)
def four_o_o(e):
    headers = dict(request.headers)
    log_error(headers, "400 Bad Request", e, request.url, request)
    return render_template('error.html', enumber="400", ename="Bad Request")

@app.errorhandler(401)
def four_o_one(e):
    headers = dict(request.headers)
    log_error(headers, "401 Unauthorized", e, request.url, request)
    return render_template('error.html', enumber="401", ename="Unauthorized")

@app.errorhandler(403)
def four_o_two(e):
    headers = dict(request.headers)
    log_error(headers, "403 Forbidden", e, request.url, request)
    return render_template('error.html', enumber="403", ename="Forbidden")

@app.errorhandler(404)
def four_o_four(e):
    headers = dict(request.headers)
    log_error(headers, "404 Not Found", e, request.url, request)
    return render_template('error.html', enumber="404", ename="Not Found")

@app.errorhandler(414)
def four_one_four(e):
    headers = dict(request.headers)
    log_error(headers, "414 URI Too Long", e, request.url, request)
    return render_template('error.html', enumber="414", ename="URI Too Long")

@app.errorhandler(500)
def five_o_o(e):
    headers = dict(request.headers)
    log_error(headers, "500 Internal Server Error", e, request.url, request)
    return render_template('error.html', enumber="500", ename="Internal Server Error")

@app.errorhandler(503)
def five_o_three(e):
    headers = dict(request.headers)
    log_error(headers, "503 Service Unavailable", e, request.url, request)
    return render_template('error.html', enumber="503", ename="Service Unavailable")

def shutdown_later(delay=1):
    time.sleep(delay)
    os._exit(0)

@app.route('/')
def index_page():
    headers = dict(request.headers)
    if "Cf-Ipcountry" in headers.keys():
        update_analytics(country=headers["Cf-Ipcountry"])
    else:
        update_analytics()
    log_access(headers, request.url, request)
    analytics = get_analytics()
    return render_template('index.html', accessNo=str(analytics["totalCount"]))

@app.route('/api/v1/')
def api_index():
    headers = dict(request.headers)
    log_access(headers, request.url, request)
    analytics = get_analytics()
    access_number = analytics["totalCount"]
    pong_data = {
        "code": 0,
        "content": "Pong!"
    }
    return jsonify(pong_data)

@app.route('/api/v1/stop/<path:key>')
def api_stop(key):
    if secret_key == key:
        threading.Thread(target=shutdown_later).start()
        headers = dict(request.headers)
        log_access(headers, request.url, request)
        pong_data = {
            "code": 0,
            "content": "Okay, Stopping Now!"
        }
        return jsonify(pong_data)
    else:
        pong_data = {
            "code": 1,
            "content": "Need Secret Key for This Action"
        }
        return jsonify(pong_data)

@app.route('/icons/<path:filename>')
def icon_return(filename):
    return send_from_directory('static/icons', filename)

@app.route('/favicon.ico')
def favicon_return():
    return send_from_directory('static/favicon', "favicon.ico")

@app.route('/zeta/')
def zeta_index_page():
    headers = dict(request.headers)
    if "Cf-Ipcountry" in headers.keys():
        update_analytics(country=headers["Cf-Ipcountry"])
    else:
        update_analytics()
    log_access(headers, request.url, request)
    return render_template('zeta-index.html')

@app.route('/burners/')
def burners_page():
    headers = dict(request.headers)
    if "Cf-Ipcountry" in headers.keys():
        update_analytics(country=headers["Cf-Ipcountry"])
    else:
        update_analytics()
    log_access(headers, request.url, request)
    return render_template('burners.html')

@app.route('/burners/img/<path:filename>')
def burners_img(filename):
    return send_from_directory('static/burners', filename)

@app.route('/analytics/')
def analytics_page():
    headers = dict(request.headers)
    log_access(headers, request.url, request)
    analytics = get_analytics()

    today = datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    today_labels = []
    today_counts = []
    got_country_total: dict = analytics["country-total"]
    new_country_total = {}
    for country in got_country_total.keys():
        if country in Countrys.keys():
            country_id = country
            country_name = Countrys[country_id]
        else:
            country_id = "XX"
            country_name = Countrys[country_id]
        new_country_total[country_id] = [country_name, got_country_total[country]]

    new_country_total = dict(sorted(new_country_total.items(), key=lambda item: item[1][1], reverse=True))

    for timestamp_str, count in analytics["counter"].items():
        if timestamp_str.startswith(today):
            today_labels.append(timestamp_str)
            today_counts.append(count)

    pages = access_logs_to_pages()
    referers = access_logs_to_referers()

    pages = dict(sorted(pages.items(), key=lambda item: item[1], reverse=True))
    referers = dict(sorted(referers.items(), key=lambda item: item[1], reverse=True))

    return render_template(
            'analytics.html',

            dailyLabels=list(analytics["counter"].keys()),
            dailyCounts=list(analytics["counter"].values()),
            todayLabels=today_labels,
            todayCounts=today_counts,

            totalCount=str(analytics["totalCount"]),
            monthlyCount=str(analytics["monthlyCount"]),
            weeklyCount=str(analytics["weeklyCount"]),
            dailyCount=str(analytics["dailyCount"]),

            countryTotal=new_country_total,

            pages=pages,
            referers=referers
        )

if __name__ == "__main__":
    if os.path.isfile("./logs/latest.log"):
        log_uuid = str(uuid.uuid4())
        shutil.copy2("./logs/latest.log", f"./logs/archives/{log_uuid}.log")
    log_reset()
    
    try:
        log_text("[START] Web Server has Started!")
        log_text(f"[SECRET KEY] Secret Key: {secret_key}")
        app.run("0.0.0.0", 80)
    except KeyboardInterrupt:
        pass
