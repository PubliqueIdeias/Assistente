import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Suas chaves
ZAPI_TOKEN = "C9E90B8EAEC425708E3EFA12"
OPENAI_API_KEY = "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"

@app.route('/', methods=['GET'])
def index():
    return "🤖 Bot Publique Ideias rodando!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('message', '')
    sender = data.get('sender', '')

    print(f"📩 Mensagem recebida: {message} de {sender}")

    if message.lower() in ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite']:
        resposta = "Olá! Sou o assistente virtual da Publique Ideias. Como posso ajudar?"
    else:
        resposta = get_openai_response(message)

    send_whatsapp_message(sender, resposta)
    return jsonify({"status": "mensagem enviada"}), 200

def send_whatsapp_message(phone, text):
    url = f"https://api.z-api.io/instances/instance0000/token/{ZAPI_TOKEN}/send-text"
    payload = {
        "phone": phone,
        "message": text
    }
    requests.post(url, json=payload)

def get_openai_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um assistente inteligente da marca Publique Ideias."},
            {"role": "user", "content": user_message}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
