import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load your API key from an environment variable or secret management service
openai.api_key = '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'

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({'response': response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
