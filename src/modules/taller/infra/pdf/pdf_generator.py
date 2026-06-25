import io
from typing import Any, Dict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.modules.taller.domain.ports.pdf_generator_port import PdfGeneratorPort

class ReportLabPdfGenerator(PdfGeneratorPort):
    def generate_pdf(self, context: Dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Cotización de Taller - ClaimVision")
        
        c.setFont("Helvetica", 12)
        y = height - 100
        
        # Simple rendering of the context dictionary
        for key, value in context.items():
            if isinstance(value, list):
                c.drawString(50, y, f"{key}:")
                y -= 20
                for item in value:
                    c.drawString(70, y, f"- {item}")
                    y -= 20
            else:
                c.drawString(50, y, f"{key}: {value}")
                y -= 20
                
            if y < 50:
                c.showPage()
                y = height - 50
                
        c.save()
        buffer.seek(0)
        return buffer.read()
