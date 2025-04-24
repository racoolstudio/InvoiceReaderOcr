from services.invoice_ocr import get_block
from services.table import extract_text
import difflib
from haystack.components.readers import ExtractiveReader
from haystack import Document
import re
import threading




reader = ExtractiveReader(model="deepset/roberta-base-squad2")
reader.warm_up()

blocks = ""
lines=[ ]

def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

def word_similarity(word1, word2):
    return difflib.SequenceMatcher(None, word1, word2).ratio()

def investigate(fInvIndex):
    firstChoice =''
    secondChoice = ''
    global lines,blocks
    if fInvIndex == 0:
        firstChoice=extract_text(lines[1]['line'])
        secondChoice=extract_text(lines[2]['line'])
    elif fInvIndex<0 or fInvIndex > 3:
        firstChoice=extract_text(lines[0]['line'])
        secondChoice=extract_text(lines[1]['line'])
    else :
        firstChoice=extract_text(lines[int(fInvIndex)-1]['line'])
        secondChoice=extract_text(lines[int(fInvIndex+1)]['line'])
    
    firstChoice = remove_special_characters(firstChoice)
    secondChoice = remove_special_characters(secondChoice)
    docs = [Document(content=f"{firstChoice}  , {secondChoice}")]
    question = "give me just the best company name"
    result = reader.run(query=question, documents=docs)
    answers = [
        a.data
        for a in result.get("answers", [])
        if a.data is not None
    ]

    return answers[0]

def getVendorName():
    global lines,blocks

    blocks = get_block()

    lines=[
        {"line": [{"value": word.value,"geometry":word.geometry} for word in line.words]}
        for block in blocks
        for line in block.lines          
    ]
    fInvIndex=-1
    fInvyaxes = 0
    for l in lines[0:10]:  
        text = extract_text(l['line'])
        if word_similarity(text.upper(),"INVOICE") > 0.5:
                fInvIndex = int(lines.index(l))
                fInvyaxes = float(l['line'][0]['geometry'][0][1])
                break

    
    return investigate(fInvIndex)

