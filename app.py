from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector
import json
import pprint
import socket


app = Flask(__name__)
def get_domain_ip(url):
    try:
        domain = url.split("//")[-1].split("/")[0]  # Extract domain from URL
        ip_address = socket.gethostbyname(domain)  # Get IP address for the domain
        return ip_address
    except socket.gaierror:
        return 'Error resolving IP'
# Scoring rules for security headers
header_scores = {
    "Strict-Transport-Security": 10,
    "Content-Security-Policy": 8,
    "X-Content-Type-Options": 6,
    "X-Frame-Options": 5,
    "X-XSS-Protection": 5,
    "Referrer-Policy": 5,
    "Permissions-Policy": 4,
    "Cache-Control": 6,
    "Expect-CT": 7,
    "Public-Key-Pins": 6,  # Deprecated, but still included for backward compatibility
    "Cross-Origin-Resource-Policy": 6,
    "Feature-Policy": 5,  # Deprecated, replaced by Permissions-Policy
    "Set-Cookie": 8,  # Check for Secure and HttpOnly flags
    "Content-Type-Security-Policy": 6,
    "report-to": 3,
    "server": 1,
    "content-encoding": 2,
    "nel": 1,
    "Cross-Origin-Embedder-Policy": 2,
    "Cross-Origin-Opener-Policy": 2,
    "Cross-Origin-Resource-Policy": 2
}

# MySQL Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='sql12.freesqldatabase.com',          # Replace with your MySQL host
        user='root',               # Replace with your MySQL username
        password='admin',       # Replace with your MySQL password
        database='mydatabase'
    )

# Function to fetch headers and score them
def fetch_and_score_headers(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        headers = response.headers
        score = 0
        header_details = []

        # Check each header in the scoring rules
        for header, points in header_scores.items():
            if header in headers:
                header_details.append({'header': header, 'value': headers[header], 'score': points})
                score += points
            else:
                header_details.append({'header': header, 'value': 'Not present', 'score': 0})

        # Check cookies for Secure and HttpOnly flags
        cookie_score = check_set_cookie(headers)
        score += cookie_score
        header_details.append({'header': 'Set-Cookie', 'value': 'Checked for Secure/HttpOnly flags', 'score': cookie_score})

        return {'score': score, 'header_details': header_details, 'total_headers': len(header_scores), 'server_ip': get_domain_ip(url)}

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Function to check Secure and HttpOnly flags in Set-Cookie header
def check_set_cookie(headers):
    cookies = headers.get('Set-Cookie', '')
    score = 0
    if 'Secure' in cookies:
        score += 4  # Secure flag found
    if 'HttpOnly' in cookies:
        score += 4  # HttpOnly flag found
    return score

# Function to save result in the MySQL database
def save_result(url, score, header_details):
    conn = get_db_connection()
    cursor = conn.cursor()
    header_details_json = json.dumps(header_details)  # Convert header details to JSON string
    if score < 30:
        grade = 'F'
    elif score < 40:
        grade = 'E'
    elif score < 50:
        grade = 'D'
    elif score < 60:
        grade = 'C'
    elif score < 75:
        grade = 'B'
    elif score < 90:
        grade = 'A'
    else:
        grade = 'A+'
    cursor.execute(
        "INSERT INTO headers_results (url, score, header_details, grade) VALUES (%s, %s, %s, %s)",
        (url, score, header_details_json, grade)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Fetch data from the database
def fetch_results():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries
    cursor.execute("SELECT url, score, grade, header_details FROM headers_results")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def fetch_unique_latest_results():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries
    cursor.execute("""
        SELECT DISTINCT url, score, grade, header_details
        FROM headers_results
        ORDER BY id DESC
        LIMIT 50
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.route("/", methods=["GET", "POST"])
def check_headers():
    if request.method == "POST":
        url = request.form.get('url')
        result = fetch_and_score_headers(url)
        
        # Save the result in the MySQL database
        if 'error' not in result:
            save_result(url, result['score'], result['header_details'])
        
        return render_template("result.html", result=result)
    
    return render_template("index.html")


@app.route('/api/results', methods=['POST'])
def get_results():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    result = fetch_and_score_headers(url)
    
    # Save the result in the MySQL database
    if 'error' not in result:
        save_result(url, result['score'], result['header_details'])

    return jsonify(result)


@app.route('/api/latest', methods=['GET'])
def get_latest_results():
    results = fetch_results()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
