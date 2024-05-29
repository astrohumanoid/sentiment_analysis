import numpy as np
import pandas as pd
import csv
import re
import requests
from html.parser import HTMLParser as htmlpar
from bs4 import BeautifulSoup
import html2text
import html
import spacy

# Load English language model
nlp = spacy.load('en_core_web_sm')
print("-----LIB IMPORTED CORRECTLY-----")

df = pd.read_csv(r'list_url_trf(1993).csv')
df['Company Name'] = df['Company Name'].apply(lambda x: re.sub('/qq/', ',', x))
df.index.name = 'index_name'
df_reset = df.reset_index()

def remove_punctuation_words(text):
    words = text.split()
    pattern = r'[a-zA-Z0-9]'

    i = 0
    while i < len(words) :
        if not re.search(pattern, words[i]) :
            words.remove(words[i])
            i -= 1
        i += 1
    cleaned_text = " ".join(words)
    return cleaned_text

def create_txt_file(id, a, b, c, d, after_id) :
    if(id > after_id) :
        filename = "sample/1993/" + str(id) + "_" + str(a) + "_" + str(b) + "_" + str(c)
        print("processing: " + filename)
        f = open(filename + '_parsed.txt', "w+", encoding = "utf-8")
        headers = {
            'User-Agent': 'TUM ge47cel@tum.de',
            'Accept-Encoding' : 'gzip, deflate',
            'Host' : 'www.sec.gov'
        }
        x = requests.get(d, headers=headers)
        text = x.text
        text = html.unescape(text)
        document_begin = text.find("<DOCUMENT>")
        document_end = text.find("</DOCUMENT>") + 11
        text = text[document_begin:document_end]

        a = html2text.html2text(text)
        a = remove_punctuation_words(a)
        a = re.sub(r'\*{2,}', '', a)
        #formula = r'(?i)Item 2[^A-Za-z0-9]+\s?\n?(Description of )?Propert(y|ies)'
        #formula = r'(?i)Item 1[^A-Za-z0-9]+\s?\n?(?:Description of )?Business'
        formula = r'(?i)(?:Item[^A-Za-z0-9]*\s?\n?1[^A-Za-z0-9]*\s?\n?(?:Description of )?Business)(.*)(?:Item[^A-Za-z0-9]*\s?\n?2[^A-Za-z0-9]*\s?\n?(Description of )?Propert(y|ies))'
        match = re.search(formula, a, re.DOTALL)
        if match:
            extracted_text = match.group(1)
            formula2 = r'(?i)(?:Item[^A-Za-z0-9]+\s?\n?1[^A-Za-z0-9]+\s?\n?(?:Description of )?Business)(.*)'
            match2 = re.search(formula2, extracted_text, re.DOTALL)
            if match2:
                extracted_text2 = match2.group(1)
                f.write(extracted_text2)
                f.close()
                return extracted_text2
            else :
                f.write(extracted_text)
                f.close()
                return extracted_text
        else:
            return "Pattern not found"
    
df['Sentences'] = df_reset.apply(lambda x : create_txt_file(x['index_name'], x['Year of the report'], x["Quarter of the report"], x["Central Index Key"], x['Report as Text'], 1), axis = 1)