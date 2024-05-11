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

with open('list_url.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",", 2) for line in stripped if line)
    lines2 = ([line[0], line[1], re.sub(',(?![0-9]|http)', '/qq/', line[2])] for line in lines)
    lines3 = (line + line[2].split(",") for line in lines2)
    lines4 = (line[0:2] + line[3:] for line in lines3)

    lines_1 = (line for line in lines4 if int(line[0]) < 2000)
    with open('list_url_trf.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Year of the report', 'Quarter of the report', 'Company Name', 'Standard Industrial Classification Code', 'Type of Report', 'Central Index Key', 'Report Page', 'Report as Text'))
        writer.writerows(lines_1)

with open('list_url.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",", 2) for line in stripped if line)
    lines2 = ([line[0], line[1], re.sub(',(?![0-9]|http)', '/qq/', line[2])] for line in lines)
    lines3 = (line + line[2].split(",") for line in lines2)
    lines4 = (line[0:2] + line[3:] for line in lines3)

    lines_2 = (line for line in lines4 if (int(line[0]) < 2010 and int(line[0]) >= 2000))
    with open('list_url_trf(2).csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Year of the report', 'Quarter of the report', 'Company Name', 'Standard Industrial Classification Code', 'Type of Report', 'Central Index Key', 'Report Page', 'Report as Text'))
        writer.writerows(lines_2)

with open('list_url.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",", 2) for line in stripped if line)
    lines2 = ([line[0], line[1], re.sub(',(?![0-9]|http)', '/qq/', line[2])] for line in lines)
    lines3 = (line + line[2].split(",") for line in lines2)
    lines4 = (line[0:2] + line[3:] for line in lines3)
    lines_3 = (line for line in lines4 if (int(line[0]) < 2020 and int(line[0]) >= 2015))
    with open('list_url_trf(3).csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Year of the report', 'Quarter of the report', 'Company Name', 'Standard Industrial Classification Code', 'Type of Report', 'Central Index Key', 'Report Page', 'Report as Text'))
        writer.writerows(lines_3)

with open('list_url.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",", 2) for line in stripped if line)
    lines2 = ([line[0], line[1], re.sub(',(?![0-9]|http)', '/qq/', line[2])] for line in lines)
    lines3 = (line + line[2].split(",") for line in lines2)
    lines4 = (line[0:2] + line[3:] for line in lines3)
    lines_3 = (line for line in lines4 if (int(line[0]) < 2015 and int(line[0]) >= 2010))
    with open('list_url_trf(3.5).csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Year of the report', 'Quarter of the report', 'Company Name', 'Standard Industrial Classification Code', 'Type of Report', 'Central Index Key', 'Report Page', 'Report as Text'))
        writer.writerows(lines_3)

with open('list_url.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",", 2) for line in stripped if line)
    lines2 = ([line[0], line[1], re.sub(',(?![0-9]|http)', '/qq/', line[2])] for line in lines)
    lines3 = (line + line[2].split(",") for line in lines2)
    lines4 = (line[0:2] + line[3:] for line in lines3)

    lines_4 = (line for line in lines4 if (int(line[0]) < 2030 and int(line[0]) >= 2020))
    with open('list_url_trf(4).csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Year of the report', 'Quarter of the report', 'Company Name', 'Standard Industrial Classification Code', 'Type of Report', 'Central Index Key', 'Report Page', 'Report as Text'))
        writer.writerows(lines_4)

df = pd.read_csv(r'list_url_trf(4).csv').head(10)
df['Company Name'] = df['Company Name'].apply(lambda x: re.sub('/qq/', ',', x))

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

def create_txt_file(a, b, c, d) :
    filename = "sample/" + str(a) + "_" + str(b) + "_" + str(c)
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
    
df['Sentences'] = df.apply(lambda x : create_txt_file(x['Year of the report'], x["Quarter of the report"], x["Central Index Key"], x['Report as Text']), axis = 1)

def remove_punctuation_sentences (chunks) :
    i = 0
    while i < len(chunks) :
        words = chunks[i].split()
        pattern = r'[a-zA-Z0-9]'

        alphabet_exists = False
        for word in words :
            if re.search(pattern, word) :
                alphabet_exists = True
                break
        if not alphabet_exists :
            chunks.remove(chunks[i])
            i -= 1
        i += 1
    return chunks

def chunking (text) :
    text = text.replace(" \n", "")
    text = text.replace("\n", " ")

    # Process the text
    doc = nlp(text)

    # Extract sentences
    sentences = [sent.text.strip() for sent in doc.sents]
    sentences_cleaned = remove_punctuation_sentences(sentences)

    return sentences_cleaned

df['Chunks of Sentences'] = df.apply(lambda x : chunking(x['Sentences']), axis = 1)

f = open('dictionary.txt', 'r')
content = f.read()
words = content.split(',')
dictionary_esg = [word.strip() for word in words]
print("-----DICTIONARY IMPORTED CORRECTLY-----")
f.close()

def is_word_in_string(word, string):
    # Convert both the word and the string to lowercase (or uppercase)
    word_lower = word.lower()
    string_lower = string.lower()
    
    # Check if the word exists in the string
    if word_lower in string_lower:
        return True
    else:
        return False

def finalize_csv(a, b, c, sentences) :
    relevant_sentences = []

    # Print the extracted sentences
    for i in range(len(sentences)):
        dictio = list()
        relevance = False
        for word in dictionary_esg:
            formula = '[^A-Za-z0-9]+' + word.lower() + '[^A-Za-rt-z0-9]+'
            #if is_word_in_string(word, sentences[i]):
            if re.search(formula, sentences[i].lower()):
                relevance = True
                if not word in dictio : 
                    dictio.append(word)
        if relevance:
            relevant_sentences.append((i, sentences[i], dictio))
        del dictio

    # Open a text file in write mode ('w')
    filename = "sample/" + str(a) + "_" + str(b) + "_" + str(c) + '.txt'
    print("finalizing: " + filename)
    with open(filename, 'w', encoding="utf-8") as file:
        # Write some text to the file
        for sent in relevant_sentences :
            print(sent, file=file)
    
    return relevant_sentences

df['Sentence w/ Relevant Words'] = df.apply(lambda x : finalize_csv(x['Year of the report'], x['Quarter of the report'], x['Central Index Key'], x['Chunks of Sentences']), axis = 1)
df.to_csv("finalized(4).csv")