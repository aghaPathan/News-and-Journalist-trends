import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os
from nltk import pos_tag
from collections import Counter
import operator
import math
import random
from nltk.corpus import stopwords
import time



def refine_raw_data(filename):
    filename_out = filename.strip('.rawtext')+str('.txt')
    data = open(filename, 'r')
    data = data.read()
    data = ' '.join(data.split())


    stopWords = set(stopwords.words('english'))

    filtered = ''
    sentence = ''
    for x in data:
        if x != '.':
            sentence = sentence + x
        if x == '.':
            filtered = filtered + check(sentence,stopWords) + '\n'
            sentence = ''

    data_out = open(filename_out, 'w+')
    data_out.write(filtered)
    data_out.close()
    print(filtered)

def check(sentence,stopWords):
    temp = ''
    for x in sentence.split():
        if x in stopWords:
            pass
        if x not in stopWords:

            temp = temp + str(x) + ' '

    return temp

def data_mining(filename):
    filename_out = filename.strip('.txt') + str('.out')
    command = ["./apriori", '-n1', filename, filename_out]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(1)
    nano_filter_function(filename_out)



def nano_filter_function(filename_out):
    f_nano = open(filename_out, 'r')
    temp = f_nano.read()

    temp = temp.split('\n')

    for x in temp:
        write_data(x)
    # nano_filter = ''
    # for x in range(len(temp)):
    #     if x % 2 == 0:
    #         if temp[x] in ['The', 'the', '"', '"The'] or temp[x].endswith("'s") or temp[x].isalpha() ==False:
    #             pass
    #         else:
    #             nano_filter += temp[x]
    #             nano_filter += ' '
    #             nano_filter += temp[x + 1] + '\n'

    f_nano.close()
    #write_data(nano_filter)


def write_data(data):

    grand = open(grand_out, 'a+')
    grand.write(str(data) + '\n')
    grand.close()


def mined_words(file):
    f = open(file, 'r')
    temp = f.read()
    temp = temp.split()
    words = []
    magnitudes = []

    for x in range(len(temp)):
        if x % 2 == 0:
            words.append(temp[x])
        if x % 2 != 0:
            magnitudes.append(float(temp[x].strip('()')))

    return words, magnitudes


def filter_words(words):

    temp = pos_tag(words, tagset='universal')

    pos_filter = ['ADJ', 'NOUN']
    words_filtered = []
    for i in range(len(temp)):

        if temp[i][1] in pos_filter:
            words_filtered.append(temp[i][0].strip('"'))
        else:
            pass

    return words_filtered

def words_in_files(filename, words_filtered):

    o = open(filename, 'r')
    total = o.read()
    total = total.split()
    freq = []
    for x in total:
        if x in words_filtered:
            freq.append(x)
    return tuple(freq)


def words_count(freq):
    frequency = dict(Counter(freq))
    return frequency

def strip_data(frequency):
    words2process = round(len(frequency) * 70 / 100)

    i = 0
    plot_words_in_occurrence = {}
    plot_words_in_support = {}
    for key, value in frequency.items():

        if i >= words2process:
            plot_words_in_occurrence[key] = value

            plot_words_in_support[key] = float()
        i += 1

    plot_words_in_support = process_strip_data(plot_words_in_support)
    final_dict = get_percent(plot_words_in_support,plot_words_in_occurrence)

    return final_dict

def process_strip_data(plot_words_in_support):
    f = open(grand_out, 'r')
    temp = f.read()
    temp = temp.split()

    for x in range(len(temp)):
        if x % 2 == 0:
            if temp[x] in plot_words_in_support.keys():
                catch = plot_words_in_support[temp[x]] + float(temp[x + 1].strip('()'))
                plot_words_in_support[temp[x]] = catch

    return plot_words_in_support

def get_percent(plot_words_in_support,plot_words_in_occurrence):
    final_dict = {}

    for key, value in plot_words_in_support.items():
        final_dict.update({key: value * 70 / 100})

    for key, value in final_dict.items():
        if key in plot_words_in_occurrence:
            temp = (plot_words_in_occurrence[key] * 30 / 100) + value
            final_dict[key] = round(temp)


    final_dict = dict(sorted(final_dict.items(), key=operator.itemgetter(1)))

    return final_dict


def get_coordinates(final_dict):

    text = []
    area = []
    for key, value in final_dict.items():
        text.append(key)
        area.append((2 * math.pi * value) * 25)


    y = []
    for key, value in final_dict.items():
        y.append(value)

    x = random.sample(range(len(y)), len(text))

    return text, area, x , y



def basic_bubble(x,y,text,area):

    grand_png = grand_out.strip('.out')+str('.png')

    for i in range(len(text)):
        #print(text[i])
        plt.text(x[i], y[i], str(text[i]), horizontalalignment='center')


    # making the scatter plot
    plt.scatter(x, y, s=area, linewidths=2, edgecolor='w')

    # axis([0,11,200,1280])
    plt.title("WORDS USED IN TODAY'S NEWS")
    plt.xlabel('Number Of Bubbles')
    plt.ylabel('Magnitude')


    plt.savefig(grand_png, format='png', dpi=1000)
    #plt.yticks([])
    #plt.xticks([])
    plt.show()
    plt.clf()


if __name__ == "__main__":

    directory = "/home/agha/Sir Naeem/"


    ############################### Grand OutPut File ###################################
    global grand_out
    grand_out = 'grand_data.out'


    ############################## IF GRANDE OUTPUT EXSIST ###############################

    if grand_out in os.listdir(directory):
        os.remove(grand_out)



    ################################## Data Refine #######################################

    for filename in os.listdir(directory):

        if filename.endswith(".rawtext"):
            refine_raw_data(filename)
            continue
        else:
            continue



    ################################## Data Mining #######################################

    for filename in os.listdir(directory):

        if filename.endswith(".txt"):
            data_mining(filename)
            continue
        else:
            continue

    ########################## Getting Words and their Magnitudes ##########################
    words, magnitudes = mined_words(grand_out)
    words_filtered = filter_words(words)



    ################### Checking number of Filtered Words in News Files ####################
    freq = ()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            temp = ()
            temp = words_in_files(filename,words_filtered)
            freq = freq + temp


    #################### Getting Count per Filtered Word as a Dictionary ####################
    frequency = words_count(freq)
    frequency = dict(sorted(frequency.items(), key=operator.itemgetter(1))) #Sorting


    #################### Getting Words in occurrence & Support Separate #######################

    final_dict = strip_data(frequency)


    #######################   Get PLotting Coordinates  ###################################

    text , area, x ,y= get_coordinates(final_dict)



    ######################### Plotting the Coordinates ###########################

    basic_bubble(x,y,text,area)

































