

import os
import time
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import subprocess
from collections import Counter
import collections
import math
import matplotlib.pyplot as plt
import numpy as np

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
    #print(filtered)

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
    command = ["./apriori", num_of_words, filename, filename_out]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(1)
    nano_filter_function(filename_out)



def nano_filter_function(filename_out):

    f_nano = open(filename_out, 'r')
    temp = f_nano.read()

    temp = temp.split('\n')

    for x in temp:
        write_data(x)

    f_nano.close()


def write_data(data):

    grand = open(grand_out, 'a+')
    grand.write(str(data) + '\n')
    grand.close()


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def create_dict(output_words=5):


    f = open(grand_out, 'r')
    temp = f.read()
    temp = temp.split('\n')
    element = []
    key = ''
    value = 0
    day_dict = {}

    for x in temp:
        element = x.split()
        for y in element:
            if y != element[-1]:
                if y is element[-2]:
                    key = str(key) + str(y)
                else:
                    key = str(key) + str(y) + ' '

            if y == element[-1]:
                value = y.strip('()')
                day_dict[key] = value
                key = ''
                value = 0

    for key, value in day_dict.items():
        if '"' in key or 'The' in key:
            day_dict =removekey(day_dict, key)


    #day_dict = trim_dict(day_dict)
    #print(day_dict)
    day_dict = dict(Counter(day_dict).most_common(output_words))  #### getting just top 7 elements in dict
    return day_dict




def trim_dict(day_dict):
    td = {}
    for key, value in day_dict.items():
        if '1' in num_of_words:
            if len(key.split()) == 1:
                td[key] = value

        if '2' in num_of_words:
            if len(key.split()) == 2:
                td[key] = value

        if '3' in num_of_words:
            if len(key.split()) == 3:
                td[key] = value

    return td




def reduce_dict_dimension(year_dict,output_words):
    temp_dt = {}
    updated = {}
    for month, words_per_day in year_dict.items():
        for key, value in words_per_day.items():
            # print(value)
            temp_dt.update(value)


        updated[month] = dict(Counter(temp_dt).most_common(output_words))
        temp_dt = {}

    return updated



def get_coordinates(dictionary):

    dates = []
    words_in_dates = []
    magnitude_per_words = []
    temp_w = []
    temp_m = []
    temp_area = []
    area = []
    x_coordinates = []
    y_coordinates = []
    temp_x = []
    temp_y = []

    for day, value in dictionary.items():
        dates.append(day)
        for words, magnitude in value.items():
            temp_w.append(words)
            temp_m.append(float(magnitude))
            for x in magnitude.split():
                temp_area.append(round(2 * math.pi * float(x))*4)
                #temp_area.append(float(x))

        area.append(temp_area)
        words_in_dates.append(temp_w)
        magnitude_per_words.append(temp_m)
        temp_w = []
        temp_m = []
        temp_area = []


    for i in range(len(magnitude_per_words)):
        for j in range(len(magnitude_per_words[i])):
            temp_x.append(i + 1)
            temp_y.append(j + 1)
        x_coordinates.append(temp_x)
        y_coordinates.append(temp_y)
        temp_x = []
        temp_y = []



    return dates ,x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area



def basic_plot(dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area, month=True):

    for i in range(len(dates)):
        for j in range(len(magnitude_per_words)):
            for k in range(len(magnitude_per_words[j])):
                # print(magnitude_per_words[j][k])
                plt.text(x=x_coordinates[j][k], y=y_coordinates[j][k], s=words_in_dates[j][k],
                         fontsize=8, horizontalalignment='center')

    plt.title("WORDS USED IN TODAY'S NEWS")

    if month == False:
        plt.xlabel('Yearly Data')
    else:
        plt.xlabel('Month Of ' + str(month_folder))
    plt.ylabel('Number Of Trends')
    # xticks( arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue') )
    # plt.yticks(list(range(1, 10+ 1)))
    plt.xticks(list(range(1, len(dates) + 1)), dates)

    plt.scatter(x_coordinates, y_coordinates, s=area, linewidths=2, edgecolor='w')
    #plt.show()


    grand_out_png = grand_out.strip('.out')+str('.png')
    plt.savefig(grand_out_png, format='png', dpi=1000)
    plt.clf()


