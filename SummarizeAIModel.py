import tkinter as tk 
import nltk 
from textblob import TextBlob
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import re 

nltk.download('punkt')
def summarize():
    url = utext.get('1.0',"end").strip()
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    response =requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    author = "Author not found"
    pub_date = "Publication date not found"

    author_meta = soup.find('meta', attrs={'name': 'author'})
    pub_date_meta = soup.find('meta', attrs={'property': 'article:published_time'})

    if author_meta:
        author = author_meta['content']
    if pub_date_meta:
        pub_date = pub_date_meta['content']
    
    common_author_patterns = ['author','byline','author-name','contributor']
    common_date_patterns = ['pub-date','date','published','publication-date']

    for pattern in common_author_patterns:
        if author == "Author not found":
            author_tag = soup.find(class_=re.compile(pattern,re.I))
            if author_tag:
                author = author_tag.get_text(strip=True)
    
    for pattern in common_date_patterns:
        if pub_date == "Publication date not found":
            pub_date_tag = soup.find(class_=re.compile(pattern, re.I))
            if pub_date_tag:
                pub_date = pub_date_tag.get_text(strip=True)

    title.config(state='normal')
    author_text.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentimental.config(state='normal')

    title.delete('1.0','end')
    title.insert('1.0', article.title)

    author_text.delete('1.0','end')
    author_text.insert('1.0', author)

    publication.delete('1.0','end')
    publication.insert('1.0', pub_date)

    summary.delete('1.0','end')
    summary.insert('1.0', article.summary)

    analysis = TextBlob(article.text)
    sentimental.delete('1.0','end')
    sentimental.insert('1.0', f'polarity:{analysis.polarity},Sentiment:{"positive" if analysis.polarity>0 else "negative" if analysis.polarity<0 else "neural"}')

    title.config(state='disabled')
    author_text.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentimental.config(state='disabled')

root = tk.Tk()
root.title('Text Summarize')
root.geometry('1200x600')

tlabel = tk.Label(root, text="Title")
tlabel.pack()

title = tk.Text(root, height=1, width=160)
title.config(state='disabled',bg='#fff')
title.pack()

alabel = tk.Label(root, text="Author")
alabel.pack()

author_text = tk.Text(root, height=1, width=160)
author_text.config(state='disabled',bg='#fff')
author_text.pack()

plabel = tk.Label(root, text="Publication Date")
plabel.pack()

publication = tk.Text(root, height=1, width=160)
publication.config(state='disabled',bg='#fff')
publication.pack()

slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk.Text(root, height=20, width=160)
summary.config(state='disabled',bg='#fff')
summary.pack()

setlabel = tk.Label(root, text="Sentimental Analysis")
setlabel.pack()

sentimental = tk.Text(root, height=1, width=160)
sentimental.config(state='disabled',bg='#fff')
sentimental.pack()

ulabel = tk.Label(root, text="URL")
ulabel.pack()

utext = tk.Text(root, height=1, width=160)
utext.pack()

btn = tk.Button(root, text='Summarize', command=summarize)
btn.pack()

root.mainloop()



