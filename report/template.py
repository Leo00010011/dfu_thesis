from fpdf import FPDF


class ReportTemplate(FPDF):
    def __init__(self):
        FPDF.__init__(self, format='Letter')
        self.alias_nb_pages()
        self.add_page()
        self.set_font("Times", "", 12)

    def header(self):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'Medición de la úlcera')
        self.ln(20)
    
    def footer(self):
        self.set_y(-30)
        self.set_font("Arial", '', 10)
        self.cell(0, 10, "Firmado por:")
        
    def add_patient(self, **patient):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "DATOS DEL PACIENTE", 1, 0)
        self.set_font("Times", "", 12)
        self.ln()
        self.cell(80, 10, f"Nombre: {patient['name']}")
        self.cell(80, 10, f"Edad: {patient['age']} años")
        self.ln()
        self.cell(80, 10, f"Sexo: {patient['sex']}")
        self.cell(80, 10, f"Tipo de diabetes: {patient['diabetes_type']}")
        self.ln()
        self.cell(80, 10, f"Tipo de úlcera: {patient['dfu_type']}")
        self.cell(80, 10, f"Localización: {patient['dfu_loc']}")
        self.ln(50)
        
        
    def add_measurement(self, p, a, v, date):
        self.set_font("Arial", "B", 12)
        self.cell(100, 10, "MEDICIONES DE LA ÚLCERA", 1)
        self.cell(0, 10, f"Fecha: {date}", 1)
        self.set_font("Times", "", 12)
        self.ln()
        self.cell(0, 10, f"Perímetro: {p} mm")
        self.ln()
        self.cell(0, 10, f"Área: {a} mm2")
        self.ln()
        self.cell(0, 10, f"Volumen: {v} mm3")