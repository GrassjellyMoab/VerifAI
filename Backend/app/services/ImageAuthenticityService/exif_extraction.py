# EXIF extraction & checking
from PIL import Image
import PIL.ExifTags as ExifTags

def extract_exif(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return {"exif_present": False, "details": None}
        
        # Convert EXIF tag IDs to names
        exif_dict = {}
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            exif_dict[tag_name] = value
        
        return {"exif_present": True, "details": exif_dict}
    except Exception as e:
        return {"exif_present": False, "error": str(e)}

def check_exif_anomalies(exif_result):
    # Simple example: if there's no EXIF data at all, flag it
    if not exif_result["exif_present"]:
        return {"exif_score": 0, "reason": "No EXIF data"}
    
    # You could add more sophisticated checks (e.g., mismatch in date, camera model, etc.)
    return {"exif_score": 1, "reason": "EXIF data present and no anomalies detected"}
