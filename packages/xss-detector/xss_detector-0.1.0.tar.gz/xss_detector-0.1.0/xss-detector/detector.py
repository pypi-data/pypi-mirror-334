"""
Core XSS detection functionality.
"""

from tensorflow.keras.preprocessing.sequence import pad_sequences
from .model import load_xss_model

class XSSDetector:
    """
    A class for detecting XSS attacks in text.
    """
    
    def __init__(self, use_existing_model=True):
        """
        Initialize the XSS detector.
        
        Args:
            use_existing_model: If True, use an existing model if available. 
                               If False, force training a new model.
        """
        # Load or train the model
        self.model, self.tokenizer, self.max_sequence_length = load_xss_model()
    
    def detect(self, text):
        """
        Detect if a text contains an XSS attack.
        
        Args:
            text: String to check for XSS
            
        Returns:
            dict: Contains 'text', 'is_xss', and 'confidence' keys
        """
        # Tokenize and pad the text
        sequence = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequence, maxlen=self.max_sequence_length)
        
        # Make prediction
        prediction = self.model.predict(padded)[0][0]
        
        return {
            'text': text,
            'is_xss': bool(prediction > 0.5),
            'confidence': float(prediction)
        }
    
    def analyze_request(self, request_data=None, url_params=None, form_data=None, 
                        headers=None, cookies=None):
        """
        Analyze a full HTTP request for XSS attacks.
        
        Args:
            request_data: Dict containing request body data
            url_params: Dict containing URL parameters
            form_data: Dict containing form data
            headers: Dict containing HTTP headers
            cookies: Dict containing cookies
            
        Returns:
            dict: Analysis results containing all checked vectors and detection results
        """
        vectors = []
        
        # Extract from URL parameters
        if url_params:
            for key, value in url_params.items():
                vectors.append(f"{key}={value}")
        
        # Extract from form data
        if form_data:
            for key, value in form_data.items():
                vectors.append(f"{key}={value}")
        
        # Extract from JSON body
        if request_data:
            for key, value in self._flatten_json(request_data).items():
                vectors.append(f"{key}={value}")
        
        # Extract from headers
        if headers:
            for key, value in headers.items():
                vectors.append(f"{key}={value}")
        
        # Extract from cookies
        if cookies:
            for key, value in cookies.items():
                vectors.append(f"{key}={value}")

        # Check each vector for XSS
        results = []
        for vector in vectors:
            results.append(self.detect(vector))
        
        # Return results
        return {
            'total_vectors_checked': len(results),
            'xss_detected': any(result['is_xss'] for result in results),
            'results': results
        }
    
    def _flatten_json(self, nested_json, parent_key=''):
        """
        Flatten a nested JSON object into key-value pairs.
        
        Args:
            nested_json: A nested JSON object
            parent_key: The parent key for nested values
            
        Returns:
            dict: Flattened key-value pairs
        """
        flattened = {}
        for key, value in nested_json.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                flattened.update(self._flatten_json(value, new_key))
            elif isinstance(value, (list, tuple)):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(self._flatten_json(item, f"{new_key}[{i}]"))
                    else:
                        flattened[f"{new_key}[{i}]"] = str(item)
            else:
                flattened[new_key] = str(value)
        return flattened