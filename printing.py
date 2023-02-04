import os
from fpdf import FPDF
from database_util import get_today_date

base_width = 74
base_height = 105  # 55 to 83mm base
height_per_obj = 5
phone_num = "6362-9187"
base_font_num = 8
test_products = [
    {
        "cantidad": 23,
        "descripcion": "Saco de Ponedora",
        "subtotal": 9880.00,
        "descuento": 100,
    },
    {
        "cantidad": 3,
        "descripcion": "Cucu Girasol 250g",
        "subtotal": 2119.60,
        "descuento": 0,
    },
    {
        "cantidad": 23,
        "descripcion": "Saco de maiz",
        "subtotal": 6766.20,
        "descuento": 10,
    },
    {
        "cantidad": 1,
        "descripcion": "Balance Puppy Saco",
        "subtotal": 23595.00,
        "descuento": 10000,
    },
]
# + numero de 5 digitos


def use_printer(fileName: str):
    os.startfile(fileName, "print")


class PDF(FPDF):

    # modifiedHeight: int
    borders = False

    def custom_header(self):
        # headerWidth = base_width/2
        self.set_xy(1, 5)
        self.set_font("Arial", "", base_font_num + 2)
        self.set_margins(1, 1)
        # self.set_text_color(220, 50, 50)
        lineY = self.get_y() - height_per_obj / 2
        lineX = 1
        self.line(lineX, lineY, base_width - lineX, lineY)
        self.cell(
            w=0,
            h=height_per_obj,
            align="C",
            txt="Recibo de Contado",
            border=self.borders,
            ln=1,
        )
        # self.set_xy(self.get_x(), self.get_y() + height_per_obj)
        self.set_font("Arial", "B", base_font_num + 3)
        self.cell(
            w=0,
            h=height_per_obj,
            align="C",
            txt="PetShop Punto A",
            border=self.borders,
            ln=1,
        )
        self.ln()

    def body(self, receipt_number: int, phone: str, name: str, products: list):

        self.set_font("Arial", "B", base_font_num)
        receiptText = f"{receipt_number:08}"
        self.cell(w=17, h=height_per_obj, txt="Factura No.:", border=self.borders)
        self.set_font("Arial", "", base_font_num)
        self.cell(w=0, h=height_per_obj, txt=receiptText, border=self.borders, ln=1)

        self.set_font("Arial", "B", base_font_num)
        self.cell(w=17, h=height_per_obj, txt="Teléfono:", border=self.borders)
        self.set_font("Arial", "", base_font_num)
        self.cell(w=0, h=height_per_obj, txt=phone, border=self.borders, ln=1)

        self.set_font("Arial", "B", base_font_num)
        self.cell(w=17, h=height_per_obj, txt="Nombre:", border=self.borders)
        self.set_font("Arial", "", base_font_num)
        self.cell(w=0, h=height_per_obj, txt=name, border=self.borders, ln=1)

        self.set_font("Arial", "U", 6)
        self.cell(
            w=10.5, h=height_per_obj, txt="Cantidad", align="C", border=self.borders
        )
        self.cell(
            w=48, h=height_per_obj, txt="Descripción", align="C", border=self.borders
        )
        self.cell(
            w=0, h=height_per_obj, txt="Subtotal", align="C", border=self.borders, ln=1
        )

        subtotal = 0.0
        descuento_total = 0.0
        for d in products:
            # subTotalProducto = d['subtotal'] - d['descuento']
            subtotal += d["subtotal"]
            descuento_total += d["descuento"]

            self.set_font("Arial", "", 6)
            self.cell(
                w=10.5, h=height_per_obj, txt=str(d["cantidad"]), border=self.borders
            )
            self.cell(
                w=48,
                h=height_per_obj,
                txt=d["descripcion"],
                align="C",
                border=self.borders,
            )
            self.cell(
                w=0,
                h=height_per_obj,
                txt=f"{d['subtotal']:,.2f}",
                align="C",
                border=self.borders,
                ln=1,
            )

        self.set_font("Arial", "B", base_font_num)
        self.cell(w=14, h=height_per_obj, txt="Sub Total:", border=self.borders)
        self.set_font("Arial", "", base_font_num)
        self.cell(
            w=0,
            h=height_per_obj,
            txt=f"{subtotal:,.2f}",
            align="R",
            border=self.borders,
            ln=1,
        )

        self.set_font("Arial", "B", base_font_num)
        self.cell(w=15, h=height_per_obj, txt="Descuento:", border=self.borders)
        self.set_font("Arial", "", base_font_num)
        self.cell(
            w=0,
            h=height_per_obj,
            txt=f"{descuento_total:,.2f}",
            align="R",
            border=self.borders,
            ln=1,
        )

        self.set_font("Arial", "B", base_font_num)
        self.cell(
            w=23, h=height_per_obj, txt="Total por servicio:", border=self.borders
        )
        self.set_font("Arial", "", base_font_num)
        self.cell(
            w=0,
            h=height_per_obj,
            txt=f"{subtotal-descuento_total:,.2f}",
            align="R",
            border=self.borders,
            ln=1,
        )

        self.set_xy(self.get_x(), self.get_y() + height_per_obj)
        lineY = self.get_y() - height_per_obj / 2
        lineX = 1
        self.line(lineX, lineY, base_width - lineX, lineY)

    def custom_footer(self, date_time: str):
        a1 = f"{'300 S centro del Adulto Mayor':^29}"
        a2 = f"{'San Rafael - Heredia':^29}"
        self.set_font("Arial", "B", base_font_num)
        self.cell(w=0, h=height_per_obj, txt=a1, align="C", border=self.borders, ln=1)
        self.cell(w=0, h=height_per_obj, txt=a2, align="C", border=self.borders, ln=1)
        self.set_font("Arial", "", base_font_num)
        self.cell(
            w=0, h=height_per_obj, txt=date_time, align="C", border=self.borders, ln=1
        )
        self.set_font("Arial", "B", base_font_num + 1)
        self.cell(
            w=0,
            h=height_per_obj,
            txt="Gracias por su Compra",
            align="C",
            border=self.borders,
            ln=1,
        )
        # self.set_font('Arial', 'B', base_font_num)
        # self.cell(w=16, h=height_per_obj, txt="Nombre:", border=self.borders)
        # self.set_font('Arial', '', base_font_num)
        # self.cell(w=0, h=height_per_obj, txt=name, border=self.borders, ln=1)


def generate_receipt(
    receipt_number: int, client_name: str, products_list: list, date_time: str
):
    print(f"RECEIPT: {products_list}")
    amount_of_items = len(products_list)
    final_height = base_height + amount_of_items * height_per_obj
    pdf = PDF(orientation="P", unit="mm", format=(base_width, final_height))
    pdf.add_page()
    pdf.custom_header()
    pdf.body(receipt_number, "6362-9187", client_name, products_list)
    pdf.custom_footer(date_time)
    # pdf.lines()
    # pdf.header(modifiedHeight=final_height)
    pdf.output(f"facturas/{date_time}_{receipt_number}.pdf", "F")
    # use_printer('test.pdf')


# generate_receipt(14, "Huu", test_products, get_today_date())
