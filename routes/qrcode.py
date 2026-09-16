#routes/qr_code.py

import os

from flask import Blueprint, render_template, request

from services.qrcode_service import generate_qr_code


qrcode = Blueprint(
    "qrcode",
    __name__,
    url_prefix="/portfolio/qrcode"
)


@qrcode.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    error = None

    # Default values
    foreground_color = "#000000"
    background_color = "#FFFFFF"
    box_size = 10
    border = 4

    if request.method == "POST":
        data = request.form.get("data", "").strip()
        filename = request.form.get("filename", "").strip()
        foreground_color = request.form.get(
            "foreground_color", "#000000"
        )
        background_color = request.form.get(
            "background_color", "#FFFFFF"
        )

        # Validate numeric values
        try:
            box_size = int(request.form.get("box_size", 10))
            border = int(request.form.get("border", 4))

            if box_size < 1 or box_size > 20:
                raise ValueError("QR size must be between 1 and 20.")

            if border < 0 or border > 10:
                raise ValueError("Border must be between 0 and 10.")

        except ValueError as exc:
            error = str(exc)

        if not error:
            try:
                # Store generated QR codes inside the portfolio's
                # existing static directory.
                output_dir = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "static",
                    "generated",
                    "qr"
                )

                generate_qr_code(
                    data=data,
                    filename=filename,
                    output_dir=output_dir,
                    box_size=box_size,
                    border=border,
                    fill_color=foreground_color,
                    back_color=background_color,
                )

                # Normalize filename because the service automatically
                # adds .png when necessary.
                if not filename.lower().endswith(".png"):
                    filename += ".png"

                qr_filename = filename

            except ValueError as exc:
                error = str(exc)

            except Exception as exc:
                error = f"Unable to generate QR code: {exc}"

    return render_template(
        "portfolio/qrcode.html",
        qr_filename=qr_filename,
        error=error,
        foreground_color=foreground_color,
        background_color=background_color,
        box_size=box_size,
        border=border,
    )