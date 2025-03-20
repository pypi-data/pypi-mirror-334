"""
Flask API for XSS detection.
"""

from flask import Flask, request, jsonify
from .detector import XSSDetector

def create_app():
    """
    Create a Flask application for XSS detection.
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Initialize detector
    detector = XSSDetector()
    
    @app.route('/proxy', methods=['POST'])
    def proxy():
        # Get request data
        request_data = request.get_json(silent=True) or {}
        
        # Analyze request for XSS
        analysis = detector.analyze_request(
            request_data=request_data,
            url_params=request.args.to_dict(),
            form_data=request.form.to_dict(),
            headers=dict(request.headers),
            cookies=request.cookies
        )
        
        # Add request ID
        response = {
            'request_id': request.headers.get('X-Request-ID', 'unknown'),
            **analysis
        }
        
        # Return results
        return jsonify(response)

    @app.route('/check', methods=['POST'])
    def check_single():
        # Get text to check
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text parameter'}), 400
        
        # Check for XSS
        result = detector.detect(data['text'])
        
        # Return result
        return jsonify(result)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'})
    
    return app