import json
import uuid
import os
import time
from pathlib import Path
import datetime as dt
from datetime import datetime, timedelta
from flask import Flask, request, send_from_directory, render_template, jsonify
import threading

app = Flask(__name__)
secret_key = str(uuid.uuid4())
log_initial_text = f"[INFO] Logging Started"

BLACKLIST_PATH = "./data/blacklist.json"
COUNT_DIR = "./data/counts"

def log_reset(filepath: str = './logs/latest.log'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        f.write(log_initial_text + '\n')

def log_text(content, filepath: str = './logs/latest.log'):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [str(line) + '\n' for line in content] if isinstance(content, list) else [str(content) + '\n']
    with path.open('a', encoding='utf-8') as f:
        f.writelines(lines)
    if content != "":
        print(content)

def load_blacklist():
    if os.path.isfile(BLACKLIST_PATH):
        with open(BLACKLIST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_blacklist(blacklist):
    with open(BLACKLIST_PATH, 'w', encoding='utf-8') as f:
        json.dump(blacklist, f, ensure_ascii=False, indent=4)

def is_blacklisted(ip, now=None):
    now = now or datetime.now(dt.timezone.utc)
    updated_blacklist = []
    still_blacklisted = False

    for entry in load_blacklist():
        if isinstance(entry, str):
            updated_blacklist.append({"ip": entry, "expire": None})
            if entry == ip:
                still_blacklisted = True
        elif entry["ip"] == ip:
            expire_time = entry.get("expire")
            if not expire_time:
                still_blacklisted = True
                updated_blacklist.append(entry)
            else:
                expire_dt = datetime.fromisoformat(expire_time)
                if now < expire_dt:
                    still_blacklisted = True
                    updated_blacklist.append(entry)
        else:
            updated_blacklist.append(entry)

    save_blacklist(updated_blacklist)
    return still_blacklisted

def add_to_blacklist(ip, duration: timedelta = None):
    now = datetime.now(dt.timezone.utc)
    expire = None if duration is None else (now + duration).isoformat()
    new_entry = {"ip": ip, "expire": expire}
    blacklist = load_blacklist()
    for entry in blacklist:
        if (isinstance(entry, str) and entry == ip) or (isinstance(entry, dict) and entry["ip"] == ip):
            return
    blacklist.append(new_entry)
    save_blacklist(blacklist)

def build_route_str(request_obj, issue_location=None):
    headers = dict(request_obj.headers)
    hostname = request.host.split(':')[0]
    path = request_obj.path
    remote_addr = request_obj.remote_addr
    x_forwarded_for = headers.get("X-Forwarded-For", None)
    isProxy = x_forwarded_for is not None

    if isProxy:
        if issue_location == "remote":
            return f"[{x_forwarded_for}] -> {remote_addr} -> {hostname}{path}"
        elif issue_location == "proxy":
            return f"{x_forwarded_for} -> [{remote_addr}] -> {hostname}{path}"
        elif issue_location == "hostname":
            return f"{x_forwarded_for} -> {remote_addr} -> [{hostname}{path}]"
        return f"{x_forwarded_for} -> {remote_addr} -> {hostname}{path}"
    else:
        if issue_location == "remote":
            return f"[{remote_addr}] -> NO PROXY -> {hostname}{path}"
        elif issue_location == "proxy":
            return f"{remote_addr} -> [NO PROXY] -> {hostname}{path}"
        elif issue_location == "hostname":
            return f"{remote_addr} -> NO PROXY -> [{hostname}{path}]"
        return f"{remote_addr} -> NO PROXY -> {hostname}{path}"

@app.before_request
def rate_limit():
    now = datetime.now(dt.timezone.utc)
    headers = dict(request.headers)
    host = request.host.split(':')[0]
    user_ip = headers.get("X-Forwarded-For", request.remote_addr)
    current_time = now.isoformat()

    if is_blacklisted(user_ip, now):
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename=f"You are in naughty list: {user_ip}"), 403

    Path(COUNT_DIR).mkdir(parents=True, exist_ok=True)
    req_file = os.path.join(COUNT_DIR, f"{user_ip}.json")
    if os.path.exists(req_file):
        with open(req_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"timestamps": []}

    data["timestamps"] = [t for t in data["timestamps"]
                          if (now - datetime.fromisoformat(t)).total_seconds() < 60]
    data["timestamps"].append(now.isoformat())
    with open(req_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    count = len(data["timestamps"])

    if count >= 45:
        add_to_blacklist(user_ip)
        return render_template('special/error.html', enumber="403", ename="You are permanently blocked"), 403
    elif count >= 40:
        add_to_blacklist(user_ip, timedelta(hours=1))
        return render_template('special/error.html', enumber="429", ename="Blocked for 1 hour"), 429
    elif count >= 35:
        add_to_blacklist(user_ip, timedelta(minutes=30))
        return render_template('special/error.html', enumber="429", ename="Blocked for 30 minutes"), 429
    elif count >= 30:
        add_to_blacklist(user_ip, timedelta(minutes=15))
        return render_template('special/error.html', enumber="429", ename="Blocked for 15 minutes"), 429
    elif count >= 25:
        add_to_blacklist(user_ip, timedelta(minutes=1))
        return render_template('special/error.html', enumber="429", ename="Blocked for 1 minute"), 429

    blacklist = load_blacklist()
    with open("./data/domains.json", 'r', encoding='utf-8') as f:
        domains = json.load(f)

    x_forwarded_for = headers.get("X-Forwarded-For", None)
    isProxy = x_forwarded_for is not None
    isOfficialDomain = any(host.endswith(allowed) for allowed in domains)

    if isProxy and is_blacklisted("PROXY", now):
        route_str = build_route_str(request, "proxy")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename="Proxies are prohibited on this server"), 403

    elif not isProxy and is_blacklisted("NOT_PROXY", now):
        route_str = build_route_str(request, "proxy")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename="This server requires an official proxy"), 403

    elif isOfficialDomain and is_blacklisted("OFFICIAL_DOMAIN", now):
        route_str = build_route_str(request, "hostname")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename="Official domains are prohibited"), 403

    elif not isOfficialDomain and is_blacklisted("NOT_OFFICIAL_DOMAIN", now):
        route_str = build_route_str(request, "hostname")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename="This server requires an official domain"), 403

    elif is_blacklisted(user_ip, now):
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename=f"You are in naughty list: {user_ip}"), 403

    elif is_blacklisted(x_forwarded_for, now):
        route_str = build_route_str(request, "proxy")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('special/error.html', enumber="403", ename=f"You are in naughty list: {x_forwarded_for}"), 403

