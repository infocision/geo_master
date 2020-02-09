from django.shortcuts import render,HttpResponse
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
from sqlalchemy import *

curr_usr = {}

cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
table1 = pd.read_sql('select * from shield_month_apr', cnx)
table2 = pd.read_sql('select * from shield_month_may', cnx)
table3 = pd.read_sql('select * from shield_month_jun', cnx)
table4 = pd.read_sql('select * from shield_month_jul', cnx)
table5 = pd.read_sql('select * from shield_month_aug', cnx)
table6 = pd.read_sql('select * from shield_month_sep', cnx)
table7 = pd.read_sql('select * from shield_month_oct', cnx)

frames = [table1, table2, table3, table4, table5, table6, table7]
result = pd.concat(frames,sort=True)

def product_view(request):
    return render(request, 'login.html')

def sign_in_view(request):
    return render(request, 'sign_in.html')

# def login_view(request):
#     return render(request, 'HiDOCTOR Welcomes you!.html')

def index(request):
    usr = [request.POST['user_name']]
    curr_usr['usr_nm']=usr
    pwd = request.POST['password']
    # print(type(pwd))
    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)


    if True in list(data1['1st Reporting User Name','2nd Reporting User Name'].isin(usr)) and pwd == 'pass@123':
        return render(request, 'index.html', {"usr":usr})
    elif True in list(data1['2nd Reporting User Name','2nd Reporting User Name'].isin(usr)) and pwd == 'pass@123':
        return render(request, 'index.html', {"usr":usr})
    else:
        return HttpResponse("Invalid credential please enter correct username and password")

def dashboard(request):
    # return render(request, 'dashboard.html')

    usr = [request.POST['user_name']]
    curr_usr['usr_nm'] = usr
    pwd = request.POST['password']
    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)

    if True in list(data1['1st Reporting User Name'].isin(usr)) and pwd == 'pass@123':
        return render(request, 'dashboard.html', {"usr": usr})
    elif True in list(data1['2nd Reporting User Name'].isin(usr)) and pwd == 'pass@123':
        return render(request, 'dashboard.html', {"usr": usr})
    else:
        return HttpResponse("Invalid credential please enter correct username and password")

def primary_sales(request):
    # cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    # table1 = pd.read_sql('select * from shield_month_apr', cnx)
    # table2 = pd.read_sql('select * from shield_month_may', cnx)
    # table3 = pd.read_sql('select * from shield_month_jun', cnx)
    # table4 = pd.read_sql('select * from shield_month_jul', cnx)
    # table5 = pd.read_sql('select * from shield_month_aug', cnx)
    # table6 = pd.read_sql('select * from shield_month_sep', cnx)
    # table7 = pd.read_sql('select * from shield_month_oct', cnx)
    #
    # frames = [table1, table2, table3, table4, table5, table6, table7]
    result = pd.concat(frames, sort=True)

    result = result[result['DIVISION'] == 'EVACARE']# only for evacare
    prods = result['PRODUCT NAMAE']
    prods.dropna(inplace=True)
    prods = prods.unique()
    # print(prods)
    return render(request, 'dashboard.html', {"prods":prods})

def prm(request):
    # div = request.POST['month']
    mnth = request.POST['month']
    usr = curr_usr['usr_nm'][0]

    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]

    # ---------------------both bar chart----------------------
    result = pd.concat(frames, sort=True)

    result = result[result['DIVISION'] == 'EVACARE']

    months = result['PRODUCT NAMAE']
    months.dropna(inplace=True)
    month = months.unique()

    p1 = result[result['MONTH'] == 'Oct-19']  # neet to be soft coded
    p1 = p1[p1['DEPOT NAME'] == c]
    p1 = p1[['SAL QTY', 'PRODUCT NAMAE']]

    mdict = {}
    for i in range(len(p1["PRODUCT NAMAE"])):
        a = mdict[p1.iloc[i]["PRODUCT NAMAE"]] = p1.iloc[i]["SAL QTY"]

    df = pd.DataFrame(index=[''], data=mdict)
    ax = df.plot.bar()

    plt.title(c)
    plt.ylabel("QTY")

    plt.legend(bbox_to_anchor=(0.75,0.5), loc='center left')

    plt.title(c)
    plt.ylabel("SAL QTY")

    # plt.show()
    plt.rcParams['figure.figsize'] = (8,2)
    # plt.figure(figsize=(10,5))
    plt.savefig('D:\geo_master\static\abm.png',dpi=10)
    return render(request, 'dashboard.html')

