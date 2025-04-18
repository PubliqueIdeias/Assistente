import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Função para pegar a resposta da OpenAI
def get_openai_response(message):
    headers = {
        'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "gpt-3.5-turbo",  # ou gpt-4, se tiver acesso
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    try:
        result = response.json()
        # A resposta da OpenAI pode não ter o campo 'choices' caso haja erro.
        return result['choices'][0]['message']['content']
    except Exception as e:
        print("Erro na resposta da OpenAI:", result)
        return "Desculpe, houve um erro ao gerar a resposta."

# Rota do webhook que vai receber a mensagem e enviar para a OpenAI
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Mensagem não recebida'}), 400
    
    message = data['message']
    
    try:
        # Chama a função para obter a resposta da OpenAI
        resposta = get_openai_response(message)
        return jsonify({'response': resposta}), 200
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")
        return jsonify({'error': 'Erro interno'}), 500

if __name__ == '__main__':
    # A aplicação deve rodar em um ambiente de produção com WSGI, como Gunicorn
    app.run(debug=True, host='0.0.0.0', port=3000)
