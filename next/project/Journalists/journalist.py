

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
    filename_out = filename.strip('.text')+str('.refined')
    with open(filename, 'r') as data:
        data = data.read()
    #data = open(filename, 'r')

    data = ' '.join(data.split())


    stopWords = set(stopwords.words('english'))

    filtered = ''
    sentence = ''
    for x in data:
        if x != '.':
            if x in [',', '“', '”', '—', '(', ')', '[', ']','{','}', ':']:
                pass
            else:
                sentence = sentence + x
        if x == '.':
            filtered = filtered + check(sentence,stopWords) + '\n'
            sentence = ''

    with open(filename_out, 'w+') as data_out:
        data_out.write(filtered)
    #data_out = open(filename_out, 'w+')

    #data_out.close()
    #print(filtered)

def check(sentence,stopWords):
    temp = ''
    for x in sentence.split():
        if x in stopWords:
            pass
        if x not in stopWords:

            temp = temp + str(x) + ' '

    return temp




def data_mining(filename, n):
    filename_out = filename.strip('.txt') + str('.out')
    command = ["./apriori", n, filename, filename_out]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(2)
    temp = nano_filter_function(filename_out)
    return temp


def nano_filter_function(filename_out):

    with open(filename_out, 'r') as f_nano:
        temp = f_nano.read()
    #f_nano = open(filename_out, 'r')


    temp = temp.split('\n')

    for x in temp:
        write_data(x)

    #f_nano.close()

    return temp


def write_data(data):

    with open(grand_out, 'a+') as grand:
        grand.write(str(data) + '\n')
    #grand = open(grand_out, 'a+')

    #grand.close()


def create_dict(n, output_words=None):

    with open(grand_out, 'r') as f:
        temp = f.read()
    #f = open(grand_out, 'r')

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


    day_dict = trim_dict(day_dict,n)
    #print(day_dict)
    if output_words != None:
        day_dict = dict(Counter(day_dict).most_common(output_words))  #### getting just top 7 elements in dict
        return day_dict
    else:
        return day_dict


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def updatekeys(d):
    temp = dict(d)
    temp = dict(Counter(temp).most_common()) #output_words
    return temp


def get_top_words(dictionary):
    for key, value in dictionary.items():
        dictionary[key] = updatekeys(dictionary[key])

    return dictionary


def short_convert_to_dict(data):
    dictionary = {}

    for x in data:
        if x != '':
            temp = x.split()
            dictionary[temp[0]] = temp[1].strip('()')


    dictionary = trim_dict(dictionary,n)
    return dictionary


def convert_to_dict(dictionary):
    dict_temp = {}
    for key, result in dictionary.items():
        for x in result:
            if x != '':
                temp = x.split()

                if 'The' not in temp[0]:
                    dict_temp[temp[0]] = temp[1].strip('()')


        dictionary[key] = dict_temp
        dict_temp = {}



    for key, value in dictionary.items():
        dictionary[key] = trim_dict(value, n)


    dictionary = get_top_words(dictionary)
    print(dictionary)

    dictionary = collections.OrderedDict(sorted(dictionary.items()))

    return dictionary



def trim_dict(day_dict,n):
    td = {}
    for key, value in day_dict.items():
        if '1' in n:
            if len(key.split()) == 1:
                td[key] = value

        if '2' in n:
            if len(key.split()) == 2:
                td[key] = value

        if '3' in n:
            if len(key.split()) == 3:
                td[key] = value

        if '4' in n:
            if len(key.split()) == 4:
                td[key] = value

    return td



def verify_word(find,words):
    for x in words.split():
        if x == find:
            return True
    return False


def conditon_verifier(condition, word):
    verified = 0
    for x in condition.split():
        if x in word:
            verified +=1
    if verified == len(word.split()):
        return True
    if verified != len(word.split()):
        return False


