from services.invoice_ocr import get_block
from services.detect_vendor import getVendorName
from haystack import Document
from haystack.components.readers import ExtractiveReader
import threading


reader = ExtractiveReader(model="deepset/roberta-base-squad2")
reader.warm_up()

docs = []



def data(question):
    result = reader.run(query=question, documents=docs)

    answers = [
        a.data
        for a in result.get("answers", [])
        if a.data is not None
    ]
    
    # Return the first answer if it exists, else return None
    return answers[0] if answers else None


def get_all():
    choice = getVendorName()
    # Dictionary to store results from threads
    results = {}
    results['vendorName']= choice
    # Define target function for threads to store results
    def fetch_data(key, question):
        results[key] = data(question)

    # Create threads for each piece of data
    threads = [
        threading.Thread(target=fetch_data, args=("invoiceNumber", "what is the number of the invoice or code of the invoice number ?")),
        threading.Thread(target=fetch_data, args=("invoiceDate", "what is the invoice date?")),
        threading.Thread(target=fetch_data, args=("dueDate", "what is the due date?")),
        threading.Thread(target=fetch_data, args=("poNumber", "what is the PO number or PO # ?")),
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
   
    return results
  

def getInfo():
    original_words = get_block()
    merged_content = " ; ".join(
        " ".join(word.value for word in line.words)
        for block in original_words
        for line in block.lines
        
    )

    docs.append(Document(content=merged_content))
    
    # Extract OCR results
    
    output=get_all()
    docs.clear()
    return output



   




