import os

import barcode as bc
from PIL import Image
import random


def generate_bar_code_img(product_name: str, product_code: str):
    my_code = bc.Code128(product_code, writer=bc.writer.ImageWriter())
    my_code.save(f"codigos_de_barra/{product_name}")


def generate_code(product_id: int, product_name: str) -> str:
    random.seed(product_id)
    number = random.randint(100000000, 1000000000)
    product_code = str(number)
    product_file_name = f"{product_name}.png"
    if product_file_name not in [f for f in os.listdir("codigos_de_barra")]:
        generate_bar_code_img(product_name, product_code)
    return product_code


# ---------------------------------------------------------------------------
# install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation


def generate_bar_codes_pdf():
    images = [
        Image.open("codigos_de_barra/" + f)
        for f in os.listdir("codigos_de_barra")
        if f.endswith(".png")
    ]

    pdf_path = "codigos_de_barra/codigos.pdf"

    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
