import pandas as pd
import re
# import torch
import time
from collections import defaultdict
# from io import BytesIO
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Perform OCR using Doctr
model = ocr_predictor(pretrained=True)

def get_lines_Ocr():
    try:
        original_image = DocumentFile.from_images('C:\\Users\\Ridwan\\Downloads\\projectOcr\\tests\\invoices\\inv1.png')  # Pass as a list of file-like objects
        original_doc = model(original_image)
        # Extract OCR results
        original_words = original_doc.pages[0].blocks
        original_lines = [
            {"line": [{"value": word.value,"geometry":word.geometry} for word in line.words]}
            for block in original_words
            for line in block.lines          
        ]
        
        return original_lines

    except ValueError as ve:
        raise ValueError(f"Error processing OCR: {ve}")
   


def extract_text(line):
    return " ".join(word["value"] for word in line)

def extract_text_qty(line):
    return line[0]["value"]


  
def check_quantity_name():
    if "QUANTITY" in headers.keys():
        return "QUANTITY"
    elif "QTY" in headers.keys():
        return "QTY"

def check_quantity():
    if "QUANTITY" in headers.keys():
        return int(headers["QUANTITY"])
    elif "QTY" in headers.keys():
        return int(headers["QTY"])

def check_description():
    if "DESCRIPTION" in headers.keys():
        return int(headers["DESCRIPTION"])
    elif "DESC" in headers.keys():
        return int(headers["DESC"])

def check_unit_price():
    if "UNIT PRICE" in headers.keys():
        return int(headers["UNIT PRICE"])
   
    elif "PRICE" in headers.keys():
        return int(headers["PRICE"])

def get_header_details():
    headers_list = {}
    for line in lines:
        y_value = line['line'][0]['geometry'][0][1]
        if abs( y_header[0] - y_value) <= 0.01:
            headers_list[extract_text(line['line']).upper()]={
                'x_min':line['line'][0]['geometry'][0][0],
                'x_max':line['line'][0]['geometry'][1][0],
                'index':lines.index(line)
            }
    return headers_list

def horizontal_overlap(x1, x2, a1, a2, left_tolerance=0.05, right_tolerance=0.05): 
    return (x1 - left_tolerance) <= a2 and (x2 + right_tolerance) >= a1

def clean_text(header,line):
    if header == "PRICE" or header == "UNIT PRICE":
        return line['line'][0]["value"]
    elif header == "QUANTITY" or header == "QTY":
        try:
            int(line['line'][0]["value"])
            return line['line'][0]["value"]
        except:
            return ''
    else:
        return extract_text(line['line'])

def clean_table(table_data):
    for header in table_data:
        table_data[header] = [value.strip() for value in table_data[header] if value.strip()]
    return table_data

def get_final_table(table_data):
    real_data= len(table_data[check_quantity_name()])
    final_table = {header: table_data[header][:real_data] for header in table_data if header in default_headers} 
    return final_table

def get_data_header(start_index): 
    table = {header_text: [] for header_text in header_info}
    for line in lines[start_index:]:
        row_values = {header_text: "" for header_text in header_info}
        if extract_text(line['line']).upper() == "SUBTOTAL":
            break
        for header in header_info:
            # If the cell's x coordinate falls within header range (with tolerance)
            try :
                line['line'][1]
                if horizontal_overlap(header_info[header]['x_min'], header_info[header]['x_max'], line['line'][1]['geometry'][0][0], line['line'][1]['geometry'][1][0]):
                    row_values[header] = clean_text(header,line)
                else:        
                    if horizontal_overlap(header_info[header]['x_min'], header_info[header]['x_max'], line['line'][0]['geometry'][0][0], line['line'][1]['geometry'][1][0]):
                        row_values[header] = clean_text(header,line)
                        
            except: 
                if horizontal_overlap(header_info[header]['x_min'], header_info[header]['x_max'], line['line'][0]['geometry'][0][0], line['line'][0]['geometry'][1][0]):
                    row_values[header] = clean_text(header,line)
                    break
            
        # Append the extracted cell values for this row into the table dictionary.
        for header_text in table:
            table[header_text].append(row_values[header_text])
    return table

def q_d_p():
    if check_description() and check_quantity() and check_unit_price():
        data_start_index = list(header_info.values())[-1]["index"] + 1
        table=get_data_header(data_start_index)
        table_cleaned=clean_table(table)
        final_table = get_final_table(table_cleaned)
        print(final_table)
               
    else:
        print("Headers not found")


lines = get_lines_Ocr()
default_headers=["QUANTITY","QTY","DESCRIPTION", "UNIT PRICE","PRICE", "DESC"]
headers = {}
y_header=[]

for l in lines:  
    text = extract_text(l['line'])
    if text.upper() in {"QUANTITY","QTY","DESCRIPTION", "UNIT PRICE","PRICE", "DESC"}:
        if text not in headers.keys():
            headers[text.upper()] = lines.index(l)
            y_header.append(l['line'][0]['geometry'][0][1])

header_info = get_header_details()
list_header = list(header_info.keys())
desc_index = list_header.index("DESCRIPTION")
before_desc_index =''

if desc_index == 0:
    before_desc_index=''
elif desc_index == len(list_header)-1:
    before_desc_index=desc_index-1
else:
    before_desc_index=desc_index-1
    
    
q_d_p()

