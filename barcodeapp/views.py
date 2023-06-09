from django.shortcuts import render
from django.conf import settings
from .forms import DataForm
from qrcode import *
from django.db import connection,models
import barcode
import time
from django.http import HttpResponse
from barcode.writer import ImageWriter
from django.utils.encoding import smart_str
from io import BytesIO
from django.core.files import File
from django.http import JsonResponse

import random

FOOD_CHOICES = {"1": "Lunch",
                "2": "Dinner"}

FOOD_CHOICES_DASHBOARD = {
    "1": "Lunch",
    "2": "Dinner_veg",
    "3": "Dinner_Nonveg",
    "4": "Dinner_kid"
}

SERVICE_TYPE =(
    ("1", "Serviced"),
    ("2", "Not Services")
)

def footballclubs(request):
    print("footballclubs entry..")
    with connection.cursor() as cursor:
        select_q = "select * from saikat_rsvp.rsvp_food"
        cursor.execute(select_q)
        print(select_q)
        res_sel = dictfectchall(cursor)
        print(res_sel)
        print("length {0}".format(len(res_sel)))
        if len(res_sel) > 0:
            details_info = []
            barcode_info = []
            for each_row in res_sel:
                print(each_row["Name_Pri"])
                details = {}
                details['name'] = each_row["Name_Pri"]
                details['email'] = each_row["Email"]
                details['lunch'] = each_row["Lunch_all"]
                details['Dinner_veg'] = each_row["Dinner_veg"]
                details['Dinner_nveg'] = each_row["Dinner_nveg"]
                details['Dinner_kid'] = each_row["Dinner_kid"]
                select_f = "select * from saikat_rsvp.food_update as t1 where t1.rsvp_userid = '{0}'".format(each_row["ID"])
                cursor.execute(select_f)
                print(select_f)
                res_sel_f = dictfectchall(cursor)
                print("length {0}".format(len(res_sel_f)))
                for each_row_f in res_sel_f:
                    details['lunch_coupon'] = each_row_f["lunch"]
                    details['dinnerv_coupon'] = each_row_f["dinnerv"]
                    details['dinnernonv_coupon'] = each_row_f["dinnernv"]
                    details['dinnernkid_coupon'] = each_row_f["dinnerkid"]
                details_info.append(details)
                select_b = "select * from saikat_rsvp.food_update as t1 inner join saikat_rsvp.barcode_scan as t2 where t1.id = t2.food_update_id and t1.rsvp_userid = '{0}'".format(each_row["ID"])
                cursor.execute(select_b)
                print(select_b)
                res_b = dictfectchall(cursor)
                print("length {0}".format(len(res_b)))
                #lcount = len(res_b)
                for each_row_b in res_b:
                    details_b = {}
                    details_b['food_type'] = each_row_b["food_type"]
                    details_b['barcode_num'] = each_row_b["barcode_num"]
                    details_b['food_service'] = each_row_b["food_service"]
                    barcode_info.append(details_b)

            #return JsonResponse(data={'food_data': details_info,"barcode_data": barcode_info}, safe=False)
            return JsonResponse(details_info, safe=False)


