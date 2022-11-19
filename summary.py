import glob
import urllib.request
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, pipeline, BartForConditionalGeneration

"""
Scraping web article
"""

url = 'https://www.tomshardware.com/features/nvidia-ada-lovelace-and-geforce-rtx-40-series-everything-we-know'

def getArticle(url):
    return requests.get(url).text

for i, link in enumerate(links):
    df = open('article' + str(i) + '.txt', 'w')
    # providing url
    url = link
    # opening the url for reading
    html = urllib.request.urlopen(url)
    # parsing the html file
    htmlParse = BeautifulSoup(html, 'html.parser')
    # getting all the paragraphs
    for para in htmlParse.find_all("p"):
        df.write(para.get_text())
        df.write('\n')
    df.close()

"""
In order to perform the summarization we need to load the objects:
Toknizer and the pre trained model which are in our case the gpt-j-6B.
"""
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")  # "EleutherAI/gpt-j-6B"
model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")  # "EleutherAI/gpt-j-6B"
summarizer = pipeline('summarization', tokenizer=tokenizer, model=model)

"""
Suammrization
"""


def return_summary(summarizer):
    articles = [f for f in glob.glob("*.txt")]
    all_summaries = open("all_summaries.txt", 'w')
    for article in articles:
        try:
            # read the file
            text = Path(article).read_text()
            # call summarizer
            summary_text = summarizer(text, do_sample=False)
            # save sammury
            all_summaries.write(summary_text[0]['summary_text'])
            all_summaries.write('\n')
        except:
            continue
    all_summaries.close()
    """
    Final results
    """
    # read the file
    results_text_input = Path("all_summaries.txt").read_text()
    summary_text_results = summarizer(results_text_input, do_sample=False)
    return summary_text[0]['summary_text']


summary = return_summary(summarizer)

print(summary)