import json
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from wordcloud import WordCloud


class ChatStatistics:
    def __init__(self, json_file: Union[str, Path]):
        with open(json_file, encoding='utf8') as f:
            self.json_file = json.load(f)
        self.normalizer = Normalizer()

        stop_words = open('src/data/stopwords.txt', encoding='utf8').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))

    def generate_tag_cloud(self):
        text_content = ''
        for msg in self.json_file['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item : item not in self.stop_words, tokens))
                text_content += f" {' '.join(tokens)}"

        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)
        tokens = word_tokenize(text_content)

        wordcloud = WordCloud(font_path='src/data/BKoodkBd.ttf', width=800, height=600,
                            background_color='white').generate(text_content)
        wordcloud.to_file('tagcloud.png')

if __name__ == "__main__":
    chat_stats = ChatStatistics(json_file='src/data/result.json')
    chat_stats.generate_tag_cloud()
    print('Done!')