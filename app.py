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

    iso_datetime = date.isoformat() + "Z"

    new_entry = {
        "datetime": iso_datetime,
        "headers": headers
    }

    data[cf_ray] = new_entry

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def log_error(error_str: str, date: Optional[datetime] = None, filepath: str = './logs/error.json'):
    if date is None:
        date = datetime.now(dt.timezone.utc)

    path = Path(filepath)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    reqid = str(uuid.uuid4())

    iso_datetime = date.isoformat() + "Z"

    new_entry = {
        "error": error_str,
        "datetime": iso_datetime
    }

    data[reqid] = new_entry

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_analytics(country: str = "XX", date: str = None, amount: int = 1, filepath: str = './data/analytics.json'):
    if date is None:
        now = datetime.now(dt.timezone.utc)
        date = now.isoformat(timespec='seconds') + "Z"
    else:
        now = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

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
    data["counter"][date] = data["counter"].get(date, 0) + amount
    data["country-total"][country] = data["country-total"].get(country, 0) + amount

    if date not in data["country"]:
        data["country"][date] = {}
    data["country"][date][country] = data["country"][date].get(country, 0) + amount

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
            timestamp = timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)

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
    log_error("400 Bad Request")
    return render_template('error.html', enumber="400", ename="Bad Request")

@app.errorhandler(401)
def four_o_one(e):
    log_error("401 Unauthorized")
    return render_template('error.html', enumber="401", ename="Unauthorized")

@app.errorhandler(403)
def four_o_two(e):
    log_error("403 Forbidden")
    return render_template('error.html', enumber="403", ename="Forbidden")

@app.errorhandler(404)
def four_o_four(e):
    log_error("404 Not Found")
    return render_template('error.html', enumber="404", ename="Not Found")

@app.errorhandler(414)
def four_one_four(e):
    log_error("414 URI Too Long")
    return render_template('error.html', enumber="414", ename="URI Too Long")

@app.route('/')
def index_page():
    headers = dict(request.headers)
    log_access(headers)
    if "CF-IPCountry" in headers.keys():
        update_analytics(country=headers["CF-IPCountry"])
    else:
        update_analytics()
    return render_template('index.html')

@app.route('/icons/<path:filename>')
def icon_return(filename):
    return send_from_directory('icons', filename)

@app.route('/zeta/')
def zeta_index_page():
    headers = dict(request.headers)
    log_access(headers)
    if "CF-IPCountry" in headers.keys():
        update_analytics(country=headers["CF-IPCountry"])
    else:
        update_analytics()
    return render_template('zeta-index.html')

