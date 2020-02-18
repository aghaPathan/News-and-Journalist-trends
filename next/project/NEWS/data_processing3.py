

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
            if x in [',', '“', '”', '—', '(', ')', '[', ']','{','}', ':']:
                pass
            else:
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

def data_mining(filename, n):
    filename_out = filename.strip('.txt') + str('.out')
    command = ["./apriori", n, filename, filename_out]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(2)
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

def create_dict(n, output_words=None):

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


    day_dict = trim_dict(day_dict,n)
    #print(day_dict)
    if output_words != None:
        day_dict = dict(Counter(day_dict).most_common(output_words))  #### getting just top 7 elements in dict
        return day_dict
    else:
        return day_dict




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




def reduce_dict_dimension(year_dict,output_words):
    temp_dt = {}
    updated = {}
    for month, words_per_day in year_dict.items():
        for key, value in words_per_day.items():
            # print(value)
            temp_dt.update(value)

        if output_words != None:
            updated[month] = dict(Counter(temp_dt).most_common(output_words))
            temp_dt = {}
        if output_words == None:
            updated[month] = dict(Counter(temp_dt))
            #updated[month] = find_words_handler(updated)
            temp_dt = {}

    return updated


def yearly_sort(dictionary):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    dictionary =collections.OrderedDict(sorted(dictionary.items(), key=lambda x: months.index(x[0])))

    return dictionary



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



    return dates ,x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area



def basic_plot(dates, x_coordinates, y_coordinates, words_in_dates,
               magnitude_per_words, area, month=True, markers=None):

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
    plt.yticks(list(range(1, len(magnitude_per_words[0]) + 1)))
    plt.xticks(list(range(1, len(dates) + 1)), dates)

    plt.scatter(x_coordinates, y_coordinates, s=area, linewidths=2, edgecolor='w')
    #plt.show()


    grand_out_png = grand_out.strip('.out')+str('.png')
    plt.savefig(grand_out_png, format='png', dpi=1000)
    plt.clf()



def complex_plot(x_coordinates,y_coordinates,dates,magnitude_per_words, markers_array,
                words_in_dates):

    for j in range(len(magnitude_per_words)):
        for k in range(len(magnitude_per_words[j])):
            plt.scatter(x_coordinates[j][k], y_coordinates[j][k], s=100, c='b',
                        marker=markers_array[j][k], label=words_in_dates[j][k])



    plt.title("WORDS USED IN TODAY'S NEWS")
    plt.xticks(list(range(1, len(dates) + 1)), dates)

    #### Deleting legends duplicacy
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = collections.OrderedDict(zip(labels, handles))
    lgd = plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.03, 1.03))

    grand_out_png = grand_out.strip('.out') + str('.png')
    plt.savefig(grand_out_png, format='png', dpi=1000, bbox_extra_artists=(lgd,),
                bbox_inches='tight')
    plt.clf()





