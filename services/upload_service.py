import os
import uuid

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


class UploadService:

    @staticmethod
    def allowed(filename):
        return (
            "." in filename and
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @staticmethod
    def save_images(files):

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        saved = []

        for file in files:

            if not file:
                continue

            if file.filename == "":
                continue

            if not UploadService.allowed(file.filename):
                continue

            extension = file.filename.rsplit(".", 1)[1].lower()

            filename = f"{uuid.uuid4()}.{extension}"

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            file.save(filepath)

            saved.append(f"uploads/{filename}")

        return saved