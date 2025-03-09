import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("AIorNOT_KEY")

# Base URL for the API
BASE_URL = "https://api.aiornot.com/v1"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

def is_url(string):
    """
    Check if a string is a valid URL.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if string is a URL, False otherwise.
    """
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def auto_detect_and_check(input_str):
    """
    Automatically detect whether the input is a URL or a file path and check it
    using the AIORNOT API. It supports image and audio files.

    Args:
        input_str (str): A URL or file path to analyze.

    Returns:
        dict: The API response with analysis results, or None if input is invalid.
    """
    # If the input is a valid URL, assume it's an image URL and check it.
    if is_url(input_str):
        return check_image_url(input_str)

    # If it's not a URL, ensure that the file exists on disk.
    if not os.path.exists(input_str):
        print(f"Error: The input '{input_str}' is not a valid URL or an existing file path.")
        return None

    # Determine file type based on the extension.
    file_extension = os.path.splitext(input_str)[1].lower()
    # Define supported audio and image extensions.
    audio_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.apng']

    if file_extension in audio_extensions:
        return check_voice_file(input_str)
    elif file_extension in image_extensions:
        return check_image_file(input_str)
    else:
        print(f"Error: Unsupported file type '{file_extension}'.")
        print("Supported image types: " + ", ".join(image_extensions))
        print("Supported audio types: " + ", ".join(audio_extensions))
        return None


# Dummy implementations of the API functions for context.
# Replace these with your actual implementations.
def check_image_url(image_url):
    print(f"Checking image URL: {image_url}")
    # Call your API here...
    return {"report": {"verdict": "real", "ai": {"confidence": 0.2}, "human": {"confidence": 0.8}}, "id": "123",
            "created_at": "2025-03-09T00:00:00Z"}


def check_image_file(file_path):
    print(f"Checking image file: {file_path}")
    # Call your API here...
    return {"report": {"verdict": "fake", "ai": {"confidence": 0.7}, "human": {"confidence": 0.3}}, "id": "456",
            "created_at": "2025-03-09T00:00:00Z"}


def check_voice_file(file_path):
    print(f"Checking voice file: {file_path}")
    # Call your API here...
    return {"report": {"verdict": "real", "confidence": 0.9, "duration": 12}, "id": "789",
            "created_at": "2025-03-09T00:00:00Z"}


# Example usage:
if __name__ == "__main__":
    # Example with a URL:
    result_url = auto_detect_and_check("https://example.com/sample_image.jpg")
    print("Result from URL:", result_url)

    # Example with a local file (adjust the path to one that exists on your system):
    result_file = auto_detect_and_check("local_image.jpg")
    print("Result from file:", result_file)
