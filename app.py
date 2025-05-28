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
from collections import Counter, defaultdict, deque
import argparse
import shutil
import threading
import traceback

app = Flask(__name__)
secret_key = str(uuid.uuid4())
log_initial_text = f"[1ST LINE] Initial Text"
ip_request_log = defaultdict(lambda: deque())
ip_block_info = {}

def log_reset(filepath: str = './logs/latest.log'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        f.write(log_initial_text + '\n')
        f.close()

def log_text(content, filepath: str = './logs/latest.log'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(content, list):
        lines = [str(line) + '\n' for line in content]
    else:
        lines = [str(content) + '\n']

    with path.open('a', encoding='utf-8') as f:
        f.writelines(lines)
        f.close()
    
    if content != "":
        print(content)

def log_access(headers: dict, url, request_obj, date: Optional[datetime] = None, filepath: str = './logs/access.json'):
    if date is None:
        date = datetime.now(dt.timezone.utc)

    path = Path(filepath)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            f.close()
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
        f.close()
    
def log_error(headers, error_str: str, error_e, url, request_obj, date: Optional[datetime] = None, filepath: str = './logs/error.json'):
    if date is None:
        date = datetime.now(dt.timezone.utc)

    path = Path(filepath)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            f.close()
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
        f.close()

def access_logs_to_pages(filepath="./logs/access.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    url_counter = Counter()

    for entry in data.values():
        url = entry.get("url")
        if url:
            url_counter[url] += 1

    return dict(url_counter)

def access_logs_to_referers(filepath="./logs/access.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        f.close()

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
            f.close()
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
        f.close()

def get_analytics(filepath="./data/analytics.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()
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
        with open("./data/blacklist.json", 'r', encoding='utf-8') as f:
            blacklist: list = json.load(f)
            f.close()
    else:
        blacklist = []
    new_blacklist = blacklist
    new_blacklist.append(ip)
    with open('./data/blacklist.json', 'w', encoding='utf-8') as f:
        json.dump(new_blacklist, f, ensure_ascii=False, indent=4)
        f.close()

@app.before_request
def limit_host_header():
    now = datetime.now(dt.timezone.utc)
    headers = dict(request.headers)

    ip = headers.get("X-Forwarded-For", request.remote_addr)

    ip_queue = ip_request_log[ip]
    while ip_queue and (now - ip_queue[0]).total_seconds() > 60:
        ip_queue.popleft()
    ip_queue.append(now)

    count = len(ip_queue)
    if count >= 101:
        log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow}(FOUND IN BLACKLIST) {request.remote_addr} -> {host}{request.full_path}")
        return render_template('error.html', enumber="403", ename=f"You are in naughty list: {request.remote_addr}"), 403

    if ip in ip_block_info:
        if now < ip_block_info[ip]:
            seconds_left = int((ip_block_info[ip] - now).total_seconds())
            log_text(f"[BLOCKED ACTIVE] {ip} still blocked for {seconds_left}s")
            return render_template('error.html', enumber="429", ename=f"You are blocked for {seconds_left}s"), 429
        else:
            del ip_block_info[ip]
    
    if count >= 80:
        add_to_blacklist(ip)
        log_text(f"[BLOCKED] IP {ip} exceeded 100 req/min -> Blacklisted")
        return render_template('error.html', enumber="429", ename="You are added to naughty list"), 429
    elif count >= 70:
        ip_block_info[ip] = now + timedelta(hours=1)
        log_text(f"[BLOCKED] IP {ip} blocked for 1 hour (>=80 req/min)")
        return render_template('error.html', enumber="429", ename="You are blocked for 3600s"), 429
    elif count >= 60:
        ip_block_info[ip] = now + timedelta(minutes=10)
        log_text(f"[BLOCKED] IP {ip} blocked for 10 minutes (>=60 req/min)")
        return render_template('error.html', enumber="429", ename="You are blocked for 600s"), 429
    elif count >= 50:
        ip_block_info[ip] = now + timedelta(minutes=5)
        log_text(f"[BLOCKED] IP {ip} blocked for 5 minutes (>=40 req/min)")
        return render_template('error.html', enumber="429", ename="You are blocked for 300s"), 429
    elif count >= 40:
        ip_block_info[ip] = now + timedelta(seconds=30)
        log_text(f"[BLOCKED] IP {ip} blocked for 30 seconds (>=20 req/min)")
        return render_template('error.html', enumber="429", ename="You are blocked for 30s"), 429

    host = request.host.split(':')[0]
    if os.path.isfile("./data/blacklist.json"):
        with open("./data/blacklist.json", 'r', encoding='utf-8') as f:
            blacklist: list = json.load(f)
            f.close()
        
        with open("./data/domains.json", 'r', encoding='utf-8') as f:
            domains: list = json.load(f)
            f.close()

        current_time = str(datetime.now(dt.timezone.utc))
        x_forwarded_for = headers.get("X-Forwarded-For", None)
        isProxy = False if x_forwarded_for == None else True

        x_forwarded_for_arrow = "" if isProxy else f"{x_forwarded_for} -> "
        x_forwarded_for_arrow_blocked = "" if isProxy else f"[{x_forwarded_for}] -> "

        if (isProxy) and "PROXY" in blacklist:
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow} [{request.remote_addr}] -> {host}{request.full_path}")
            return render_template('error.html', enumber="403", ename=f"Proxies are prohibited on this server."), 403
        elif (not isProxy) and "NOT_PROXY" in blacklist:
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow} [{request.remote_addr}] -> {host}{request.full_path}")
            return render_template('error.html', enumber="403", ename=f"This server requires an official proxy."), 403

        if request.remote_addr in blacklist:
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow} [{request.remote_addr}] -> {host}{request.full_path}")
            return render_template('error.html', enumber="403", ename=f"You are in naughty list: {request.remote_addr}"), 403

        elif x_forwarded_for in blacklist:
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow_blocked}{request.remote_addr} -> {host}{request.full_path}")
            return render_template('error.html', enumber="403", ename=f"You are in naughty list: {x_forwarded_for}"), 403

        elif (not any(host.endswith(allowed) for allowed in domains)) and ("NOT_OFFICIAL_DOMAIN" in blacklist):
            log_text(f"[BLOCKED] {current_time} {x_forwarded_for_arrow}{request.remote_addr} -> [{host}{request.full_path}]")
            return render_template('error.html', enumber="403", ename=f"This URL does not appear to be official."), 403
        
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

@app.route('/error/<path:code>/')
def error_page(code):
    return render_template('error.html', enumber=code, ename=f"Error Page (/error/{code}/)")

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