# XSS Detector

A Python package for detecting Cross-Site Scripting (XSS) attacks using machine learning.

## Installation

```bash
pip install xss-detector
```

## Features

- Detect XSS attacks in text, URLs, files, and HTTP requests
- Command-line interface for quick checks
- REST API for integration with other tools
- Deep learning model trained on a comprehensive XSS dataset
- Automated model training and management

## Quick Start

### Command Line Usage

Check a specific string for XSS:

```bash
xss-detector check "<script>alert(1)</script>"
```

Check a file for XSS:

```bash
xss-detector file suspicious.html
```

Check a URL:

```bash
xss-detector url "https://example.com/?param=value"
```

Start the API server:

```bash
xss-detector server --port 5000
```

### Python API Usage

```python
from xss_detector import XSSDetector

# Initialize the detector
detector = XSSDetector()

# Check a single string
result = detector.detect('<img src="x" onerror="alert(1)">')
print(f"XSS detected: {result['is_xss']}, Confidence: {result['confidence']}")

# Analyze a full HTTP request
analysis = detector.analyze_request(
    url_params={'search': 'something<script>alert(1)</script>'},
    headers={'User-Agent': 'Mozilla/5.0'},
    cookies={'session': 'abc123'}
)
print(f"Request contains XSS: {analysis['xss_detected']}")
```

### REST API Usage

Start the server:

```bash
xss-detector server
```

Then make requests:

```bash
# Check a single string
curl -X POST http://localhost:5000/check \
  -H "Content-Type: application/json" \
  -d '{"text": "<script>alert(1)</script>"}'

# Analyze a full request
curl -X POST http://localhost:5000/proxy \
  -H "Content-Type: application/json" \
  -d '{"param": "<img src=x onerror=alert(1)>"}'
```

## Model Training

The package automatically downloads a dataset and trains a model on first use. To manually train a new model:

```bash
xss-detector train
```

## License

MIT
