import json

import numpy as np
import pandas as pd
import random

import spacy
import en_core_web_sm
import pyinflect

import gensim.downloader as api
from sentence_splitter import SentenceSplitter

# малая модель spacy
nlp = en_core_web_sm.load()

# малая модель glove wiki
# внимание - очень долго скачивает, если она еще не установлена
model = api.load("glove-wiki-gigaword-100")


class EnglishEx:
    def __init__(self, count, txt):
        
        self.count = count
        self.txt = txt
        self.df = self.df_maker()
        self.df_type = self.type_ex(self.df)
    
    def df_maker(self):
        
        df = pd.DataFrame()
        
        #Сплитим на предложения
        splitter = SentenceSplitter(language='en')
        split_sentence = splitter.split(self.txt) 

        #Cоздаем датафрейм
        sentences = pd.DataFrame(split_sentence) 

        #Удаляем пропуски
        sentences = sentences[sentences != '']
        sentences = sentences.dropna()

        df['sentences'] = sentences[0]
        df = df.sample(self.count)
        df = df.reset_index(drop=True)

        #Токенизация
        for i in range(len(df)):
            df['sentences'][i] = nlp(df['sentences'][i])

        df['object'] = None
        df['options'] = None
        df['answer'] = None
        df['describe'] = None 
        df['result'] = None
        df['total'] = 0
        
        for i in range(len(df['result'])):
            df['result'][i] = ['']
        #Колонки с заданиями и описанием
        types_excercies = ['select_word', 'missing_word', 'select_sent', 'tobe_verb', 'delete_word']

        random_dict = [{'type': random.choice(types_excercies)} for _ in range(len(df))]
        random_dict = pd.DataFrame(random_dict)
        df['type'] = random_dict['type']

        
        df = df.reset_index(drop=True)
        
        return df
        
        
    def select_word(self, row): #Упражнение 1
    
        sent = row['sentences']
        options = []
        word = sent[random.randint(0,len(sent) - 1)]

        for i in range(len(sent)):
            if word.pos_ not in ['NOUN', 'VERB', 'ADV', 'ADJ']:
                word = sent[random.randint(0,len(sent) - 1)]
            else:
                break

        options.append(word)
        options.append(model.most_similar(word.text.lower())[-1][0])
        options.append(model.most_similar(word.text.lower())[-2][0])
        options = [str(x) for x in options]
        options.insert(0, '---')
        
        list_text = []
        for token in sent:
            if token == word:
                list_text.append('___')
            else:
                list_text.append(token.text)

        doc = ' '.join(list_text) 
        
        row['sentences'] = doc
        row['object'] = word.text
        row['options'] = options
        row['answer'] = word.text
        row['describe'] = 'Выберите слово'

        return row
    
    def missing_word(self, row): #Упражнение 2

        sent = row['sentences']
        options = []
        word = sent[random.randint(0,len(sent) - 1)]
        word 

        for i in range(len(sent)):
            if word.pos_ not in ['NOUN', 'VERB', 'ADV', 'ADJ']:
                word = sent[random.randint(0,len(sent) - 1)]
            else:
                break

        list_text = []
        for token in sent:
            if token == word:
                list_text.append('___')
            else:
                list_text.append(token.text)

        doc = ' '.join(list_text)


        row['sentences'] = doc
        row['object'] = word.text
        row['options'] = ''
        row['answer'] = word.text
        row['describe'] = 'Заполните пропуск'

        return row
    
    
    def delete_word(self, row): #Упражнение 3

        sent = row['sentences']
        options = []
        word = sent[random.randint(0,len(sent) - 1)]

        for i in range(len(sent)):
            if word.pos_ not in ['NOUN', 'VERB', 'ADV', 'ADJ']:
                word = sent[random.randint(0,len(sent) - 1)]
            else:
                break

        list_text = []
        for token in sent:
            if token == word:
                answer = model.most_similar(word.text.lower())[0][0]
                list_text.append(answer)
                list_text.append(token.text)     
            else:
                list_text.append(token.text)

        doc = ' '.join(list_text)

        
        i = 0
        while i != 2:
            option_ = sent[random.randint(0,len(sent) - 1)]
            if option_.pos_ in ['NOUN', 'VERB', 'ADV', 'ADJ']:
                option_ = sent[random.randint(0,len(sent) - 1)]
            if option_ != word:
                options.append(option_)
                i += 1

        options.append(answer)
        options = [str(x) for x in options]
        options.insert(0, '---')
        
        
        row['sentences'] = doc
        row['object'] = word.text
        row['options'] = options
        row['answer'] = answer
        row['describe'] = 'Выбери лишние слово'

        return row

    def select_sent(self, row): #Упражнение 4
    
        sent = row['sentences']    
        new_sent_1, new_sent_2 = sent.text, sent.text
        options = []


        i=5
        for token in sent:
            if token.pos_ in ['NOUN', 'VERB', 'ADV', 'ADJ']:
                m, n = np.random.randint(0, i, 2)

                new_word_1 = model.most_similar(token.text.lower(), topn=i)[m][0]
                new_word_2 = model.most_similar(positive = [token.text.lower(), 'bad'],
                                                negative = ['good'],
                                                topn=i)[n][0]

                new_word_1 = new_word_1.title() if token.text.istitle() else new_word_1
                new_word_2 = new_word_2.title() if token.text.istitle() else new_word_2

                new_sent_1 = new_sent_1.replace(token.text, new_word_1)
                new_sent_2 = new_sent_2.replace(token.text, new_word_2)

        options.append(sent.text)
        options.append(new_sent_1)
        options.append(new_sent_2)
        options = [str(x) for x in options]
        options.insert(0, '---')
        
        row['sentences'] = ''
        row['object'] = sent.text
        row['options'] = options
        row['answer'] = sent.text
        row['describe'] = 'Выбери правильное предложение'

        return row
    
    def tobe_verb(self, row, df): #Упражнение 5
        sent = row['sentences']
        options = []
        word = ''

        for s in sent:
            if s.lemma_ == 'be':
                word = s
        