def find_words(dictionary, regular=True):

    temp = {}
    if regular == True:
        for key, value in dictionary.items():

            if conditon_verifier(condition,key.lower()) == True:
                temp[key] = value
        return temp


    if regular == False:
        for key, value in dictionary.items():
            for words, values in value.items():
                if find_me1 in words.lower():
                    if verify_word(find_me1,words.lower()) == True:
                        if find_me1 not in temp.items():
                            temp[words] = values
                        # print(words)
                if find_me2 in words.lower():
                    if verify_word(find_me2,words.lower()) == True:
                        if find_me2 not in temp.items():
                            temp[words] = values
                            # print(words)
                if find_me3 in words.lower():
                    if verify_word(find_me3, words.lower()) == True:
                        if find_me3 not in temp.items():
                            temp[words] = values

                if find_me4 in words.lower():
                    if verify_word(find_me4, words.lower()) == True:
                        if find_me4 not in temp.items():
                            temp[words] = values

        return temp


def find_words_handler(dictionary):
    found_you = {}
    direct = True
    found_you = find_words(dictionary, regular=True)
    # if found_you == {}:
    #     found_you = find_words(dictionary, regular=False)
    #     direct = False

    found_you = dict(Counter(found_you).most_common(1))

    return found_you


def autofill(x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area):

    x_coordinates = autofill_algorithm(x_coordinates, datatype='int')
    y_coordinates = autofill_algorithm(y_coordinates, datatype='int',append='one')
    words_in_dates = autofill_algorithm(words_in_dates, datatype='str')
    magnitude_per_words = autofill_algorithm(magnitude_per_words, datatype='int',append='one')
    area = autofill_algorithm(area, datatype='int',append='one')

    return x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area


def autofill_algorithm(lists, datatype=None, append=None):
    if datatype == 'int' and append == None:
        for i, value in enumerate(lists):
            if len(value) < output_words:
                while len(value) != output_words:
                    value.append(i + 1)
                    pass

        return lists

    if datatype == 'int' and append == 'one':
        for i, value in enumerate(lists):
            if len(value) < output_words:
                while len(value) != output_words:
                    value.append(1)
                    pass

        return lists



    if datatype == 'str':
        for i, value in enumerate(lists):
            if len(value) < output_words:
                while len(value) != output_words:
                    value.append('')
                    pass

        return lists




def get_coordinates(dictionary,autofill=None):

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
                temp_area.append(round(2 * math.pi * float(x))*5)
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

    if autofill == True:
        autofill(x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area)


    return dates ,x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area




def basic_plot(dates, x_coordinates, y_coordinates, words_in_dates,magnitude_per_words, area,individual=None):

    for i in range(len(dates)):
        for j in range(len(magnitude_per_words)):
            for k in range(len(magnitude_per_words[j])):
                plt.text(x=x_coordinates[j][k], y=y_coordinates[j][k], s=words_in_dates[j][k].replace(' ', '\n'),
                         fontsize=8, horizontalalignment='center', verticalalignment='center', rotation='vertical')

    if individual == None:
        plt.title("TOP JOURNALIST'S TRENDS FOR LAST 6 MONTHS")
        plt.ylabel('Number Of Trends')
        # xticks( arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue') )
        plt.yticks(list(range(1, len(y_coordinates[0]) + 1)))
        plt.xticks(list(range(1, len(dates) + 1)), dates, rotation='vertical')
        plt.scatter(x=x_coordinates, y=y_coordinates, s=area)
        #plt.show()
        grand_out_png = grand_out.strip('.out')+str('.png')
        plt.savefig(grand_out_png, format='png', dpi=1000,bbox_inches='tight')
        plt.clf()

    if individual != None:
        plt.title('Top Trends For ' + individual + ' Last 6 Months')
        plt.ylabel('Number Of Trends')
        # xticks( arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue') )
        plt.yticks(list(range(1, len(y_coordinates[0]) + 1)))
        plt.xticks(list(range(1, len(dates) + 1)), dates, rotation='vertical')
        plt.scatter(x=x_coordinates, y=y_coordinates, s=area, linewidths=2, edgecolor='w')
        #plt.show()

        plt.savefig(individual+'.png', format='png', dpi=1000,bbox_inches='tight')
        plt.clf()


