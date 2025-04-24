from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Perform OCR using Doctr
model = ocr_predictor(pretrained=True)

def get_block():
    original_image = DocumentFile.from_images('C:\\Users\\ridwan\\Documents\\GitHub\\TownSuite.InvoiceOcr\\api-ocr\\invoice.png')  # Pass as a list of file-like objects
    original_doc = model(original_image)
    return original_doc.pages[0].blocks




   
