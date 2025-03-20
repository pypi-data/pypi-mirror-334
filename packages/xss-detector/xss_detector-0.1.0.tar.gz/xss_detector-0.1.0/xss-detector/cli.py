"""
Command-line interface for XSS detection.
"""

import argparse
import json
import sys
import requests
from .detector import XSSDetector

def main():
    parser = argparse.ArgumentParser(description='XSS Detection Tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Check text command
    check_parser = subparsers.add_parser('check', help='Check text for XSS')
    check_parser.add_argument('text', help='Text to check for XSS')
    
    # Check file command
    file_parser = subparsers.add_parser('file', help='Check file for XSS')
    file_parser.add_argument('file', help='File to check for XSS')
    
    # Train model command
    train_parser = subparsers.add_parser('train', help='Train XSS detection model')
    
    # Start API server command
    server_parser = subparsers.add_parser('server', help='Start API server')
    server_parser.add_argument('--host', default='127.0.0.1', help='Host to listen on')
    server_parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    
    # URL check command
    url_parser = subparsers.add_parser('url', help='Check a URL for XSS')
    url_parser.add_argument('url', help='URL to check')
    url_parser.add_argument('--method', default='GET', help='HTTP method (GET, POST)')
    url_parser.add_argument('--data', help='Data to send with request (for POST)')
    
    args = parser.parse_args()
    
    # Handle no command
    if args.command is None:
        parser.print_help()
        return
    
    # Initialize detector
    detector = XSSDetector()
    
    # Handle commands
    if args.command == 'check':
        result = detector.detect(args.text)
        print_result(result)
    
    elif args.command == 'file':
        try:
            with open(args.file, 'r') as f:
                content = f.read()
                result = detector.detect(content)
                print_result(result)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    
    elif args.command == 'train':
        # This will force a new model to be trained
        detector = XSSDetector(use_existing_model=False)
        print("Model training complete.")
    
    elif args.command == 'server':
        from .api import create_app
        app = create_app()
        print(f"Starting XSS detection server on {args.host}:{args.port}")
        app.run(host=args.host, port=args.port)
    
    elif args.command == 'url':
        try:
            # Make request to URL
            if args.method.upper() == 'POST':
                data = json.loads(args.data) if args.data else None
                response = requests.post(args.url, json=data)
            else:
                response = requests.get(args.url)
            
            # Check response
            result = detector.detect(response.text)
            print(f"URL: {args.url}")
            print_result(result)
            
            # Also check any parameters
            if '?' in args.url:
                url_parts = args.url.split('?')
                if len(url_parts) > 1:
                    params = url_parts[1]
                    param_result = detector.detect(params)
                    print("\nURL Parameters:")
                    print_result(param_result)
            
        except Exception as e:
            print(f"Error checking URL: {e}", file=sys.stderr)
            return 1

def print_result(result):
    """Print detection result in a readable format."""
    xss_status = "DETECTED" if result['is_xss'] else "NOT DETECTED"
    confidence = result['confidence'] * 100
    
    print(f"XSS: {xss_status} (Confidence: {confidence:.2f}%)")
    if result['is_xss']:
        print(f"Text: {result['text'][:100]}{'...' if len(result['text']) > 100 else ''}")

if __name__ == '__main__':
    sys.exit(main())