def abm(request):

    cnx = pymysql.connect('localhost', 'root', 'root', 'new_pharma')
    table = pd.read_sql('select * from report_mr_level_month_fact', cnx)
    table1 = pd.read_sql('select * from report_1st_level_month_fact', cnx)

    Reporting_Region_abm = table1[table1['1st_Reporting_Region_Name'] == 'Vellore ABM ']

    months = Reporting_Region_abm[
        Reporting_Region_abm['report_month'].isin(['2019-August', '2019-September', '2019-October'])]

    val1 = months[['1st_Reporting_Region_Name', 'report_month', 'product_name', 'net_amt']]

    df_val = val1.groupby(['1st_Reporting_Region_Name', 'report_month', 'product_name']).sum()[['net_amt']]
    df_val = df_val.groupby(['product_name']).sum()[['net_amt']]

    df_val.dropna(inplace=True)
    df_val = df_val.reset_index()

    val = df_val['net_amt']
    item = df_val['product_name']

    df_val = df_val.reset_index()
    explode = (0.1, 0, 0, 0, 0, 0)

    def make_autopct(val):
        def my_autopct(pct):
            total = sum(val)
            val1 = int(round(pct * total / 100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val1)

        return my_autopct

    plt.title('Vellore ABM', bbox={'facecolor': '0.5', 'pad': 4})

    plt.pie(val, autopct=make_autopct(val), radius=1.0, startangle=90,
            pctdistance=1.2, labeldistance=1.5)
    plt.legend(item, fontsize=11, loc=(1.2, 0.1))

    plt.savefig('D:\geo_master\static\abm.png')
    return render(request, 'dashboard.html')

    # plt.savefig('D:/graphs/abm.png')


def spm(request):

    mnth = request.POST['month']
    usr = curr_usr['usr_nm'][0]

    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    # user_details = data1[data1['1st Reporting User Name'] == usr]
    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    # div_val = user_details.iloc[0]["Division_Values"]
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]
    # --------------------------------------ABM
    result = pd.concat(frames, sort=True)

    result = result[result['DIVISION'] == 'EVACARE']
    cochin = result[result['DEPOT NAME'] == c]
    oct = cochin[cochin['MONTH'] == mnth]  # need to be option on ui side
    val = oct['SAL VAL']

    prod = list(oct['PRODUCT NAMAE'])

    def make_autopct(val):
        def my_autopct(pct):
            total = sum(val)
            val1 = int(round(pct * total / 100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val1)

        return my_autopct
    plt.title('Sales Value'+' '+mnth, bbox={'facecolor':'0.9', 'pad':3})

    plt.pie(val, autopct=make_autopct(val), radius=1.1, startangle=60,
            pctdistance=1.3, labeldistance=1.5)
    plt.legend(prod, fontsize=10, loc=(1.3, 0.3))

    plt.savefig('D:\geo_master\static\SPM.png')
    return render(request, 'graph2.html')

def cup(request):
    prod = request.POST['prod']
    usr = curr_usr['usr_nm'][0]
    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')

    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    # user_details = data1[data1['1st Reporting User Name'] == usr]
    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    # div_val = user_details.iloc[0]["Division_Values"]
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]
    # --------------------------------------abm
    result = pd.concat(frames, sort=True)

    months = result['MONTH']
    months.dropna(inplace=True)
    month = months.unique()

    result = result[result['DIVISION'] == 'EVACARE']

    p1 = result[result['PRODUCT NAMAE'] == 'PRIWASH 100 ML']  # neet to be soft coded
    p1 = p1[p1['DEPOT NAME'] == c]
    p1 = p1[['SAL VAL', 'MONTH', 'SAL QTY']]

    mdict = {}
    for i in range(len(p1["MONTH"])):
        mdict[p1.iloc[i]["MONTH"]] = p1.iloc[i]["SAL QTY"]
    print(mdict)

    df = pd.DataFrame(index=[''], data=mdict)
    ax = df.plot.barh(stacked=True)

    plt.title(c+' '+str(prod))
    plt.xlabel("SAL QTY")

    plt.legend(bbox_to_anchor=(0.80,0.95), loc='center left')
    # plt.show()
    # plt.figure(figsize=(80,50))
    plt.savefig('D:\geo_master\static\cup.png')
    return render(request, 'graph3.html')


