# Error Level Analysis
from PIL import Image, ImageChops
import os

def perform_ela(image_path, quality=90):
    """ 
    Saves the image at a certain JPEG quality, 
    then compares differences to original for compression artifacts.
    """
    temp_path = "temp_compressed.jpg"
    original = Image.open(image_path).convert('RGB')
    original.save(temp_path, 'JPEG', quality=quality)
    
    compressed = Image.open(temp_path)
    ela_image = ImageChops.difference(original, compressed)
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    return ela_image

def analyze_ela(ela_image):
    # Convert to grayscale, get pixel stats to see how large the difference is
    extrema = ela_image.getextrema()
    max_diff = max([point[1] for point in extrema])  # The max difference in any channel
    
    # Heuristic: higher differences may indicate digital manipulation
    if max_diff > 50:
        return {"ela_score": 0.5, "reason": f"Significant ELA difference: {max_diff}"}
    else:
        return {"ela_score": 1.0, "reason": f"Minor ELA difference: {max_diff}"}