def scancode(request,code):
    print("here... {0}".format(code))

    with connection.cursor() as cursor:
        select_q = "select * from saikat_rsvp.barcode_scan as t1 where t1.barcode_num = '{0}' and food_service = 'Y'".format(code)
        cursor.execute(select_q)
        print(select_q)
        res_sel = cursor.fetchall()
        print(res_sel)
        print("length {0}".format(len(res_sel)))
        if len(res_sel) > 0:
            details_info = []
            cursor.execute("select food_update_id,food_service,food_type from saikat_rsvp.barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
            res = dictfectchall(cursor)
            print("done")
            for each_row1 in res:
                print(each_row1["food_update_id"])
                cursor.execute("select * from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
                res1 = dictfectchall(cursor)
                print("done2")
                details = {}
                for each_row in res1:
                    print(each_row["Name_Pri"])
                    details['name'] = each_row["Name_Pri"]
                    details['email'] = each_row["Email"]
                    details['Lunch_all'] = each_row["Lunch_all"]
                    details['Dinner_veg'] = each_row["Dinner_veg"]
                    details['Dinner_nveg'] = each_row["Dinner_nveg"]
                    details['Dinner_kid'] = each_row["Dinner_kid"]
                    details['Volunteering'] = each_row["Volunteering"]
                    details['lunch'] = each_row["lunch"]
                    details['dinnerv'] = each_row["dinnerv"]
                    details['dinnernv'] = each_row["dinnernv"]
                    details['dinnerkid'] = each_row["dinnerkid"]
                    details['food_type'] = each_row1["food_type"]
                    details['foods'] = "AlreadyServed"
                    details_info.append(details)
            return JsonResponse(data={'barcode_data': details_info})
        else:
            update_q = "update saikat_rsvp.barcode_scan as t1 set food_service='Y' where t1.barcode_num = '{0}'".format(code)
            print(update_q)
            cursor.execute(update_q)
            connection.commit()


            details_info = []
            cursor.execute("select food_update_id,food_service,food_type from saikat_rsvp.barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
            res = dictfectchall(cursor)
            print("done")
            for each_row1 in res:
                print(each_row1["food_update_id"])
                cursor.execute("select * from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
                res1 = dictfectchall(cursor)
                print("done2")
                details = {}
                for each_row in res1:
                    print(each_row["Name_Pri"])
                    details['name'] = each_row["Name_Pri"]
                    details['email'] = each_row["Email"]
                    details['Lunch_all'] = each_row["Lunch_all"]
                    details['Dinner_veg'] = each_row["Dinner_veg"]
                    details['Dinner_nveg'] = each_row["Dinner_nveg"]
                    details['Dinner_kid'] = each_row["Dinner_kid"]
                    details['Volunteering'] = each_row["Volunteering"]
                    details['lunch'] = each_row["lunch"]
                    details['dinnerv'] = each_row["dinnerv"]
                    details['dinnernv'] = each_row["dinnernv"]
                    details['dinnerkid'] = each_row["dinnerkid"]
                    details['food_type'] = each_row1['food_type']
                    if(each_row1["food_service"]) == 'Y':
                        details['foods'] = "Served"
                    else:
                        details['foods'] = "Not Served"
                    details_info.append(details)

            return JsonResponse(data={'barcode_data': details_info})
    #return HttpResponse("Success!")

def generate_file(barcode_file):
    #output = HttpResponse(content_type="image/jpeg")
    output = HttpResponse(content_type="application/force-download")
    barcode_file.save(output, "JPEG")
    output['Content-Disposition'] = 'attachment; filename=%s' % smart_str('barcode.jpg')
    output['X-Sendfile'] = smart_str('barcode.jpg')
    return output


def dictfectchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]


def foodscan(request):
    data = "info"
    return render(request, 'scan.html',{'data': data});


def qr_gen(request):
    context = {
        'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']
    }
    global gform
    if request.method == 'POST':
        b_type = request.POST['typeOfBarcode']
        b_data = request.POST['barcodeData']
        form = DataForm(request.POST)
        gform = form





        if b_type == 'qrcode':
            data = request.POST['data']
            img = make(data)
            img_name = f'qr_{time.time()}.png'
            img.save(settings.MEDIA_ROOT/img_name)


            return render(request, 'index.html', {'img_name': img_name})
        else:

            if 'search' in request.POST:
                print("hello")
                print(name_info)

                details = {}
                details_info = []
                with connection.cursor() as cursor:
                    cursor.execute("select * from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
                    res = dictfectchall(cursor)
                    print("done")
                    for each_row in res:
                        print(each_row["Name_Pri"])
                        details['name'] = each_row["Name_Pri"]
                        details['email'] = each_row["Email"]
                        details['Lunch_all'] = each_row["Lunch_all"]
                        details['Dinner_veg'] = each_row["Dinner_veg"]
                        details['Dinner_nveg'] = each_row["Dinner_nveg"]
                        details['Dinner_kid'] = each_row["Dinner_kid"]
                        details['Volunteering'] = each_row["Volunteering"]
                        details['lunch'] = each_row["lunch"]
                        details_info.append(details)
                return render(request, 'index.html', {'form':form, 'details_info':details_info,'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']})
            elif('generate' in request.POST):
                name_info = str(gform.data['name_field'])
                temp = FOOD_CHOICES[request.POST['food_field']]
                print("temp_data {0}".format(temp))

                barcode1 = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)
                #bar = barcode.get_barcode(name=b_type, code=b_data, writer=ImageWriter())
                #barcode_file = bar.render() # creates a PIL class image object
                #print(barcode_file)
                #out = generate_file(barcode_file) # generate the file
                #print(out)
                details_info = []
                filename = []

                with connection.cursor() as cursor:
                    cursor.execute("select Name_Pri,Email,Lunch_all,Dinner_veg,Dinner_nveg,Dinner_kid,Volunteering,lunch,dinnerv,dinnernv,dinnerkid,t2.id as foodid from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
                    res = dictfectchall(cursor)
                    print("done")
                    if res and len(res) > 0:
                        print(filename)
                        for each_row in res:
                            print(each_row["Name_Pri"])
                            details = {}
                            details['name'] = each_row["Name_Pri"]
                            details['email'] = each_row["Email"]
                            details['Lunch_all'] = each_row["Lunch_all"]
                            details['Dinner_veg'] = each_row["Dinner_veg"]
                            details['Dinner_nveg'] = each_row["Dinner_nveg"]
                            details['Dinner_kid'] = each_row["Dinner_kid"]
                            details['Volunteering'] = each_row["Volunteering"]
                            details['lunch'] = each_row["lunch"]
                            fod_head_count = each_row["Lunch_all"]
                            id = each_row["foodid"]
                            details_info.append(details)

                            if temp == "Lunch" and each_row["lunch"] == 'Y':
                                update_q = "update saikat_rsvp.food_update as t1 inner join saikat_rsvp.rsvp_food as t2 set lunch='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                print(update_q)
                                cursor.execute(update_q)
                                connection.commit()

                                while fod_head_count > 0:
                                    data_barcode = ""
                                    value = random.randint(1000000000000, 9999999999999)
                                    print("value = {0}".format(value))
                                    img_name = f'qr_{time.time()}'
                                    img_name = each_row["Name_Pri"] + "_" + img_name + "_lunch_" + str(fod_head_count)
                                    filename_map = {}
                                    '''for num in b_data:
                                        data_barcode = data_barcode + str(ord(num))'''

                                    data_barcode = data_barcode + str(value) + str(ord(str(fod_head_count)))
                                    for num in temp:
                                        data_barcode = data_barcode + str(ord(num))
                                    print("data_barcode {0}".format(data_barcode))
                                    EAN = barcode.get_barcode_class('ean13')
                                    ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                    print("ean {0}".format(ean))
                                    #buffer = BytesIO()
                                    #ean.write(buffer)
                                    filename_map["lunch_" + str(fod_head_count)] = ean.save(f'{settings.MEDIA_ROOT/img_name}')
                                    filename.append(filename_map)
                                    fod_head_count = fod_head_count - 1
                                    insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'lunch', '{1}','N')".format(id,ean)
                                    print("insertq {0}".format(insertq))
                                    cursor.execute(insertq)
                                    connection.commit()
                            elif temp == "Dinner" and (each_row["dinnerv"] == 'N' and each_row["dinnernv"] == 'N' and each_row["dinnerkid"] == 'N'):
                                update_q = "update saikat_rsvp.food_update as t1 inner join saikat_rsvp.rsvp_food as t2 set dinnerv='Y',dinnernv='Y',dinnerkid='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                print(update_q)
                                cursor.execute(update_q)
                                connection.commit()
                                fod_head_count_dinner = each_row["Dinner_veg"]+ each_row["Dinner_nveg"]+ each_row["Dinner_kid"]
                                dinner_map = {"veg": each_row["Dinner_veg"],
                                              "nveg": each_row["Dinner_nveg"],
                                              "kid": each_row["Dinner_kid"]}

                                vcount = dinner_map["veg"]
                                nvcount = dinner_map["nveg"]
                                kcount = dinner_map["nveg"]
                                while fod_head_count_dinner > 0:
                                    data_barcode = ""
                                    value = random.randint(1000000000000, 9999999999999)
                                    print("value = {0}".format(value))
                                    img_name_d = f'qr_{time.time()}'
                                    img_name_d = each_row["Name_Pri"] + "_" + img_name_d
                                    filename_map = {}
                                    '''for num in b_data:
                                        data_barcode = data_barcode + str(ord(num))'''

                                    data_barcode = data_barcode + str(value) + str(ord(str(fod_head_count_dinner)))
                                    for num in temp:
                                        data_barcode = data_barcode + str(ord(num))
                                    print("data_barcode {0}".format(data_barcode))
                                    EAN = barcode.get_barcode_class('ean13')

                                    if (vcount > 0):
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        print("ean {0}".format(ean))
                                        img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                        filename_map["dinner_veg_" +str(vcount)] = ean.save(f'{settings.MEDIA_ROOT/img_name_d}.png')
                                        filename.append(filename_map)
                                        insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'dinner_veg', '{1}','N')".format(id,ean)
                                        vcount = vcount - 1
                                    elif(nvcount > 0):
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        print("ean {0}".format(ean))
                                        img_name_d = img_name_d + '_dinner_nveg_' + str(nvcount)
                                        filename_map["dinner_nveg_" +str(nvcount)] = ean.save(f'{settings.MEDIA_ROOT/img_name_d}.png')
                                        filename.append(filename_map)
                                        insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'dinner_nveg', '{1}','N')".format(id,ean)
                                        nvcount = nvcount - 1
                                    elif(kcount > 0):
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        print("ean {0}".format(ean))
                                        img_name_d = img_name_d + '_dinner_kid_' + str(kcount)
                                        filename_map["dinner_kid_" +str(kcount)] = ean.save(f'{settings.MEDIA_ROOT/img_name_d}.png')
                                        filename.append(filename_map)
                                        insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'dinner_kid', '{1}','N')".format(id,ean)
                                        kcount = kcount - 1
                                    fod_head_count_dinner = fod_head_count_dinner - 1

                                    print("insertq {0}".format(insertq))
                                    cursor.execute(insertq)
                                    connection.commit()
                return render(request, 'index.html', {'form':form, 'details_info':details_info,'img_name':filename,'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']})

            elif('autogenerate' in request.POST):
                name_info_list = []
                with connection.cursor() as cursor:
                    cursor.execute("select Name_Pri,Email from saikat_rsvp.rsvp_food")
                    res_email_list = dictfectchall(cursor)
                    for each_email in res_email_list:
                        name_info_list.append(each_email["Email"])
                for name_info in name_info_list:
                    #name_info = str(gform.data['name_field'])
                    temp = FOOD_CHOICES[request.POST['food_field']]
                    print("temp_data {0}".format(temp))

                    barcode1 = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)
                    #bar = barcode.get_barcode(name=b_type, code=b_data, writer=ImageWriter())
                    #barcode_file = bar.render() # creates a PIL class image object
                    #print(barcode_file)
                    #out = generate_file(barcode_file) # generate the file
                    #print(out)
                    details_info = []
                    filename = []

                    with connection.cursor() as cursor:
                        cursor.execute("select Name_Pri,Email,Lunch_all,Dinner_veg,Dinner_nveg,Dinner_kid,Volunteering,lunch,dinnerv,dinnernv,dinnerkid,t2.id as foodid from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
                        res = dictfectchall(cursor)
                        print("done")
                        if res and len(res) > 0:
                            print(filename)
                            for each_row in res:
                                print(each_row["Name_Pri"])
                                details = {}
                                details['name'] = each_row["Name_Pri"]
                                details['email'] = each_row["Email"]
                                details['Lunch_all'] = each_row["Lunch_all"]
                                details['Dinner_veg'] = each_row["Dinner_veg"]
                                details['Dinner_nveg'] = each_row["Dinner_nveg"]
                                details['Dinner_kid'] = each_row["Dinner_kid"]
                                details['Volunteering'] = each_row["Volunteering"]
                                details['lunch'] = each_row["lunch"]
                                fod_head_count = each_row["Lunch_all"]
                                id = each_row["foodid"]
                                details_info.append(details)

                                if temp == "Lunch" and each_row["lunch"] == 'N':
                                    update_q = "update saikat_rsvp.food_update as t1 inner join saikat_rsvp.rsvp_food as t2 set lunch='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                    print(update_q)
                                    cursor.execute(update_q)
                                    connection.commit()

                                    while fod_head_count > 0:
                                        data_barcode = ""
                                        value = random.randint(1000000000000, 9999999999999)
                                        print("value = {0}".format(value))
                                        img_name = f'qr_{time.time()}'
                                        img_name = each_row["Name_Pri"] + "_" + img_name + "_lunch_" + str(fod_head_count)
                                        filename_map = {}
                                        '''for num in b_data:
                                            data_barcode = data_barcode + str(ord(num))'''

                                        data_barcode = data_barcode + str(value) + str(ord(str(fod_head_count)))
                                        for num in temp:
                                            data_barcode = data_barcode + str(ord(num))
                                        print("data_barcode {0}".format(data_barcode))
                                        EAN = barcode.get_barcode_class('ean13')
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        print("ean {0}".format(ean))
                                        #buffer = BytesIO()
                                        #ean.write(buffer)
                                        filename_map["lunch_" + str(fod_head_count)] = ean.save(f'{settings.MEDIA_ROOT/img_name}')
                                        filename.append(filename_map)
                                        fod_head_count = fod_head_count - 1
                                        insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'lunch', '{1}','N')".format(id,ean)
                                        print("insertq {0}".format(insertq))
                                        cursor.execute(insertq)
                                        connection.commit()
                                elif temp == "Dinner" and (each_row["dinnerv"] == 'N' and each_row["dinnernv"] == 'N' and each_row["dinnerkid"] == 'N'):
                                    update_q = "update saikat_rsvp.food_update as t1 inner join saikat_rsvp.rsvp_food as t2 set dinnerv='Y',dinnernv='Y',dinnerkid='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                    print(update_q)
                                    cursor.execute(update_q)
                                    connection.commit()
                                    fod_head_count_dinner = each_row["Dinner_veg"]+ each_row["Dinner_nveg"]+ each_row["Dinner_kid"]
                                    dinner_map = {"veg": each_row["Dinner_veg"],
                                                  "nveg": each_row["Dinner_nveg"],
                                                  "kid": each_row["Dinner_kid"]}

                                    vcount = dinner_map["veg"]
                                    nvcount = dinner_map["nveg"]
                                    kcount = dinner_map["nveg"]
                                    while fod_head_count_dinner > 0:
                                        data_barcode = ""
                                        value = random.randint(1000000000000, 9999999999999)
                                        print("value = {0}".format(value))
                                        img_name_d = f'qr_{time.time()}'
                                        img_name_d = each_row["Name_Pri"] + "_" + img_name_d
                                        filename_map = {}
                                        '''for num in b_data:
                                            data_barcode = data_barcode + str(ord(num))'''

                                        data_barcode = data_barcode + str(value) + str(ord(str(fod_head_count_dinner)))
                                        for num in temp:
                                            data_barcode = data_barcode + str(ord(num))
                                        print("data_barcode {0}".format(data_barcode))
                                        EAN = barcode.get_barcode_class('ean13')

                                        if (vcount > 0):
                                            ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                            print("ean {0}".format(ean))
                                            img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                            filename_map["dinner_veg_" +str(vcount)] = ean.save(f'{settings.MEDIA_ROOT/img_name_d}.png')
                                            filename.append(filename_map)
                                            insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'dinner_veg', '{1}','N')".format(id,ean)
                                            vcount = vcount - 1
                                        elif(nvcount > 0):
                                            ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                            print("ean {0}".format(ean))
                                            img_name_d = img_name_d + '_dinner_nveg_' + str(nvcount)
                                            filename_map["dinner_nveg_" +str(nvcount)] = ean.save(f'{settings.MEDIA_ROOT/img_name_d}.png')
                                            filename.append(filename_map)
                                            insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'dinner_nveg', '{1}','N')".format(id,ean)
                                            nvcount = nvcount - 1
                                        elif(kcount > 0):
                                            ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                            print("ean {0}".format(ean))
                                            img_name_d = img_name_d + '_dinner_kid_' + str(kcount)
                                            filename_map["dinner_kid_" +str(kcount)] = ean.save(f'{settings.MEDIA_ROOT/img_name_d}.png')
                                            filename.append(filename_map)
                                            insertq = "INSERT INTO saikat_rsvp.barcode_scan (food_update_id, food_type, barcode_num,food_service) VALUES ('{0}', 'dinner_kid', '{1}','N')".format(id,ean)
                                            kcount = kcount - 1
                                        fod_head_count_dinner = fod_head_count_dinner - 1

                                        print("insertq {0}".format(insertq))
                                        cursor.execute(insertq)
                                        connection.commit()
                                elif temp == "Lunch" and each_row["lunch"] == 'Y':
                                    nameimg = 'lunch.jpg'
                                    filename_map = {}
                                    filename_map["idata"] = settings.MEDIA_ROOT/nameimg
                                    filename.append(filename_map)

                return render(request, 'index.html', {'form':form, 'details_info':details_info,'img_name':filename,'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']})

            #return render(request, 'index.html', {'img_name': filename,'form':form})
    else:
        with connection.cursor() as cursor:
            cursor.execute("select * from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid ")
            res = dictfectchall(cursor)
            print("done")

            details_info = []
            for each_row in res:
                details = {}
                print(each_row["Name_Pri"])
                details['name'] = each_row["Name_Pri"]
                details['email'] = each_row["Email"]
                details['Lunch_all'] = each_row["Lunch_all"]
                details['Dinner_veg'] = each_row["Dinner_veg"]
                details['Dinner_nveg'] = each_row["Dinner_nveg"]
                details['Dinner_kid'] = each_row["Dinner_kid"]
                details['Volunteering'] = each_row["Volunteering"]
                details['lunch'] = each_row["lunch"]

                details_info.append(details)
        form = DataForm()
        print(details_info)
        return render(request, 'index.html', {'form':form, 'details_info':details_info,'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']})


