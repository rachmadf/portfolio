#services/qrcode_service.py

import os
import re

import qrcode


def validate_filename(filename):
    """
    Validate and normalize a QR code output filename.

    Returns:
        str: Validated filename with .png extension.

    Raises:
        ValueError: If the filename is invalid.
    """
    filename = filename.strip()

    if not filename:
        raise ValueError("Filename cannot be empty.")

    # Prevent directory traversal
    if os.path.basename(filename) != filename:
        raise ValueError("Filename cannot contain directory paths.")

    # Allow letters, numbers, spaces, underscores, hyphens, and dots
    if not re.match(r"^[a-zA-Z0-9 _.-]+$", filename):
        raise ValueError(
            "Filename contains invalid characters. "
            "Use only letters, numbers, spaces, underscores, hyphens, and dots."
        )

    # Automatically add .png
    if not filename.lower().endswith(".png"):
        filename += ".png"

    return filename


def generate_qr_code(
    data,
    filename,
    output_dir,
    box_size=10,
    border=4,
    fill_color="#000000",
    back_color="#FFFFFF",
):
    """
    Generate and save a QR code as a PNG image.

    Args:
        data (str): Data encoded into the QR code.
        filename (str): Output filename.
        output_dir (str): Directory where the QR image is saved.
        box_size (int): Size of each QR module.
        border (int): QR border width.
        fill_color (str): QR foreground color.
        back_color (str): QR background color.

    Returns:
        str: Absolute path to the generated QR image.
    """

    if not data or not data.strip():
        raise ValueError("QR code data cannot be empty.")

    filename = validate_filename(filename)

    if box_size <= 0:
        raise ValueError("Box size must be greater than 0.")

    if border < 0:
        raise ValueError("Border cannot be negative.")

    if not output_dir:
        raise ValueError("Output directory cannot be empty.")

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )

    qr.add_data(data.strip())
    qr.make(fit=True)

    image = qr.make_image(
        fill_color=fill_color,
        back_color=back_color,
    )

    image.save(output_path)

    return os.path.abspath(output_path)