def cvp(request):
    prod = request.POST['prod']
    usr = curr_usr['usr_nm'][0]

    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')

    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')

    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]
    result = pd.concat(frames, sort=True)

    result = result[result['DIVISION'] == 'EVACARE']
    p1 = result[result['PRODUCT NAMAE'] == prod]
    p1 = p1[p1['DEPOT NAME'] == c]
    p1 = p1[['SAL VAL', 'MONTH']]

    mdict = {}
    for i in range(len(p1["MONTH"])):
        a = mdict[p1.iloc[i]["MONTH"]] = p1.iloc[i]["SAL VAL"]
    df = pd.DataFrame(index=[''], data=mdict)
    ax = df.plot.barh(stacked=True)

    plt.title(c+' '+str(prod))
    plt.xlabel("SAL VAL")

    plt.legend(bbox_to_anchor=(0.80,0.95), loc='center left')
    plt.savefig('D:\geo_master\static\cvp.png')
    return render(request, 'graph4.html')


def msgu(request):
    # mnth = request.POST['month']
    usr = curr_usr['usr_nm'][0]
    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')

    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    # user_details = data1[data1['1st Reporting User Name'] == usr]
    # div_val = user_details.iloc[0]["Division_Values"]
    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])
    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]
    result = pd.concat(frames, sort=True)
    result = result[result['DIVISION'] == "EVACARE"]
    test = result[result['DEPOT NAME'] == c]
    test = test[['DEPOT NAME', 'MONTH', 'PRODUCT NAMAE', 'SAL QTY', 'SAL VAL']]

    df_final_sale = test.groupby(['PRODUCT NAMAE', 'MONTH'], as_index=False).sum()

    fig, ax = plt.subplots(figsize=(15, 7))

    test.groupby(['MONTH', 'PRODUCT NAMAE']).sum()['SAL QTY'].unstack().plot(ax=ax)
    ax.set_xlabel('MONTH')
    ax.set_ylabel('Sale Quantity')
    ax.set_title(c)
    plt.legend(bbox_to_anchor=(1.01, 0.5), loc='center left')
    plt.savefig('D:\geo_master\static\msgu.png')
    return render(request, 'graph5.html')

def msgv(request):
    # mnth = request.POST['month']
    usr = curr_usr['usr_nm'][0]
    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    # user_details = data1[data1['1st Reporting User Name'] == usr]
    # div_val = user_details.iloc[0]["Division_Values"]
    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]

    result = pd.concat(frames, sort=True)

    result = result[result['DIVISION'] == "EVACARE"]
    test = result[result['DEPOT NAME'] == c]
    test = test[['DEPOT NAME', 'MONTH', 'PRODUCT NAMAE', 'SAL QTY', 'SAL VAL']]

    df_final_sale = test.groupby(['PRODUCT NAMAE', 'MONTH'], as_index=False).sum()

    fig, ax = plt.subplots(figsize=(15, 7))
    test.groupby(['MONTH', 'PRODUCT NAMAE']).sum()['SAL VAL'].unstack().plot(ax=ax)
    ax.set_xlabel('MONTHS')
    ax.set_ylabel('Sale Values')
    ax.set_title(c)

    plt.legend(bbox_to_anchor=(1.01, 0.5), )
    plt.savefig('D:\geo_master\static\msgv.png')
    return render(request, 'graph6.html')