def line_chart(dates,x_coordinates,words_in_dates,magnitude_per_words, journalist, convert=None):

    mylabel = ''
    for x in words_in_dates:
        if x != []:
            mylabel = str(x).strip('[]')
            break

    if mylabel == '':
        return

    if convert == True:
        temp_m = []
        temp_x = []
        i = 1
        for x in magnitude_per_words:
            print(x)
            temp_m.append(float(str(x).strip('[]') + str(0)))
            temp_x.append(i)
            i += 1
        magnitude_per_words = temp_m
        x_coordinates = temp_x


    if mylabel != '':
        plt.plot(x_coordinates, magnitude_per_words, label=mylabel, linestyle='-')
        plt.legend(bbox_to_anchor=(1.4, 1.03))
        plt.xticks(x_coordinates, dates, rotation='vertical')
        plt.ylabel('Word Magnitude')
        plt.title(journalist)
        plt.grid()
        #plt.axis([0, int(x_coordinates[-1]), 0, max(magnitude_per_words)])

        grand_out_png = journalist + str('.png')
        plt.savefig(grand_out_png, format='png',bbox_inches='tight', dpi=1000)
        plt.clf()




def initail_process_individual(root,output_words):
    articles_info = {}
    main_dict = {}
    journalist_dir = ''


    for journalist in os.listdir(root):
        if '.' not in journalist:
            journalist_dir = root + '/' + journalist + '/'
            os.chdir(journalist_dir)

            if grand_out in os.listdir(journalist_dir):
                os.remove(grand_out)

            for articles in os.listdir(journalist_dir):
                if articles.endswith('.text'):
                    refine_raw_data(articles)
                    continue
                else:
                    continue

            for filename in os.listdir(journalist_dir):
                if filename.endswith("refined"):
                    article = filename.strip('.refined')
                    file = data_mining(filename, n)
                    #print(file)

                    file = short_convert_to_dict(file)
                    file = find_words_handler(file)
                    articles_info[article] = file

                    #articles_info[article] = find_words_handler(articles_info[article])
                    #print(articles_info[article])
                    #articles_info[article] =convert_to_dict(articles_info)

            #main_dict[journalist] = articles_info
            #articles_info = convert_to_dict(articles_info)
            articles_info = collections.OrderedDict(sorted(articles_info.items()))
            print(articles_info)
            #articles_info = find_words_handler(articles_info)
            #articles_info = find_words_handler(articles_info)
            #print(articles_info)

            dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area = get_coordinates(articles_info,autofill=None)
            #print(articles_info)


            line_chart(dates, x_coordinates, words_in_dates, magnitude_per_words, journalist, convert=True)
            #basic_plot(dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area, individual=journalist)
            print(journalist)
            #articles_info = create_dict(n=n,output_words=output_words)
            #main_dict[journalist] = articles_info

    os.chdir(root)
    return main_dict
















def initail_process_all(root,output_words):
    articles_info = {}
    main_dict = {}
    journalist_dir = ''

    for journalist in os.listdir(root):
        if '.' not in journalist:
            journalist_dir = root + '/' + journalist + '/'
            os.chdir(journalist_dir)

            if grand_out in os.listdir(journalist_dir):
                os.remove(grand_out)

            for articles in os.listdir(journalist_dir):
                if articles.endswith('.rawtext'):
                    refine_raw_data(articles)
                    continue
                else:
                    continue

            for filename in os.listdir(journalist_dir):
                if filename.endswith("refined"):
                    data_mining(filename, n)
                    continue
                else:
                    continue

            articles_info = create_dict(n=n,output_words=output_words)
            main_dict[journalist] = articles_info

    os.chdir(root)
    return main_dict






if __name__ == "__main__":

    root = os.getcwd()
    journalist_dir = ''
    global n
    n = '-n1'
    global grand_out
    grand_out = 'grand_data.out'
    global output_words
    output_words = 5

    global find_me1
    global find_me2
    global find_me3
    global find_me4
    global condition

    find_me1 = 'political'.strip().lower()  # ['PSP', 'MQM']
    find_me2 = ''.strip().lower()
    find_me3 = ''.strip().lower()
    find_me4 = ''.strip().lower()

    condition = find_me1 + ' ' + find_me2 + ' ' + find_me3 + ' ' + find_me4
    condition = condition.strip()

    #main_dict = initail_process_individual(root, output_words=output_words)

    main_dict = initail_process_all(root,output_words=output_words)
    # print(main_dict)
    # dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area = get_coordinates(main_dict)
    # basic_plot(dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area)
