#!/usr/bin/env python
# coding: utf-8

import re
import thulac
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# 2.cleaning the punctuation mark and dividing into sentence.
def pandasreadTxt(pathTxt):
    csvframe = pd.read_table(pathTxt, sep="\n",encoding='UTF_8')
    csvframe.columns = ['x']
    csvframe['y'] = None
    sentencesList = []
    for i in range(len(csvframe)):
        coordinate = csvframe['x'][i]
        coordinate = coordinate.replace('「', '').replace('」', '')
        sentencesList.append(coordinate)
    return sentencesList

#3.Chinese Word Segmentation and label the type of word. 分词及词性分析：进行中文分词和标注词的类型；
def thulac_use(myList):
    th = thulac.thulac()
    all_list = []
    for str in myList:
        res = th.cut(str,text=True)# word segmentation
        word_list = re.split(' ', res)#word segmentation through space.
        all_list.append(word_list)
    return all_list

#4.Select idioms (i) to analyse semantic annotation; 选择习语（i）进行语义标注分析；
def select_i(all_list):
    word_i_list = []
    for word_list in all_list:
        for word in word_list:
            if '_i' in word:
                word_i_list.append(word)
                str = re.sub("[A-Za-z0-9\!\%\[\]\,\。\_]", "", word)
    return word_i_list

#5.select the noun, verb, adjustive and adverb,generate the word frequency and wordcloud.选择名词、动词、形容词和副词计算词频进行分析；
def select_word(all_list):
    word_v_List = []
    for word_list in all_list:
        for i in range(len(word_list)):
            if '_n' in word_list[i] or '_v' in word_list[i] or '_a' in word_list[i] or '_d' in word_list[i]:
                str = re.sub("[A-Za-z0-9\!\%\[\]\,\。\_]", "", word_list[i])
                word_v_List.append(str)
    # print(word_v_List) 
    counts = {}
    for word in word_v_List:
        if '\u4e00' <= word <= '\u9fff':
            counts[word] = counts.get(word, 0) + 1

    words_frequency = list(counts.items())
    words_frequency.sort(key=lambda x: x[1], reverse=True)
    print(words_frequency)  #words_frequency:Save the word frequency statistics after sorting
    wordstext = " ".join(word_v_List)
    image_WC = WordCloud(background_color='white',  # Blaceground color
        width=600,  
        height=420,  
        font_path='SIMHEI.TTF',  
        margin=1  
    ).generate(wordstext)
    plt.imshow(image_WC)
    plt.axis("off")
    plt.show()
    # tmpWC.to_file('词云图{}.png'.format(wordType)) 生成词云图，用词云图进行数据可视化的结果展示      

#1.read the text 读取文本：Python读取诸子百家的数字文本
if __name__ == '__main__':
    tmpList = pandasreadTxt("Fajia.txt")
    # print(tmpList)
    #zheyeList = select(tmpList)
    all_list = thulac_use(tmpList)
    word_i_list = select_i(all_list)
    word_vb_List = select_word(all_list)

    print(all_list)
    print(word_i_list)

