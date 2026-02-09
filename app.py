from flask import Flask, request, jsonify, send_from_directory
import os
import ai_engine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def landing():
    return send_from_directory(os.getcwd(), 'landing.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.getcwd(), path)

# --- API Endpoints ---

@app.route('/api/marketing', methods=['POST'])
def marketing():
    data = request.json
    try:
        result = ai_engine.generate_marketing_campaign(
            data.get('product'),
            data.get('description'),
            data.get('audience'),
            data.get('platform')
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error: {e}")
        # Always return success to UI with fallback
        return jsonify({"result": ai_engine.fallback_marketing(
            data.get('product'),
            data.get('description'),
            data.get('audience'),
            data.get('platform')
        )})

@app.route('/api/sales', methods=['POST'])
def sales():
    data = request.json
    try:
        result = ai_engine.generate_sales_pitch(
            data.get('product'),
            data.get('persona'),
            data.get('industry'),
            data.get('size')
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"result": ai_engine.fallback_sales(
            data.get('product'),
            data.get('persona'),
            data.get('industry'),
            data.get('size')
        )})

@app.route('/api/lead-scoring', methods=['POST'])
def lead_scoring():
    data = request.json
    try:
        result = ai_engine.generate_lead_score(
            data.get('product'),
            data.get('icp'),
            data.get('valueProp'),
            data.get('leadData')
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"result": ai_engine.fallback_lead_scoring(
            data.get('product'),
            data.get('leadData')
        )})

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible if needed, strict local otherwise
    app.run(debug=True, port=5001)
