from flask import Flask, request, render_template
import os
import fitz  # PyMuPDF
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_text(text):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Summarize the following text and provide suggestions:\n\n{text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        text = pdf_to_text(filepath)
        summary = analyze_text(text)
        return summary

if __name__ == "__main__":
    app.run(debug=True)
