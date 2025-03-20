"""
Utility functions for XSS detection.
"""

import re

def extract_input_fields(html):
    """
    Extract input fields from HTML content for XSS analysis.
    
    Args:
        html: HTML content as string
        
    Returns:
        list: Extracted input fields
    """
    # Basic pattern to extract input fields (could be enhanced with more sophisticated HTML parsing)
    input_pattern = r'<input[^>]*>'
    input_fields = re.findall(input_pattern, html)
    
    # Extract attributes from input fields
    results = []
    for field in input_fields:
        name_match = re.search(r'name=["\'](.*?)["\']', field)
        value_match = re.search(r'value=["\'](.*?)["\']', field)
        
        name = name_match.group(1) if name_match else "unnamed"
        value = value_match.group(1) if value_match else ""
        
        if value:
            results.append(f"{name}={value}")
    
    return results

def extract_script_content(html):
    """
    Extract content from script tags for XSS analysis.
    
    Args:
        html: HTML content as string
        
    Returns:
        list: Extracted script contents
    """
    script_pattern = r'<script[^>]*>(.*?)</script>'
    return re.findall(script_pattern, html, re.DOTALL)

def extract_event_handlers(html):
    """
    Extract event handlers from HTML content for XSS analysis.
    
    Args:
        html: HTML content as string
        
    Returns:
        list: Extracted event handlers
    """
    # Look for common event handlers
    events = ['onclick', 'onload', 'onmouseover', 'onerror', 'onmouseout', 'onkeydown', 'onkeyup']
    handlers = []
    
    for event in events:
        pattern = f'{event}=["\'](.*?)["\']'
        matches = re.findall(pattern, html)
        handlers.extend([f"{event}={match}" for match in matches])
    
    return handlers

def analyze_html(html, detector):
    """
    Analyze HTML content for potential XSS vulnerabilities.
    
    Args:
        html: HTML content as string
        detector: XSSDetector instance
        
    Returns:
        dict: Analysis results
    """
    vectors = []
    
    # Extract various potential XSS vectors
    vectors.extend(extract_input_fields(html))
    vectors.extend(extract_script_content(html))
    vectors.extend(extract_event_handlers(html))
    
    # Check raw HTML as well
    vectors.append(html)
    
    # Check each vector
    results = []
    for vector in vectors:
        if vector:  # Skip empty vectors
            results.append(detector.detect(vector))
    
    return {
        'total_vectors_checked': len(results),
        'xss_detected': any(result['is_xss'] for result in results),
        'results': results
    }