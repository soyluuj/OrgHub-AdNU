import os
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join("static", "uploads")

class UploadService:
    @staticmethod
    def save_image(file):
        if not file or file.filename == "":
            return None
            
        # Ensure folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Secure the filename and add a unique ID so files don't overwrite
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Return the relative path for the database
        return f"uploads/{unique_filename}"