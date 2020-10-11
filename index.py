#importing libraries
import re
import nltk ,requests
from bs4 import BeautifulSoup
from collections import Counter
from docx import Document
import pandas as pd
import matplotlib.pyplot as plt

#get url  from user
url = input("Enter url :")
full_url = 'http://'+url
new_url = full_url.replace("www.", "")

#new_url = 'http://quotes.toscrape.com'
page = requests.get(new_url)

#extract content of the page
soup = BeautifulSoup(page.content, 'html.parser')

#extract all text from span tag
quote = soup.find_all('span', attrs={'class':'text'})

#remove double quotes from list
quotes = [q.text.replace('“', '').replace('”', '') for q in quote]

#combine all strings of list
s = ' '
s = s.join(quotes)

#remove special characters
bad_chars = [';', ':', '!', ".","*",",","-"]
s = ''.join(i for i in s if not i in bad_chars)

#extract words in token
wList = word_tokenize(s)
print(wList)

#list of stopwords
stop_words = set(stopwords.words('english'))

wordList = [word for word in wList if not word in stop_words]
print(wordList)

#get a words type
word_type = nltk.pos_tag(wordList)
print(len(word_type))

#get a word type with frequency
counts = Counter( (word,tag) for word, tag in word_type)
print(sum(counts.values()))

#create a list of word and count with 100 most common words
Word_And_Type= []
Count = []
Word = []
Type = []
for w, c in counts.most_common(100): 
    Word_And_Type.append(w)
    Count.append(c)

#break a tuple into two part
for w, t in Word_And_Type:
    Word.append(w)
    Type.append(t)
    
#create a zip of word, type, and count
allData = zip(Word, Type, Count)

#create a document page
document = Document()
print(document)

#create a table in document
 table = document.add_table(rows=1, cols=3)
 
#table cells
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Word'
hdr_cells[1].text = 'Type'
hdr_cells[2].text = 'Count'

#fill data in cells
for word, typ, count in allData:
    row_cells = table.add_row().cells
    row_cells[0].text = word
    row_cells[1].text = typ
    row_cells[2].text = str(count)
    
document.add_page_break()

#save a file in docx format
document.save('demo.docx')

#Create frequency histogram of 50 most common words a
fd = nltk.FreqDist(wordList)
fd.plot(20)

#Create DataFrame
 df = pd.DataFrame({"Word":Word,"Type":Type,"Count":Count})

#plotting a graph
plt.plot(df.Word, df.Count,color='green')
plt.xlabel('Word')
plt.ylabel('Count')