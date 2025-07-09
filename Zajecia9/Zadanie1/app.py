from flask import Flask, request, jsonify
from transformers import pipeline
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in JSON payload"}), 400

        text = data['text']
        if not isinstance(text, str) or not text.strip():
            return jsonify({"error": "Text must be a non-empty string"}), 400

        max_length = data.get('max_length', 150)
        min_length = data.get('min_length', 30)
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)

        summary_text = summary[0]['summary_text']

        return jsonify({
            "summary": summary_text,
            "original_length": len(text.split()),
            "summary_length": len(summary_text.split())
        }), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)