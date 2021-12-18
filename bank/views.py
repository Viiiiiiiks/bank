import csv
import io
import sys, traceback
from audioop import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from .models import Post
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
from dbfread import DBF
from time import localtime, strftime
import xlwt
from tqdm import tqdm


def index(request):
    """

    Цель: подключить основную html страницу
    :param request:
    :return: рендер шаблона 'index.html'
    """
    return render(request, 'index.html')


def profile_upload(request):
    """

    Цель: Загрузка БД

    :param request:
    :return: рендер шаблона
    """

    # declaring template
    template = "profile_upload.html"
    data = Post.objects.all()

    # prompt is a context variable that can have different values      depending on their context
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

    csv_file = request.FILES['file']

    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('cp1251')
    print(data_set.count('\n'))
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    y = 1
    j = 0
    for column in tqdm(csv.reader(io_string, delimiter=';', quotechar="|")):
        _, created = Post.objects.update_or_create(
            Number=column[0],
            REGN=column[1],
            NAME_B=column[2],
            ROOT=column[3],
            SIM_R=column[4],
            SIM_V=column[5],
            SIM_ITOGO=column[6],
            DT=column[7],
        )
        j += 1
    context = {'index': j}
    return render(request, 'index.html', context, {'flag': y})




codes = []

def list_of_banks(request):
    """
    Выводит список банков, содержащихся в базе данных
    """
    try:
        f = 1
        obj = Post.objects.all()[0]
        r_date = obj.DT
        qr_banks = Post.objects.filter(DT=r_date)
        bankes = []
        for record in qr_banks:
            if str(record.NAME_B) not in bankes:
                bankes.append(str(record.NAME_B))
        return render(request, 'index.html', {'result': f, 'bankes': bankes})
    except Exception as e:
        print(e)
        return render(request, 'includes/index_new_report.html', {'rort': f})


def new_database(request):
    """
    Заполняет базу данных на основе класса Post
    """
    csv_file = 'bank/BD1.csv'
    with open(csv_file) as f:
        data_set = f.read()
    io_string = io.StringIO(data_set)
    for column in tqdm(csv.reader(io_string, delimiter=';', quotechar="|"), total=data_set.count('\n') - 1):
        _, created = Post.objects.update_or_create(
            Number=column[0],
            REGN=column[1],
            NAME_B=column[2],
            ROOT=column[3],
            SIM_R=column[4],
            SIM_V=column[5],
            SIM_ITOGO=column[6],
            DT=column[7],
        )
    context = {}
    return render(request, 'index.html', context)





def choises(request):
    """

    Цель: передать значение выбора пользователя по виду отчета
    :param request:
    :return: рендер шаблона 'index.html', словарь с выбранным типом отчета и списком банков
    """
    results = request.GET.get("choises")
    bank_list = Post.objects.all()
    return render(request, 'index.html', {'choises': results, 'bank': '', 'bank_list': bank_list})




df = pd.DataFrame(columns=['NAME_B', 'SIM_R', 'SIM_V', 'SIM_ITOGO', 'REGN', 'DT'])


