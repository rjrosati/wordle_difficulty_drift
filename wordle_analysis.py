import pandas as pd
import os
from collections import Counter
import matplotlib.pyplot as plt


answers_file = 'wordle_answers.csv'
answers_url = 'https://wordsrated.com/tools/wordsfinder/past-wordle-answers/'


if not os.path.exists(answers_file):
    print(f"{answers_file} not found, rescraping word list...")
    from bs4 import BeautifulSoup
    from selenium import webdriver
    browser = webdriver.Firefox()
    browser.get(answers_url)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source,features='html.parser')

    nums, words = [], []
    wordlis = soup.find_all('li', {'class': 'wordle-item'})
    for wordli in wordlis:
        txt = wordli.get_text().split(' ')
        nums.append(int(txt[2]))
        words.append(txt[-1].strip().lower())
    df = pd.DataFrame(words[::-1], columns=['answers'])
    df.to_csv(answers_file)
    print(f"New wordlist saved in {answers_file}")

df = pd.read_csv(answers_file)


# see https://wordsrated.com/letter-frequency-in-english/
letterfreqs_eng5letters = {
    'a': 7.57e-2,
    'b': 1.84e-2,
    'c': 4.09e-2,
    'd': 3.38e-2,
    'e': 11.51e-2,
    'f': 1.23e-2,
    'g': 2.7e-2,
    'h': 2.32e-2,
    'i': 9.01e-2,
    'j': 0.16e-2,
    'k': 0.85e-2,
    'l': 5.31e-2,
    'm': 2.84e-2,
    'n': 6.85e-2,
    'o': 6.58e-2,
    'p': 2.94e-2,
    'q': 0.16e-2,
    'r': 7.07e-2,
    's': 9.52e-2,
    't': 6.68e-2,
    'u': 3.27e-2,
    'v': 0.98e-2,
    'w': 0.74e-2,
    'x': 0.29e-2,
    'y': 1.63e-2,
    'z': 0.47e-2,
}
letterfreqs = {chr(i): [] for i in range(97,97+26)}
days_in_chunk = 60
for i in range(len(df.answers)//days_in_chunk):
    # break words into letters and histogram
    ans_in_month = df.answers.iloc[i:i+days_in_chunk].str.cat(sep='')
    letterhist = Counter(ans_in_month)
    for c in letterfreqs.keys():
        if c in letterhist.keys():
            letterfreqs[c].append(letterhist[c] / len(ans_in_month))
        else:
            letterfreqs[c].append(0.0)

import numpy as np
xarr = np.array(list(range(len(df.answers)//days_in_chunk)))*days_in_chunk
plt.plot(xarr, letterfreqs['s'], label = 's', color='C0')
plt.hlines(letterfreqs_eng5letters['s'],xarr[0],xarr[-1], color='C0')
plt.plot(xarr, letterfreqs['t'], label = 't', color='C1')
plt.hlines(letterfreqs_eng5letters['t'],xarr[0],xarr[-1], color='C1')
plt.plot(xarr, letterfreqs['e'], label = 'e', color='C2')
plt.hlines(letterfreqs_eng5letters['s'],xarr[0],xarr[-1], color='C2')
plt.plot(xarr, letterfreqs['a'], label = 'a', color='C3')
plt.hlines(letterfreqs_eng5letters['a'],xarr[0],xarr[-1], color='C3')
plt.plot(xarr, letterfreqs['r'], label = 'r', color='C4')
plt.hlines(letterfreqs_eng5letters['r'],xarr[0],xarr[-1], color='C4')
plt.xlabel('')
plt.legend()
plt.show()