@app.route('/analytics/')
def analytics_page():
    headers = dict(request.headers)
    log_access(headers)
    analytics = get_analytics()

    now = datetime.now(dt.timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    daily_counter = {}
    for timestamp_str, count in analytics["counter"].items():
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue

        date_key = timestamp.strftime("%Y-%m-%d")
        daily_counter[date_key] = daily_counter.get(date_key, 0) + count

    sorted_daily_items = sorted(daily_counter.items())
    daily_labels = [item[0] for item in sorted_daily_items]
    daily_counts = [item[1] for item in sorted_daily_items]

    today_labels = [f"{hour:02d}:00" for hour in range(24)]
    today_counts = [0 for _ in range(24)]

    for timestamp_str, count in analytics["counter"].items():
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue

        if timestamp.date() == now.date():
            hour = timestamp.hour
            today_counts[hour] += count

    return render_template(
        'analytics.html',
        dailyLabels=daily_labels,
        dailyCounts=daily_counts,
        todayLabels=today_labels,
        todayCounts=today_counts,
        totalCount=str(analytics["totalCount"]),
        monthlyCount=str(analytics["monthlyCount"]),
        weeklyCount=str(analytics["weeklyCount"]),
        dailyCount=str(analytics["dailyCount"])
    )

countrys = {
    # Normal
    'AF': 'Afghanistan',
    'AX': 'Åland Islands',
    'AL': 'Albania',
    'DZ': 'Algeria',
    'AS': 'American Samoa',
    'AD': 'Andorra',
    'AO': 'Angola',
    'AI': 'Anguilla',
    'AQ': 'Antarctica',
    'AG': 'Antigua and Barbuda',
    'AR': 'Argentina',
    'AM': 'Armenia',
    'AW': 'Aruba',
    'AU': 'Australia',
    'AT': 'Austria',
    'AZ': 'Azerbaijan',
    'BS': 'Bahamas',
    'BH': 'Bahrain',
    'BD': 'Bangladesh',
    'BB': 'Barbados',
    'BY': 'Belarus',
    'BE': 'Belgium',
    'BZ': 'Belize',
    'BJ': 'Benin',
    'BM': 'Bermuda',
    'BT': 'Bhutan',
    'BO': 'Bolivia, Plurinational State of',
    'BQ': 'Bonaire, Sint Eustatius and Saba',
    'BA': 'Bosnia and Herzegovina',
    'BW': 'Botswana',
    'BV': 'Bouvet Island',
    'BR': 'Brazil',
    'IO': 'British Indian Ocean Territory',
    'BN': 'Brunei Darussalam',
    'BG': 'Bulgaria',
    'BF': 'Burkina Faso',
    'BI': 'Burundi',
    'KH': 'Cambodia',
    'CM': 'Cameroon',
    'CA': 'Canada',
    'CV': 'Cape Verde',
    'KY': 'Cayman Islands',
    'CF': 'Central African Republic',
    'TD': 'Chad',
    'CL': 'Chile',
    'CN': 'China',
    'CX': 'Christmas Island',
    'CC': 'Cocos (Keeling) Islands',
    'CO': 'Colombia',
    'KM': 'Comoros',
    'CG': 'Congo',
    'CD': 'Congo, the Democratic Republic of the',
    'CK': 'Cook Islands',
    'CR': 'Costa Rica',
    'CI': 'Côte d\'Ivoire',
    'HR': 'Croatia',
    'CU': 'Cuba',
    'CW': 'Curaçao',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DK': 'Denmark',
    'DJ': 'Djibouti',
    'DM': 'Dominica',
    'DO': 'Dominican Republic',
    'EC': 'Ecuador',
    'EG': 'Egypt',
    'SV': 'El Salvador',
    'GQ': 'Equatorial Guinea',
    'ER': 'Eritrea',
    'EE': 'Estonia',
    'ET': 'Ethiopia',
    'FK': 'Falkland Islands (Malvinas)',
    'FO': 'Faroe Islands',
    'FJ': 'Fiji',
    'FI': 'Finland',
    'FR': 'France',
    'GF': 'French Guiana',
    'PF': 'French Polynesia',
    'TF': 'French Southern Territories',
    'GA': 'Gabon',
    'GM': 'Gambia',
    'GE': 'Georgia',
    'DE': 'Germany',
    'GH': 'Ghana',
    'GI': 'Gibraltar',
    'GR': 'Greece',
    'GL': 'Greenland',
    'GD': 'Grenada',
    'GP': 'Guadeloupe',
    'GU': 'Guam',
    'GT': 'Guatemala',
    'GG': 'Guernsey',
    'GN': 'Guinea',
    'GW': 'Guinea-Bissau',
    'GY': 'Guyana',
    'HT': 'Haiti',
    'HM': 'Heard Island and McDonald Islands',
    'VA': 'Holy See (Vatican City State)',
    'HN': 'Honduras',
    'HK': 'Hong Kong',
    'HU': 'Hungary',
    'IS': 'Iceland',
    'IN': 'India',
    'ID': 'Indonesia',
    'IR': 'Iran, Islamic Republic of',
    'IQ': 'Iraq',
    'IE': 'Ireland',
    'IM': 'Isle of Man',
    'IL': 'Israel',
    'IT': 'Italy',
    'JM': 'Jamaica',
    'JP': 'Japan',
    'JE': 'Jersey',
    'JO': 'Jordan',
    'KZ': 'Kazakhstan',
    'KE': 'Kenya',
    'KI': 'Kiribati',
    'KP': 'Korea, Democratic People\'s Republic of',
    'KR': 'Korea, Republic of',
    'KW': 'Kuwait',
    'KG': 'Kyrgyzstan',
    'LA': 'Lao People\'s Democratic Republic',
    'LV': 'Latvia',
    'LB': 'Lebanon',
    'LS': 'Lesotho',
    'LR': 'Liberia',
    'LY': 'Libya',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'MO': 'Macao',
    'MK': 'Macedonia, the Former Yugoslav Republic of',
    'MG': 'Madagascar',
    'MW': 'Malawi',
    'MY': 'Malaysia',
    'MV': 'Maldives',
    'ML': 'Mali',
    'MT': 'Malta',
    'MH': 'Marshall Islands',
    'MQ': 'Martinique',
    'MR': 'Mauritania',
    'MU': 'Mauritius',
    'YT': 'Mayotte',
    'MX': 'Mexico',
    'FM': 'Micronesia, Federated States of',
    'MD': 'Moldova, Republic of',
    'MC': 'Monaco',
    'MN': 'Mongolia',
    'ME': 'Montenegro',
    'MS': 'Montserrat',
    'MA': 'Morocco',
    'MZ': 'Mozambique',
    'MM': 'Myanmar',
    'NA': 'Namibia',
    'NR': 'Nauru',
    'NP': 'Nepal',
    'NL': 'Netherlands',
    'NC': 'New Caledonia',
    'NZ': 'New Zealand',
    'NI': 'Nicaragua',
    'NE': 'Niger',
    'NG': 'Nigeria',
    'NU': 'Niue',
    'NF': 'Norfolk Island',
    'MP': 'Northern Mariana Islands',
    'NO': 'Norway',
    'OM': 'Oman',
    'PK': 'Pakistan',
    'PW': 'Palau',
    'PS': 'Palestine, State of',
    'PA': 'Panama',
    'PG': 'Papua New Guinea',
    'PY': 'Paraguay',
    'PE': 'Peru',
    'PH': 'Philippines',
    'PN': 'Pitcairn',
    'PL': 'Poland',
    'PT': 'Portugal',
    'PR': 'Puerto Rico',
    'QA': 'Qatar',
    'RE': 'Réunion',
    'RO': 'Romania',
    'RU': 'Russian Federation',
    'RW': 'Rwanda',
    'BL': 'Saint Barthélemy',
    'SH': 'Saint Helena, Ascension and Tristan da Cunha',
    'KN': 'Saint Kitts and Nevis',
    'LC': 'Saint Lucia',
    'MF': 'Saint Martin (French part)',
    'PM': 'Saint Pierre and Miquelon',
    'VC': 'Saint Vincent and the Grenadines',
    'WS': 'Samoa',
    'SM': 'San Marino',
    'ST': 'Sao Tome and Principe',
    'SA': 'Saudi Arabia',
    'SN': 'Senegal',
    'RS': 'Serbia',
    'SC': 'Seychelles',
    'SL': 'Sierra Leone',
    'SG': 'Singapore',
    'SX': 'Sint Maarten (Dutch part)',
    'SK': 'Slovakia',
    'SI': 'Slovenia',
    'SB': 'Solomon Islands',
    'SO': 'Somalia',
    'ZA': 'South Africa',
    'GS': 'South Georgia and the South Sandwich Islands',
    'SS': 'South Sudan',
    'ES': 'Spain',
    'LK': 'Sri Lanka',
    'SD': 'Sudan',
    'SR': 'Suriname',
    'SJ': 'Svalbard and Jan Mayen',
    'SZ': 'Eswatini',
    'SE': 'Sweden',
    'CH': 'Switzerland',
    'SY': 'Syrian Arab Republic',
    'TW': 'Taiwan, Province of China',
    'TJ': 'Tajikistan',
    'TZ': 'Tanzania, United Republic of',
    'TH': 'Thailand',
    'TL': 'Timor-Leste',
    'TG': 'Togo',
    'TK': 'Tokelau',
    'TO': 'Tonga',
    'TT': 'Trinidad and Tobago',
    'TN': 'Tunisia',
    'TR': 'Turkey',
    'TM': 'Turkmenistan',
    'TC': 'Turks and Caicos Islands',
    'TV': 'Tuvalu',
    'UG': 'Uganda',
    'UA': 'Ukraine',
    'AE': 'United Arab Emirates',
    'GB': 'United Kingdom',
    'US': 'United States',
    'UM': 'United States Minor Outlying Islands',
    'UY': 'Uruguay',
    'UZ': 'Uzbekistan',
    'VU': 'Vanuatu',
    'VE': 'Venezuela, Bolivarian Republic of',
    'VN': 'Viet Nam',
    'VG': 'Virgin Islands, British',
    'VI': 'Virgin Islands, U.S.',
    'WF': 'Wallis and Futuna',
    'EH': 'Western Sahara',
    'YE': 'Yemen',
    'ZM': 'Zambia',
    'ZW': 'Zimbabwe',
    # Other
    'T1': 'Tor Network',
    'XX': 'Cannot Recognition',
    '': 'Cannot Recognition',
}

if __name__ == "__main__":
    app.run("0.0.0.0", 80)