def bar_chart(dates, magnitude_per_words, words_in_dates,year=None):

    if year == None:
        magnitude_new = []
        for x in magnitude_per_words:
            magnitude_new.append(float(str(x).strip('[]') + str(0)))

    if year == True:
        magnitude_new = []
        for x in magnitude_per_words:
            magnitude_new.append(float(str(x).strip('[]')+str(0)))



    objects = dates
    magnitude = magnitude_new  # [0, 15, 10]
    y_pos = np.arange(len(objects))

    for i, v in enumerate(magnitude):
        print(i, v)
        plt.text(i, v, s=str(words_in_dates[i]).strip('[]'), horizontalalignment='center',fontsize=8)

    plt.bar(y_pos, magnitude, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.title("WORDS TRENDS")
    plt.ylabel('Magnitude')

    #plt.show()
    grand_out_png = grand_out.strip('.out') + str('.png')
    plt.savefig(grand_out_png, format='png', dpi=1000)
    plt.clf()






def line_chart(dates,x_coordinates,words_in_dates,magnitude_per_words, convert=None):

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
        plt.ylabel('Magnitude')
        plt.title("WORDS TRENDS")
        plt.grid()
        #plt.axis([0, int(x_coordinates[-1]), 0, max(magnitude_per_words)])

        grand_out_png = grand_out.strip('.out') + str('.png')
        plt.savefig(grand_out_png, format='png',bbox_inches='tight', dpi=1000)
        plt.clf()












def get_markers(words_in_dates):
    markers = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+",
               "x", "X", "D", "d", "|", "_", 'TICKLEFT', 'TICKRIGHT', 'TICKUP', 'TICKDOWN', 'CARETLEFT',
               'CARETRIGHT', 'CARETUP', 'CARETDOWN', 'CARETLEFTBASE', 'CARETRIGHTBASE', 'CARETUPBASE']

    marker_dict = {}
    markers_array = []
    temp = []
    k = 0


    for i in range(len(words_in_dates)):
        for j in range(len(words_in_dates[i])):
            if words_in_dates[i][j] in marker_dict:
                pass
            if words_in_dates[i][j] not in marker_dict:
                marker_dict[words_in_dates[i][j]] = markers[k]
                k += 1


    for i in range(len(words_in_dates)):
        for j in range(len(words_in_dates[i])):
            temp.append(marker_dict[words_in_dates[i][j]])

        markers_array.append(temp)
        temp = []

    return markers_array


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
            for words, values in value.items():
                # print(words)
                if conditon_verifier(condition,words.lower()) == True:
                    # print(words, values)
                    temp[words] = values
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


def monthly_data_on_demand(n, output_words=None, chart_type=None):

    global month_dict
    global month_folder
    month_dict = {}


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
                            data_mining(filename,n)
                            continue
                        else:
                            continue


                    ###### Generating day_dict by their day month-wise
                    day_dict = create_dict(n=n,output_words=output_words)

                    month_dict[day_folder] = day_dict
                    month_dict[day_folder] = find_words_handler(month_dict)
                    print(month_dict)
                    #print(month_dict)

                #### Sorting Monthly Dict
                month_dict = collections.OrderedDict(sorted(month_dict.items()))


            ##### Changing Dir
            os.chdir(month_dir)

            dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area = get_coordinates(
                 month_dict)

            if chart_type == 'bar':
                bar_chart(dates=dates,magnitude_per_words=magnitude_per_words,words_in_dates=words_in_dates)

            if chart_type == 'line':
                line_chart(dates=dates,x_coordinates=x_coordinates,words_in_dates=words_in_dates,magnitude_per_words=magnitude_per_words,convert=True)

            month_dict = {}












def monthly_data_output(n, output_words=None, plot=None):

    global month_dict
    global month_folder
    month_dict = {}


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
                            data_mining(filename,n)
                            continue
                        else:
                            continue


                    ###### Generating day_dict by their day month-wise
                    day_dict = create_dict(n=n,output_words=output_words)
                    month_dict[day_folder] = day_dict
                    print(month_dict)

                #### Sorting Monthly Dict
                month_dict = dict(collections.OrderedDict(sorted(month_dict.items())))


            #### Changing Dir
            os.chdir(month_dir)


            if plot == 'basic':

                #### Getting coordinates for plotting
                dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area = get_coordinates(
                    month_dict)

                #### Plotting
                basic_plot(dates, x_coordinates, y_coordinates,
                           words_in_dates, magnitude_per_words, area)
                month_dict = {}




