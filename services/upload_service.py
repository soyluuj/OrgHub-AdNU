import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

class UploadService:
    @staticmethod
    def save_image(file):
        if not file or file.filename == "":
            return None
            
        try:
            # Upload directly to Cloudinary
            upload_result = cloudinary.uploader.upload(file)
            
            # Return the permanent HTTPS URL
            return upload_result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary Upload Error: {e}")
            return None