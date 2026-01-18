from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
BOT_TOKEN =8523682354:AAFErcCLoiFIbpG9Zw3TioMCI07-StT3h8s
os.environ.get('BOT_TOKEN')  # Токен установим позже в Render

@app.route('/check_premium', methods=['POST'])
def check_premium():
    data = request.get_json()
    username = data.get('username', '').lstrip('@')

    if not username:
        return jsonify({'error': 'No username'}), 400

    try:
        resp = requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/getChat',
            params={'chat_id': f'@{username}'}
        ).json()

        if resp.get('ok'):
            return jsonify({'is_premium': resp['result'].get('is_premium', False)})
        else:
            return jsonify({'error': 'User not found or never interacted with bot'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'Server is running. Use POST /check_premium'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
