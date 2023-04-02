import os

import barcode as bc
from PIL import Image
import random


def delete_files_in_dir(folder_path: str):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


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


def generate_bar_codes_pdf(products: list):
    folder_path = "codigos_de_barra"
    images = [
        Image.open(f"{folder_path}/" + f)
        for f in os.listdir(folder_path)
        if f.endswith(".png")
    ]

    pdf_path = f"{folder_path}/codigos.pdf"

    if len(products) != len(images):
        delete_files_in_dir(folder_path)
        for product in products:
            product_id = product[5]
            product_name = product[0]
            generate_code(product_id, product_name)

    if len(images) != 0:
        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
