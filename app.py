import json
import uuid
import os
import time
from pathlib import Path
import datetime as dt
from datetime import datetime, timedelta
from flask import Flask, request, send_from_directory, render_template, jsonify
from collections import defaultdict, deque
import threading

app = Flask(__name__)
secret_key = str(uuid.uuid4())
log_initial_text = f"[INFO] Logging Started"
ip_request_log = defaultdict(lambda: deque())
ip_404_log = defaultdict(lambda: deque())
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

def build_route_str(request_obj, issue_location=None):
    headers = dict(request_obj.headers)
    hostname = request.host.split(':')[0]
    path = request_obj.path

    remote_addr = request_obj.remote_addr
    x_forwarded_for = headers.get("X-Forwarded-For", None)

    isProxy = False if x_forwarded_for == None else True
    if isProxy:
        if issue_location == None:
            return f"{x_forwarded_for} -> {remote_addr} -> {hostname}{path}"
        
        elif issue_location == "remote":
            return f"[{x_forwarded_for}] -> {remote_addr} -> {hostname}{path}"
        
        elif issue_location == "proxy":
            return f"{x_forwarded_for} -> [{remote_addr}] -> {hostname}{path}"
        
        elif issue_location == "hostname":
            return f"{x_forwarded_for} -> {remote_addr} -> [{hostname}{path}]"
        
    else:
        if issue_location == None:
            return f"{remote_addr} -> NO PROXY -> {hostname}{path}"
        
        elif issue_location == "remote":
            return f"[{remote_addr}] -> NO PROXY -> {hostname}{path}"
        
        elif issue_location == "proxy":
            return f"{remote_addr} -> [NO PROXY] -> {hostname}{path}"
        
        elif issue_location == "hostname":
            return f"{remote_addr} -> NO PROXY -> [{hostname}{path}]"

@app.before_request
def rate_limit():
    now = datetime.now(dt.timezone.utc)
    headers = dict(request.headers)
    host = request.host.split(':')[0]

    user_ip = headers.get("X-Forwarded-For", request.remote_addr)
    current_time = str(datetime.now(dt.timezone.utc))

    ip_queue = ip_request_log[user_ip]
    while ip_queue and (now - ip_queue[0]).total_seconds() > 60:
        ip_queue.popleft()
    ip_queue.append(now)

    count = len(ip_queue)
    if count >= 45:
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('error.html', enumber="403", ename=f"You are in naughty list: {request.remote_addr}"), 403

    if user_ip in ip_block_info:
        if now < ip_block_info[user_ip]:
            seconds_left = int((ip_block_info[user_ip] - now).total_seconds())
            route_str = build_route_str(request, "remote")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="429", ename=f"You are blocked for {seconds_left}s"), 429
        else:
            del ip_block_info[user_ip]
    
    if count >= 44:
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('final_warning.html'), 429
    elif count >= 40:
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('error.html', enumber="429", ename="You are blocked for 3600s"), 429
    elif count >= 35:
        ip_block_info[user_ip] = now + timedelta(hours=1)
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('error.html', enumber="429", ename="You are blocked for 3600s"), 429
    elif count >= 30:
        ip_block_info[user_ip] = now + timedelta(minutes=30)
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('error.html', enumber="429", ename="You are blocked for 1800s"), 429
    elif count >= 25:
        ip_block_info[user_ip] = now + timedelta(minutes=15)
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('error.html', enumber="429", ename="You are blocked for 900s"), 429
    elif count >= 20:
        ip_block_info[user_ip] = now + timedelta(minutes=1)
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY | {current_time} {route_str}")
        return render_template('error.html', enumber="429", ename="You are blocked for 60s"), 429

    if os.path.isfile("./data/blacklist.json"):
        with open("./data/blacklist.json", 'r', encoding='utf-8') as f:
            blacklist: list = json.load(f)
            f.close()
        
        with open("./data/domains.json", 'r', encoding='utf-8') as f:
            domains: list = json.load(f)
            f.close()

        x_forwarded_for = headers.get("X-Forwarded-For", None)
        isProxy = False if x_forwarded_for == None else True
        isOfficialDomain = any(host.endswith(allowed) for allowed in domains)

        if (isProxy) and "PROXY" in blacklist:
            route_str = build_route_str(request, "proxy")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="403", ename=f"Proxies are prohibited on this server"), 403
        elif (not isProxy) and "NOT_PROXY" in blacklist:
            route_str = build_route_str(request, "proxy")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="403", ename=f"This server requires an official proxy"), 403
        
        if (isOfficialDomain) and "OFFICIAL_DOMAIN" in blacklist:
            route_str = build_route_str(request, "hostname")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="403", ename=f"Unofficial domains are prohibited on this server"), 403
        elif (not isOfficialDomain) and "NOT_OFFICIAL_DOMAIN" in blacklist:
            route_str = build_route_str(request, "hostname")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="403", ename=f"This server requires an official domain"), 403

        if request.remote_addr in blacklist:
            route_str = build_route_str(request, "remote")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="403", ename=f"You are in naughty list: {request.remote_addr}"), 403

        if x_forwarded_for in blacklist:
            route_str = build_route_str(request, "proxy")
            log_text(f"[INFO] DENY | {current_time} {route_str}")
            return render_template('error.html', enumber="403", ename=f"You are in naughty list: {x_forwarded_for}"), 403

