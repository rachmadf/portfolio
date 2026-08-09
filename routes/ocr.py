# portfolio\routes\ocr.py
from werkzeug.utils import secure_filename
from flask import render_template
from flask import Blueprint
from flask import send_file
from flask import request
import os
import io

from services.ocr_service import OCRService

ocr = Blueprint(
	"ocr",
	__name__,
	url_prefix="/ocr"
)

@ocr.route("/", methods=["GET"])
def index():
    """
    Display OCR Text Extractor page.

    URL: GET /portfolio/ocr/

    Returns:
        Rendered OCR page.
    """

    return render_template(
        "portfolio/ocr/index.html",
        extracted_text="text123abc"
    )

@ocr.route("/extract", methods=["POST"])
def extract():
    image = request.files.get("image_file")

    if image is None:

        return render_template(
            "portfolio/ocr/index.html",
            extracted_text="No image selected."
        )

    filename = secure_filename(image.filename)

    upload_folder = os.path.join(
        "static",
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(
        upload_folder,
        filename
    )

    image.save(image_path)

    extracted_text = OCRService.extract_text(
        image_path
    )

    return render_template(
        "portfolio/ocr/index.html",
        extracted_text=extracted_text
    )


@ocr.route("/download_txt", methods=["POST"])
def download_txt():
	ocr_text = request.form.get(
	    "ocr_text",
	    ""
	)

	txt_file = io.BytesIO()

	txt_file.write(
	    ocr_text.encode("utf-8")
	)

	txt_file.seek(0)

	return send_file(
	    txt_file,
	    as_attachment=True,
	    download_name="ocr_result.txt",
	    mimetype="text/plain"
	)