def initail_processing(category, output_words):

    root = os.getcwd()
    global grand_out
    grand_out = 'grand_data.out'
    month_dict = {}
    year_dict = {}

    ##### Scaning root folders for folders of months
    for month_folder in os.listdir(root):
        if '.' not in month_folder:
            month_dir = root + '/' + month_folder + '/'
            os.chdir(month_dir)

            ##### Found month folders are scanned for day's NEWS
            for day_folder in os.listdir(month_dir):
                if '.' not in day_folder:
                    day_dir = month_dir + '/' + day_folder + '/'
                    os.chdir(day_dir)
                    print('asd')

                    ##### If there is a grand out file it will remove it
                    if grand_out in os.listdir(day_dir):
                        os.remove(grand_out)

                    ###### Refining raw text files
                    for filename in os.listdir(day_dir):
                        if filename.endswith(".rawtext"):
                            refine_raw_data(filename)
                            continue
                        else:
                            continue

                    ###### Data Mining in refined files and generating grand_out
                    for filename in os.listdir(day_dir):
                        if filename.endswith(".txt"):
                            data_mining(filename)

                            continue
                        else:
                            continue


                    ###### Generating day_dict by their day month-wise
                    day_dict = create_dict()

                    month_dict[day_folder] = day_dict

                ###### Sorting Monthly Dict
                month_dict = dict(collections.OrderedDict(sorted(month_dict.items())))
                if category == 'month':
                    os.chdir(month_dir)
                    return month_dict
                else:
                    pass
            ##### Change Dir and Generating year_dict by their month

            year_dict[month_folder] = month_dict
            month_dict = {}
    #### Change Dir and reducing dictionary dimensions

    year_dict = reduce_dict_dimension(year_dict, output_words)
    os.chdir(root)
    return year_dict

if __name__ == "__main__":
# for month_folder in os.listdir(root):
#     if '.' not in month_folder:
#         month_dir = root + '/' + month_folder + '/'
#         os.chdir(month_dir)
#
#         for day_folder in os.listdir(month_dir):
#             if '.' not in day_folder:
#                 day_dir = month_dir + '/' + day_folder + '/'
#                 os.chdir(day_dir)
#
#
#                 if grand_out in os.listdir(day_dir):
#                     os.remove(grand_out)
#
#                 ################################## Data Refine #######################################
#
#                 for filename in os.listdir(day_dir):
#                     if filename.endswith(".rawtext"):
#                         refine_raw_data(filename)
#                         continue
#                     else:
#                         continue
#
#                 ################################## Data Mining #######################################
#
#                 for filename in os.listdir(day_dir):
#                     if filename.endswith(".txt"):
#                         data_mining(filename)
#                         continue
#                     else:
#                         continue
#
#                 ################################ Getting daily Dict #################################
#
#
#                 day_dict = create_dict()
#                 month_dict[day_folder] = day_dict
#
#
#
#             ## Sorting Monthly Dict
#             month_dict = dict(collections.OrderedDict(sorted(month_dict.items())))
#
#             #for key, value in month_dict.items():
#             #    print(key,value)
#             #print(month_dict)
#
#         #################################### Get Coordinates ######################################
#
#
#         #dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area = get_coordinates(month_dict)
#
#
#
#     #####################################    Plotting    #######################################
#
#         os.chdir(month_dir)
#         year_dict[month_folder] = month_dict
#         #print(month_dict)
#         #basic_plot(dates,x_coordinates,words_in_dates,magnitude_per_words)
#         month_dict = {}
#
# os.chdir(root)
# year_dict = reduce_dict_dimension(year_dict,output_words)
#
#
# months, x_coordinates, y_coordinates, words_in_months, magnitude_per_words, area = get_coordinates(year_dict)
#
#
# basic_plot(dates=months,x_coordinates=x_coordinates,
#            y_coordinates=y_coordinates,words_in_dates=words_in_months,
#            magnitude_per_words=magnitude_per_words, area=area)
