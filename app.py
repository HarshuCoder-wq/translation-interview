from flask import Flask, render_template, request, jsonify, send_file
import openai
from gtts import gTTS  
import uuid

app = Flask(__name__)

openai.api_key = "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"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    original_text = data.get("text")
    target_lang = data.get("target_lang", "es")  

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": f"Translate this healthcare text to {target_lang}. Preserve medical terminology."},
                {"role": "user", "content": original_text}
            ]
        )
        translated_text = response.choices[0].message["content"].strip()
        return jsonify({"translated": translated_text})
    except Exception as e:
        print("❌ OpenAI Error:", e)
        return jsonify({"translated": f"[Error: {str(e)}]"})

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text")

    
    tts = gTTS(text=text, lang="es")
    filename = f"static/{uuid.uuid4()}.mp3"
    tts.save(filename)

    return jsonify({"audio_url": "/" + filename})

if __name__ == "__main__":
    print("🚀 Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
