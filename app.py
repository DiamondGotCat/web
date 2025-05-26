import json
import uuid
from pathlib import Path
import datetime as dt
from datetime import datetime, timedelta
from flask import Flask, request, send_from_directory
from flask import render_template
from markupsafe import escape
from typing import Optional

app = Flask(__name__)
log_initial_text = "INITIAL LOG - This is 1st Line"

def log_reset(filepath: str = './logs/log.txt'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        f.write(log_initial_text + '\n')

def log_text(content, filepath: str = './logs/log.txt'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(content, list):
        lines = [str(line) + '\n' for line in content]
    else:
        lines = [str(content) + '\n']

    with path.open('a', encoding='utf-8') as f:
        f.writelines(lines)

def log_access(headers: dict, date: Optional[datetime] = None, filepath: str = './logs/access.json'):
    if date is None:
        date = datetime.now(dt.timezone.utc)

    path = Path(filepath)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    cf_ray = headers.get("CF-Ray")
    if not cf_ray:
        cf_ray = str(uuid.uuid4())

    iso_datetime = date.isoformat()

    new_entry = {
        "datetime": iso_datetime,
        "headers": headers
    }

    data[cf_ray] = new_entry

    path.parent.mkdir(parents=True, exist_ok=True)
    log_text("----- NEW ACCESS -----")
    log_text(json.dumps(new_entry, indent=4))
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def log_error(headers, error_str: str, date: Optional[datetime] = None, filepath: str = './logs/error.json'):
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

    new_entry = {
        "error": error_str,
        "datetime": iso_datetime,
        "header": headers,
    }

    data[reqid] = new_entry

    path.parent.mkdir(parents=True, exist_ok=True)
    log_text("----- ACCESS ERROR -----")
    log_text(json.dumps(new_entry, indent=4))
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
        log_text("----- UPDATE DGC-ANALYTICS DATA -----")
        log_text(json.dumps(data, indent=4))
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

@app.errorhandler(400)
def four_o_o(e):
    headers = dict(request.headers)
    log_error(headers, "400 Bad Request")
    return render_template('error.html', enumber="400", ename="Bad Request")

@app.errorhandler(401)
def four_o_one(e):
    headers = dict(request.headers)
    log_error(headers, "401 Unauthorized")
    return render_template('error.html', enumber="401", ename="Unauthorized")

@app.errorhandler(403)
def four_o_two(e):
    headers = dict(request.headers)
    log_error(headers, "403 Forbidden")
    return render_template('error.html', enumber="403", ename="Forbidden")

@app.errorhandler(404)
def four_o_four(e):
    headers = dict(request.headers)
    log_error(headers, "404 Not Found")
    return render_template('error.html', enumber="404", ename="Not Found")

@app.errorhandler(414)
def four_one_four(e):
    headers = dict(request.headers)
    log_error(headers, "414 URI Too Long")
    return render_template('error.html', enumber="414", ename="URI Too Long")

@app.errorhandler(500)
def five_o_o(e):
    headers = dict(request.headers)
    log_error(headers, "500 Internal Server Error")
    return render_template('error.html', enumber="500", ename="Internal Server Error")

@app.errorhandler(503)
def five_o_three(e):
    headers = dict(request.headers)
    log_error(headers, "503 Service Unavailable")
    return render_template('error.html', enumber="503", ename="Service Unavailable")

@app.route('/')
def index_page():
    headers = dict(request.headers)
    log_access(headers)
    if "Cf-Ipcountry" in headers.keys():
        update_analytics(country=headers["Cf-Ipcountry"])
    else:
        update_analytics()
    return render_template('index.html')

@app.route('/icons/<path:filename>')
def icon_return(filename):
    return send_from_directory('static/icons', filename)

@app.route('/favicon.ico')
def favicon_return():
    return send_from_directory('static/favicon', "favicon.ico")

@app.route('/zeta/')
def zeta_index_page():
    headers = dict(request.headers)
    log_access(headers)
    if "Cf-Ipcountry" in headers.keys():
        update_analytics(country=headers["Cf-Ipcountry"])
    else:
        update_analytics()
    return render_template('zeta-index.html')

@app.route('/analytics/')
def analytics_page():
    headers = dict(request.headers)
    log_access(headers)
    analytics = get_analytics()

    today = datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    today_labels = []
    today_counts = []

    for timestamp_str, count in analytics["counter"].items():
        if timestamp_str.startswith(today):
            today_labels.append(timestamp_str)
            today_counts.append(count)

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

            countryTotal=analytics["country-total"]
        )

if __name__ == "__main__":
    log_reset()
    app.run("0.0.0.0", 80)