def yearly_data_ondemand(n, output_words=None, chart_type=None):
    year_dict = {}
    month_dict = {}


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
                            data_mining(filename,n)
                            continue
                        else:
                            continue

                    ###### Generating day_dict by their day month-wise
                    day_dict = create_dict(n=n)
                    month_dict[day_folder] = day_dict
                    #month_dict[day_folder] = find_words_handler(month_dict)



                ###### Sorting Monthly Dict
                #month_dict = dict(collections.OrderedDict(sorted(month_dict.items())))

            month_dict = find_words_handler(month_dict)
            #print(month_dict)

            ##### Change Dir and Generating year_dict by their month
            os.chdir(month_dir)
            year_dict[month_folder] = month_dict



            #year_dict[month_folder] = find_words_handler(year_dict)
            month_dict = {}

    #### Change Dir and reducing dictionary dimensions and sorting
    os.chdir(root)
    #year_dict = reduce_dict_dimension(year_dict,output_words)
    print(year_dict)
    #year_dict = find_words_handler(year_dict)

    year_dict = yearly_sort(year_dict)

    dates, x_coordinates, y_coordinates, words_in_dates, magnitude_per_words, area = get_coordinates(
        year_dict)

    if chart_type == 'bar':
        bar_chart(dates=dates, magnitude_per_words=magnitude_per_words, words_in_dates=words_in_dates, year=True)

    if chart_type == 'line':
        line_chart(dates=dates,x_coordinates=x_coordinates,words_in_dates=words_in_dates,magnitude_per_words=magnitude_per_words, convert=True)





















def yearly_data_output(output_words, n, plot=None):
    year_dict = {}
    month_dict = {}


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
                            data_mining(filename,n)
                            continue
                        else:
                            continue

                    ###### Generating day_dict by their day month-wise
                    day_dict = create_dict(n=n)
                    month_dict[day_folder] = day_dict



                ###### Sorting Monthly Dict
                month_dict = dict(collections.OrderedDict(sorted(month_dict.items())))


            ##### Change Dir and Generating year_dict by their month
            os.chdir(month_dir)
            year_dict[month_folder] = month_dict
            month_dict = {}

    #### Change Dir and reducing dictionary dimensions and sorting
    os.chdir(root)
    year_dict = reduce_dict_dimension(year_dict,output_words)


    year_dict = yearly_sort(year_dict)

    #### Getting coordinates for plotting
    months, x_coordinates, y_coordinates, words_in_months, magnitude_per_words, area = get_coordinates(year_dict)


    if plot == False:
        return year_dict
    if plot == 'basic':

        #### Plotting
        basic_plot(dates=months,x_coordinates=x_coordinates,
                   y_coordinates=y_coordinates,words_in_dates=words_in_months,
                   magnitude_per_words=magnitude_per_words, area=area,month=False)

        return year_dict

    if plot == 'complex':
        markers_array = get_markers(words_in_months)

        complex_plot(x_coordinates=x_coordinates, y_coordinates=y_coordinates,
                     dates=months, magnitude_per_words=magnitude_per_words,
                     markers_array=markers_array,words_in_dates=words_in_months)














if __name__ == "__main__":

    global n
    n = '-n3'

    global root
    #global month_folder
    global day_folder


    root = os.getcwd()
    month_dir = ''
    day_dir = ''


    #output_words = 4

    ############################### Grand OutPut File ###################################
    global grand_out
    grand_out = 'grand_data.out'

    ############################## IF GRANDE OUTPUT EXSIST ###############################

    #monthly_data_output(output_words,plot=True)

    #qwe = monthly_data_output(n=n,output_words=None, plot=False)
    #print(qwe)
    global find_me1
    global find_me2
    global find_me3
    global find_me4
    global condition

    find_me1 = 'Pakistan'.strip().lower()  # ['PSP', 'MQM']
    find_me2 = 'India'.strip().lower()
    find_me3 = 'Border'.strip().lower()
    find_me4 = ''.strip().lower()

    condition = find_me1 +' '+ find_me2 + ' ' +  find_me3 + ' ' + find_me4
    condition = condition.strip()

    yearly_data_ondemand(n=n,output_words=None,chart_type='line')
    #monthly_data_on_demand(n=n,output_words=None,chart_type='line')