@app.errorhandler(400)
def four_o_o(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E400 | {current_time} {route_str}")

    return render_template('special/error.html', enumber="400", ename="Bad Request")

@app.errorhandler(401)
def four_o_one(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E401 | {current_time} {route_str}")

    return render_template('special/error.html', enumber="401", ename="Unauthorized")

@app.errorhandler(403)
def four_o_two(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E403 | {current_time} {route_str}")

    return render_template('special/error.html', enumber="403", ename="Forbidden")

@app.errorhandler(404)
def four_o_four(e):
    now = datetime.now(dt.timezone.utc)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    key = os.path.join(COUNT_DIR, f"404_{ip}.json")
    Path(COUNT_DIR).mkdir(parents=True, exist_ok=True)

    if os.path.exists(key):
        with open(key, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"timestamps": []}

    data["timestamps"] = [t for t in data["timestamps"]
                          if (now - datetime.fromisoformat(t)).total_seconds() < 60]
    data["timestamps"].append(now.isoformat())
    with open(key, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    current_time = now.isoformat()
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E404 | {current_time} {route_str}")

    if len(data["timestamps"]) >= 5:
        add_to_blacklist(ip, timedelta(hours=1))
        return render_template('special/error.html', enumber="403", ename="You are temporarily blacklisted"), 403
    elif len(data["timestamps"]) >= 4:
        return render_template('final_warning.html'), 404
    return render_template('special/error.html', enumber="404", ename="Not Found")

@app.errorhandler(414)
def four_one_four(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E414 | {current_time} {route_str}")

    return render_template('special/error.html', enumber="414", ename="URI Too Long")

@app.errorhandler(500)
def five_o_o(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E500 | {current_time} {route_str}")

    return render_template('special/error.html', enumber="500", ename="Internal Server Error")

@app.errorhandler(503)
def five_o_three(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[INFO] E503 | {current_time} {route_str}")

    return render_template('special/error.html', enumber="503", ename="Service Unavailable")

@app.route('/')
def index_page():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")
    return render_template('index.html')

@app.route('/robots.txt')
def robots_txt():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")
    return send_from_directory('static/for-crowler', "robots.txt")

@app.route('/sitemap.xml')
def sitemap_xml():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")
    return send_from_directory('static/for-crowler', "sitemap.xml")

@app.route('/api/v1/')
def api_index():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")
    return jsonify({"code": 0, "content": "Pong!"})

def shutdown_later(delay=1):
    time.sleep(delay)
    os._exit(0)

@app.route('/api/v1/stop/<path:key>')
def api_stop(key):
    if secret_key == key:
        threading.Thread(target=shutdown_later).start()
        return jsonify({"code": 0, "content": "Okay, Stopping Now!"})
    else:
        return jsonify({"code": 1, "content": "Need Secret Key for This Action"})

@app.route('/favicon.ico')
def favicon_return():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")
    return send_from_directory('static/favicon', "favicon.ico")

@app.route('/icons/<path:filename>')
def icon_return(filename):
    try:
        current_time = str(datetime.now(dt.timezone.utc))
        route_str = build_route_str(request)
        log_text(f"[INFO] PASS | {current_time} {route_str}")

        icon_dir = os.path.join(app.root_path, 'static/icons')
        return send_from_directory(icon_dir, filename)
    
    except Exception as e:
        import traceback
        log_text(f"[ERROR] Failed to serve icon: {filename}")
        log_text(traceback.format_exc())
        return render_template('special/error.html', enumber="500", ename="Internal Server Error"), 500

@app.route('/zeta/')
def zeta_index_page():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return render_template('zeta/index.html')

@app.route('/burners/')
def burners_page():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return render_template('burners/index.html')

@app.route('/burners/img/<path:filename>')
def burners_img(filename):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return send_from_directory('static/burners', filename)

if __name__ == "__main__":
    public = True
    port = 80
    log_reset()
    host = "0.0.0.0" if public else "localhost"
    try:
        log_text(f"[INFO] Server Started ({host}:{port})")
        log_text(f"[INFO] Secret Key ({secret_key})")
        app.run(host, port)
    except KeyboardInterrupt:
        pass