def dashboard(request):
     context = {}
     global gform
     form = DataForm(request.POST)
     gform = form
     select_q = "select * from saikat_rsvp.rsvp_food"
     with connection.cursor() as cursor:
         cursor.execute(select_q)
         print(select_q)
         res_sel = dictfectchall(cursor)
         print("length {0}".format(len(res_sel)))
         if len(res_sel) > 0:
            lunch_count = 0
            dinner_veg_count = 0
            dinner_nveg_count = 0
            dinner_kid_count = 0
            for each_row in res_sel:
               lunch_count = lunch_count + int(each_row['Lunch_all'])
               dinner_veg_count = dinner_veg_count + int(each_row['Dinner_veg'])
               dinner_nveg_count = dinner_nveg_count + int(each_row['Dinner_nveg'])
               dinner_kid_count = dinner_kid_count + int(each_row['Dinner_kid'])

     if request.method == 'POST':
            if 'fetch' in request.POST:
                print("hello dashboard {0}".format(request.POST['food_dash']))
                temp = FOOD_CHOICES_DASHBOARD[request.POST['food_dash']]
                print(temp)
                details_info = []
                coupon_given = 0
                coupon_not_given = 0
                food_serviced = 0
                food_not_serviced = 0
                with connection.cursor() as cursor:
                    cursor.execute("select * from saikat_rsvp.food_update as t1 inner join saikat_rsvp.barcode_scan as t2 where t1.id = t2.food_update_id and t2.food_type = '{0}'".format(temp))
                    res = dictfectchall(cursor)
                    print("done")
                    for each_row in res:
                        details = {}
                        cursor.execute("select * from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t2.id = '{0}'".format(each_row['food_update_id']))
                        res1 = dictfectchall(cursor)
                        if (temp == "Lunch"):
                            details['coupon'] = each_row["lunch"]
                        if (temp == "Dinner_veg"):
                            details['coupon'] = each_row["dinnerv"]
                        if (temp == "Dinner_Nonveg"):
                            details['coupon'] = each_row["dinnerv"]
                        if (temp == "Dinner_kid"):
                            details['coupon'] = each_row["dinnerkid"]
                        details['name'] = res1[0]["Name_Pri"]
                        details['email'] = res1[0]["Email"]
                        details['food_type'] = temp
                        details['barcode_num'] = each_row["barcode_num"]
                        if (each_row["food_service"] == "Y"):
                            details['food_service'] = "given"
                            food_serviced = food_serviced + 1
                        else:
                            details['food_service'] = "not given"
                            food_not_serviced = food_not_serviced + 1

                        if (details["coupon"] == "Y"):
                            details['coupon'] = "Coupon done"
                            coupon_given = coupon_given + 1
                        else:
                            details['coupon'] = "coupon notdone"
                        details_info.append(details)
                print(details_info)
                if(temp == 'Lunch'):
                    coupon_not_given =  lunch_count - coupon_given
                if(temp == 'Dinner_veg'):
                    coupon_not_given =  dinner_veg_count - coupon_given
                if(temp == 'Dinner_Nonveg'):
                    coupon_not_given =  dinner_nveg_count - coupon_given
                if(temp == 'Dinner_kid'):
                    coupon_not_given =  dinner_kid_count - coupon_given
                return render(request, 'dashboard.html', {'form':form, 'details_info':details_info,'lunch_count':lunch_count,'dinner_veg_count':dinner_veg_count,'dinner_nveg_count':dinner_nveg_count,'dinner_kid_count':dinner_kid_count,
                                                          'food_type':temp,'coupon_not_given':coupon_not_given,'coupon_given':coupon_given,'food_serviced':food_serviced,'food_not_serviced':food_not_serviced})
            else:
                return render(request, 'dashboard.html',{'form':form})
     return render(request, 'dashboard.html',{'form':form, 'lunch_count':lunch_count,'dinner_veg_count':dinner_veg_count,'dinner_nveg_count':dinner_nveg_count,'dinner_kid_count':dinner_kid_count})
