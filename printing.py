import os
from fpdf import FPDF

baseWidth = 74
baseHeight = 105  # 55 to 83mm base
heightPerObj = 5
phoneNum = "6362-9187"
baseFontNum = 8
testProducts = [
    {'cantidad':23, 'descripcion':"Saco de Ponedora", 'subtotal':9880.00, 'descuento':100},
    {'cantidad':3, 'descripcion':"Cucu Girasol 250g", 'subtotal':2119.60, 'descuento':0},
    {'cantidad':23, 'descripcion':"Saco de maiz", 'subtotal':6766.20, 'descuento':10},
    {'cantidad':1, 'descripcion':"Balance Puppy Saco", 'subtotal':23595.00, 'descuento':10000}
]
# + numero de 5 digitos


def usePrinter(fileName: str):
    os.startfile(fileName, "print")


class PDF(FPDF):

    # modifiedHeight: int
    borders = False

    def customHeader(self):
        # headerWidth = baseWidth/2
        self.set_xy(1, 5)
        self.set_font('Arial', '', baseFontNum+2)
        self.set_margins(1, 1)
        # self.set_text_color(220, 50, 50)
        lineY = self.get_y() - heightPerObj/2
        lineX = 1
        self.line(lineX, lineY, baseWidth-lineX, lineY)
        self.cell(w=0, h=heightPerObj, align='C',
                  txt="Recibo de Contado", border=self.borders, ln=1)
        # self.set_xy(self.get_x(), self.get_y() + heightPerObj)
        self.set_font('Arial', 'B', baseFontNum+3)
        self.cell(w=0, h=heightPerObj, align='C',
                  txt="PetShop Punto A", border=self.borders, ln=1)
        self.ln()

    def body(self, receiptNumber: int, phone: str, name: str, products: list):
        
        self.set_font('Arial', 'B', baseFontNum)
        receiptText = f"PSPA{receiptNumber:06}"
        self.cell(w=17, h=heightPerObj, txt="Factura No.:", border=self.borders)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=receiptText, border=self.borders, ln=1)

        self.set_font('Arial', 'B', baseFontNum)
        self.cell(w=17, h=heightPerObj, txt="Teléfono:", border=self.borders)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=phone, border=self.borders, ln=1)

        self.set_font('Arial', 'B', baseFontNum)
        self.cell(w=17, h=heightPerObj, txt="Nombre:", border=self.borders)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=name, border=self.borders, ln=1)

        self.set_font('Arial', 'U', 6)
        self.cell(w=10.5, h=heightPerObj, txt="Cantidad", align='C', border=self.borders)
        self.cell(w=48, h=heightPerObj, txt="Descripción", align='C', border=self.borders)
        self.cell(w=0, h=heightPerObj, txt="Subtotal", align='C', border=self.borders, ln=1)

        subtotal = 0
        descuentoTotal = 0
        for d in products:
            # subTotalProducto = d['subtotal'] - d['descuento']
            subtotal += d['subtotal']
            descuentoTotal += d['descuento']

            self.set_font('Arial', '', 6)
            self.cell(w=10.5, h=heightPerObj, txt=str(d['cantidad']), border=self.borders)
            self.cell(w=48, h=heightPerObj, txt=d['descripcion'], align='C', border=self.borders)
            self.cell(w=0, h=heightPerObj, txt=f"{d['subtotal']:,.2f}", align='C', border=self.borders, ln=1)

        self.set_font('Arial', 'B', baseFontNum)
        self.cell(w=14, h=heightPerObj, txt="Sub Total:", border=self.borders)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=f"{subtotal:,.2f}", align='R', border=self.borders, ln=1)

        self.set_font('Arial', 'B', baseFontNum)
        self.cell(w=15, h=heightPerObj, txt="Descuento:", border=self.borders)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=f"{descuentoTotal:,.2f}", align='R', border=self.borders, ln=1)

        self.set_font('Arial', 'B', baseFontNum)
        self.cell(w=23, h=heightPerObj, txt="Total por servicio:", border=self.borders)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=f"{subtotal-descuentoTotal:,.2f}", align='R', border=self.borders, ln=1)
        

        self.set_xy(self.get_x(), self.get_y() + heightPerObj)
        lineY = self.get_y() - heightPerObj/2
        lineX = 1
        self.line(lineX, lineY, baseWidth-lineX, lineY)

    def customFooter(self, dateTime: str):
        a1 = f"{'300 S centro del Adulto Mayor':^29}"
        a2 = f"{'San Rafael - Heredia':^29}"
        self.set_font('Arial', 'B', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=a1, align='C', border=self.borders, ln=1)
        self.cell(w=0, h=heightPerObj, txt=a2, align='C', border=self.borders, ln=1)
        self.set_font('Arial', '', baseFontNum)
        self.cell(w=0, h=heightPerObj, txt=dateTime, align='C', border=self.borders, ln=1)
        self.set_font('Arial', 'B', baseFontNum+1)
        self.cell(w=0, h=heightPerObj, txt="Gracias por su Compra", align='C', border=self.borders, ln=1)
        # self.set_font('Arial', 'B', baseFontNum)
        # self.cell(w=16, h=heightPerObj, txt="Nombre:", border=self.borders)
        # self.set_font('Arial', '', baseFontNum)
        # self.cell(w=0, h=heightPerObj, txt=name, border=self.borders, ln=1)


def generateReceipt(ammountOfItems: int, dateTime: str):
    finalHeight = baseHeight + ammountOfItems * heightPerObj
    pdf = PDF(orientation='P', unit='mm', format=(baseWidth, finalHeight))
    pdf.add_page()
    pdf.customHeader()
    pdf.body(123, '6362-9187', 'Macho Peña',testProducts)
    pdf.customFooter(dateTime)
    # pdf.lines()
    # pdf.header(modifiedHeight=finalHeight)
    pdf.output('test.pdf', 'F')
    # usePrinter('test.pdf')


generateReceipt(len(testProducts), '27')
