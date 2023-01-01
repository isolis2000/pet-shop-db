import os
from fpdf import FPDF

baseWidth = 76
baseHeight = 105  # 55 to 83mm base
heightPerObj = 6

receiptHeading = """
---------------------------------
        Recibo de Contado
        PetShop Punto A
        """
receiptNumber = "Factura # PSPA"  # + numero de 5 digitos


def usePrinter(fileName: str):
    os.startfile(fileName, "print")


class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(0, baseHeight/2, baseWidth, baseHeight/2)


def createPDF(ammountOfItems):
    finalHeight = baseHeight + ammountOfItems * heightPerObj
    pdf = PDF(orientation='P', unit='mm', format=(baseWidth, finalHeight))
    pdf.add_page()
    pdf.output('test.pdf', 'F')
