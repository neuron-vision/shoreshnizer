import json
from pathlib import Path as _P
from matplotlib import pyplot as plt 
import re

hebrew_chars = re.compile(r'[^\u0590-\u05FF\s]+')



with open('word_count.json', 'rt') as f:
    sorted_word_count = json.load(f)

sorted_word_count = [(hebrew_chars.sub('', word), count) for word, count in sorted_word_count]


max_freq = max([count for word, count in sorted_word_count])
print(f"Found max freq {max_freq}")

#Prefer size of frequncies.
sorted_word_count = sorted(sorted_word_count, key=lambda x: min(len(x[0]), 7)*50000 + x[1] if x[1] > 30 else x[1], reverse=True)
most_common_words = [word for word, count in sorted_word_count if len(word) > 2]
frequencies = [count for word, count in sorted_word_count if len(word) > 2]
cut_off = 400

# Plot the most common words and their frequencies
plt.figure(figsize=(20, 100))
plt.barh(most_common_words[:cut_off], frequencies[:cut_off])
plt.ylabel('Words')
plt.xlabel('Frequencies')
plt.title(f'Top {cut_off} Most Common Words')
plt.xticks(rotation=90)
plt.title('Weight score of Frequencies and word length')
plt.savefig('words_histogram.png')