@app.errorhandler(400)
def four_o_o(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 400 | {current_time} {route_str}")

    return render_template('error.html', enumber="400", ename="Bad Request")

@app.errorhandler(401)
def four_o_one(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 401 | {current_time} {route_str}")

    return render_template('error.html', enumber="401", ename="Unauthorized")

@app.errorhandler(403)
def four_o_two(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 403 | {current_time} {route_str}")

    return render_template('error.html', enumber="403", ename="Forbidden")

@app.errorhandler(404)
def four_o_four(e):
    now = datetime.now(dt.timezone.utc)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip_queue = ip_404_log[ip]

    while ip_queue and (now - ip_queue[0]).total_seconds() > 60:
        ip_queue.popleft()
    ip_queue.append(now)
    
    current_time = str(now)
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 404 | {current_time} {route_str}")

    if len(ip_queue) >= 5:
        add_to_blacklist(ip)
        return render_template('error.html', enumber="403", ename="You are now in the naughty list"), 403

    elif len(ip_queue) >= 4:
        return render_template('final_warning.html'), 404

    return render_template('error.html', enumber="404", ename="Not Found")

@app.errorhandler(414)
def four_one_four(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 414 | {current_time} {route_str}")

    return render_template('error.html', enumber="414", ename="URI Too Long")

@app.errorhandler(500)
def five_o_o(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 500 | {current_time} {route_str}")

    return render_template('error.html', enumber="500", ename="Internal Server Error")

@app.errorhandler(503)
def five_o_three(e):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[ERROR] 503 | {current_time} {route_str}")

    return render_template('error.html', enumber="503", ename="Service Unavailable")

def shutdown_later(delay=1):
    time.sleep(delay)
    os._exit(0)

@app.route('/')
def index_page():
    headers = dict(request.headers)
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return render_template('index.html')

@app.route('/error/<path:code>/')
def error_page(code):

    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request, "hostname")
    log_text(f"[WARN] {current_time} {route_str}")

    return render_template('error.html', enumber=code, ename=f"Error Page"), int(code)

@app.route('/api/v1/')
def api_index():
    headers = dict(request.headers)
    pong_data = {
        "code": 0,
        "content": "Pong!"
    }

    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return jsonify(pong_data)

@app.route('/api/v1/stop/<path:key>')
def api_stop(key):
    if secret_key == key:
        threading.Thread(target=shutdown_later).start()
        headers = dict(request.headers)
        
        pong_data = {
            "code": 0,
            "content": "Okay, Stopping Now!"
        }

        current_time = str(datetime.now(dt.timezone.utc))
        route_str = build_route_str(request)
        log_text(f"[INFO] PASS | {current_time} {route_str}")

        return jsonify(pong_data)
    else:
        pong_data = {
            "code": 1,
            "content": "Need Secret Key for This Action"
        }

        current_time = str(datetime.now(dt.timezone.utc))
        route_str = build_route_str(request, "remote")
        log_text(f"[INFO] DENY {current_time} {route_str}")

        return jsonify(pong_data)

@app.route('/icons/<path:filename>')
def icon_return(filename):
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return send_from_directory('static/icons', filename)

@app.route('/favicon.ico')
def favicon_return():
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return send_from_directory('static/favicon', "favicon.ico")

@app.route('/zeta/')
def zeta_index_page():
    headers = dict(request.headers)
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return render_template('zeta-index.html')

@app.route('/burners/')
def burners_page():
    headers = dict(request.headers)
    current_time = str(datetime.now(dt.timezone.utc))
    route_str = build_route_str(request)
    log_text(f"[INFO] PASS | {current_time} {route_str}")

    return render_template('burners.html')

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