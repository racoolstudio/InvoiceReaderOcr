
import re
import time
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

from haystack import Document
from haystack.components.readers import ExtractiveReader
import threading

# Perform OCR using Doctr
model = ocr_predictor(pretrained=True)
reader = ExtractiveReader(model="deepset/roberta-base-squad2")
reader.warm_up()

docs = []

def data(question):
    result = reader.run(query=question, documents=docs)

    return [
    a.data
    for a in result.get("answers", [])
    if a.data is not None ]


def get_all():
    # Dictionary to store results from threads
    results = {}

    # Define target function for threads to store results
    def fetch_data(key, question):
        results[key] = data(question)

    # Create threads for each piece of data
    threads = [
        threading.Thread(target=fetch_data, args=("invoiceNumber", "what is the invoice number?")),
        threading.Thread(target=fetch_data, args=("invoiceDate", "what is the invoice date?")),
        threading.Thread(target=fetch_data, args=("dueDate", "what is the due date?")),
        threading.Thread(target=fetch_data, args=("vendorName", "what is the vendor's name?")),
        threading.Thread(target=fetch_data, args=("vendorAddress", "what is the vendor's address?")),
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return results

def runNewOcr():
    # pass full invoice image to the model
    original_image = DocumentFile.from_images('./invoice.png')  # Pass as a list of file-like objects
    original_doc = model(original_image)
    # Extract OCR results
    original_words = original_doc.pages[0].blocks
    merged_content = " ".join(
        word.value
        for block in original_words
        for line in block.lines
        for word in line.words
    )

    docs.append(Document(content=merged_content))
    
    output=get_all()
    docs.clear()
    return output


   