#         if word == '':
#             for sent in df['sentences'].sample(15):
#                 for s in sent:
#                     if s.lemma_ == 'be':
#                         word = s
#                         sent = sent
#                 try:
#                     if word.text != '':
#                         break
#                 except:
#                     if word != '':
#                         break
        if isinstance(word, str):
            if word == '':
                row = self.select_word(row)
                row['type'] = 'select_word'
                return row
        
        list_text = []
        for token in sent:
            if token.text == word.text:
                list_text.append('___')
            else:
                list_text.append(token.text)

        doc = ' '.join(list_text)  

        options.append(word)
        options.append(model.most_similar(word.text)[random.randint(0, 6)][0])
        options.append(model.most_similar(word.text)[random.randint(0, 6)][0])
        
        
        
        if options[1] == options[2]:
            options[2] = model.most_similar(word.text)[random.randint(0, 6)][0]
            
        options = [str(x) for x in options]
        options.insert(0, '---')
        
        row['sentences'] = doc
        row['object'] = word.text
        row['options'] = options
        row['answer'] = word.text
        row['describe'] = 'Выбери правильную форму глагола'

        return row       
    
    def type_ex(self, df):

        for i in range(len(df)):
            if df['type'][i] == 'tobe_verb':
                df.loc[i] = self.tobe_verb(df.loc[i], df)
            elif df['type'][i] == 'missing_word':
                df.loc[i] = self.missing_word(df.loc[i])   
            elif df['type'][i] == 'select_sent':
                df.loc[i] = self.select_sent(df.loc[i])
            elif df['type'][i] == 'select_word':
                df.loc[i] = self.select_word(df.loc[i])
            else:
                df.loc[i] = self.delete_word(df.loc[i])

        return df 
    