def input_bank(request):
    """

    Цель: Получения названия банка, проверка наличия такого в БД, загрузка отчета по банку в случае наличия
    :param request:
    :return: рендер нужного шаблона в зависимости от наличия банка в БД, название введенного пользователем банка
    """
    global result
    try:
        obj = Post.objects.all()[0]
        r_date = obj.DT
        qr_banks = Post.objects.filter(DT=r_date)
        bankes = []
        for record in qr_banks:
            if str(record.NAME_B) not in bankes:
                bankes.append(str(record.NAME_B))
        result = request.GET.get("bank")
        j=-1
        for i in range(0,20):
            obj1 = Post.objects.all()[i]
            name = obj1.NAME_B
            if name == result:
                j+=1
                df.loc[j, 'ROOT'] = obj.ROOT
                df.loc[j, 'NAME_B'] = obj.NAME_B
                df.loc[j, 'SIM_R'] = obj.SIM_R
                df.loc[j, 'SIM_V'] = obj.SIM_V
                df.loc[j, 'SIM_ITOGO'] = obj.SIM_ITOGO
                df.loc[j, 'REGN'] = obj.REGN
                df.loc[j, 'DT'] = obj.DT
        tm_struct = localtime()
        filename = 'report_one_bank_' + strftime('%Y_%m_%d_%H_%M_%S', tm_struct) + '.xls'
        df.to_excel(filename)
        trfg = 1
        codes =[]
        qr_codes = Post.objects.filter(NAME_B=request.GET.get("bank"))
        for record in qr_codes:
            if str(record.ROOT) not in codes:
                codes.append(str(record.ROOT))
        print(codes)
        return render(request, 'includes/main2_dop.html',
                    {'bank': str(request.GET['bank']), 'plot': trfg, 'codes': codes})
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return render(request, 'includes/bank_not_found.html', {'bank': request.GET['bank']})


def input_date(request):
    """

    Цель: загрузка отчета по всем банкам за определенную дату
    :param request:
    :return: рендер нужного шаблона в зависимости от резульата, выбранная пользователем дата
    """
    try:
        if request.method == 'GET' and 'date' in request.GET:
            date = str(request.GET['date']).replace('.', '-')
            filtered_by_date = Post.objects.filter(DT=date)

            dataframe = pd.DataFrame(columns=['NAME_B',
                                              'SIM_R',
                                              'SIM_V',
                                              'SIM_ITOGO',
                                              'REGN',
                                              'DT'
                                              ])
            i = -1
            for obj in filtered_by_date:
                i += 1
                dataframe.loc[i, 'ROOT'] = obj.ROOT
                dataframe.loc[i, 'NAME_B'] = obj.NAME_B
                dataframe.loc[i, 'SIM_R'] = obj.SIM_R
                dataframe.loc[i, 'SIM_V'] = obj.SIM_V
                dataframe.loc[i, 'SIM_ITOGO'] = obj.SIM_ITOGO
                dataframe.loc[i, 'REGN'] = obj.REGN
                dataframe.loc[i, 'DT'] = obj.DT
            tm_struct = localtime()
            filename = 'report_by_date_' + strftime('%Y_%m_%d_%H_%M_%S', tm_struct) + '.xls'
            dataframe.to_excel(filename)
            return render(request, 'includes/main1_dop.html', {'date': date})

    except Exception as e:
        print('exception:', e)
        return render(request, 'includes/date_not_found.html', {'date': request.GET['date']})


def graphic(request):
    """

    Цель: Построить график на основе показателя выбранного пользователем
    :param request:
    :return: рендер шаблона 'graphic,html'
    """
    try:
        code = Post.objects.filter(ROOT=request.GET.get("graphic"), NAME_B=result)[0]
        codes = Post.objects.filter(ROOT=request.GET.get("graphic"), NAME_B=result)
        plt.ioff()
        i = -1
        dataframe1 = pd.DataFrame(columns=['NAME_B',
                                           'SIM_R',
                                           'SIM_V',
                                           'SIM_ITOGO',
                                           'REGN',
                                           'DT'
                                           ])
        for obj in codes:
            i += 1
            dataframe1.loc[i, 'SIM_ITOGO'] = obj.SIM_ITOGO
            dataframe1.loc[i, 'DT'] = obj.DT
        if dataframe1.shape[0] > 1:
            dataframe1.plot(kind='line', y='SIM_ITOGO', x='DT')
        elif dataframe1.shape[0] == 1:
            dataframe1.plot(kind='scatter', y='SIM_ITOGO', x='DT')
        plt.savefig('main2_dop.png')
        return render(request, 'includes/graphic.html', {'code': code.ROOT})
    except Exception as e:
        print(e)
        return render(request, 'includes/date_not_found.html')


def my_image(request):
    """

    Цель: Вывод графика пользователю
    :param request:
    :return:
    """
    image_data = open("main2_dop.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