def dsv(request):
    mnth = request.POST['month']
    usr = curr_usr['usr_nm'][0]

    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    # user_details = data1[data1['1st Reporting User Name'] == usr]
    # div_val = user_details.iloc[0]["Division_Values"]
    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])

    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)
    c = list(consigne_set)[0]
    # result = pd.concat(frames, sort=True)
    result = pd.read_csv('D:/db_sales/shield/daily_shield/daily_shield_sale.csv')

    result1 = result[result['Item Division'] == "EVACARE"]

    test = result1[result1['Consignee'] == c]

    test = test[['Consignee', 'Doc Date', 'Item Name FINAL', 'Qty.', 'Taxable Amt']]
    df_final_sale = test.groupby(['Item Name FINAL', 'Doc Date'], as_index=False).sum()
    fig, ax = plt.subplots(figsize=(15, 7))

    test.groupby(['Doc Date', 'Item Name FINAL']).sum()['Taxable Amt'].unstack().plot(ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sale Value')
    ax.set_title(c+' Nov-19')
    fig.autofmt_xdate()

    plt.legend(bbox_to_anchor=(1.01, 0.5), loc='center left')
    plt.savefig('D:\geo_master\static\dsv.png')
    return render(request, 'graph7.html')

def dsu(request):
    mnth = request.POST['month']
    usr = curr_usr['usr_nm'][0]

    cnx = pymysql.connect('localhost', 'root', 'root', 'nutri_db')
    data1 = pd.read_sql('select * from organogram_geo_master', cnx)
    data2 = pd.read_sql('select * from masterstockiest', cnx)
    data3 = pd.read_sql('select * from shield_cnf_stockist', cnx)

    # user_details = data1[data1['1st Reporting User Name'] == usr]
    # div_val = user_details.iloc[0]["Division_Values"]
    abm_df = data1[data1['1st Reporting Region Name'].str.contains('ABM')]
    abm = list(abm_df['1st Reporting User Name'])

    rbm_df = data1[data1['2nd Reporting Region Name'].str.contains('RBM')]
    rbm = list(rbm_df['2nd Reporting User Name'])

    if usr in abm:
        user_details = data1[data1['1st Reporting User Name'] == usr]
    elif usr in rbm:
        user_details = data1[data1['2nd Reporting User Name'] == usr]
    else:
        print('nope')
    region_name = user_details['Region Name']

    region_list = []
    for r in region_name:
        region_list.append(r.upper())

    doc = data2[data2['MR HI doctor'].isin(region_list)]
    parties = list(doc['Party Name.'])
    consigne_set = set()
    for p in parties:
        con_df = data3[data3['Party Name'] == parties[0]]
        consigne = con_df.iloc[0]['Consignee']
        consigne_set.add(consigne)

    c = list(consigne_set)[0]
    result = pd.read_csv('D:/db_sales/shield/daily_shield/daily_shield_sale.csv')
    result1 = result[result['Item Division'] == "EVACARE"]
    test = result1[result1['Consignee'] == c]
    test = test[['Consignee', 'Doc Date', 'Item Name FINAL', 'Qty.']]
    df_final_sale = test.groupby(['Item Name FINAL', 'Doc Date'], as_index=False).sum()
    fig, ax = plt.subplots(figsize=(15, 7))
    test.groupby(['Doc Date', 'Item Name FINAL']).sum()['Qty.'].unstack().plot(ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sale Qty')
    ax.set_title(c+' Nov-19')
    plt.legend(bbox_to_anchor=(1.01, 0.5), loc='center left')
    plt.savefig('D:\geo_master\static\dsu.png')
    return render(request, 'graph8.html')