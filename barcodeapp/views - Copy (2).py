from django.shortcuts import render
from django.conf import settings
from .forms import DataForm
from django.db import connection,models
import barcode
import time
from django.http import HttpResponse
from barcode.writer import ImageWriter
from django.utils.encoding import smart_str
from io import BytesIO
from django.core.files import File
from django.http import JsonResponse
import code128
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
import random

import smtplib, os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE, formatdate

FOOD_CHOICES = {"1": "Lunch",
                "2": "Dinner"}

FOOD_CHOICES_DASHBOARD = {
    "1": "Lunch",
    "2": "Dinner_veg",
    "3": "Dinner_nveg",
    "4": "Dinner_kid"
}

SERVICE_TYPE =(
    ("1", "Serviced"),
    ("2", "Not Services")
)
def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    # storing the senders email address
    msg['From'] = send_from
    # storing the receivers email address
    msg['To'] = send_to
    # storing the subject
    msg['Subject'] = subject

    # string to store the body of the mail
    body = text
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    #filename = files
    #attachment = open(filename, "rb")
    for f in files:  # add files to the message
        #file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(f, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)

    # instance of MIMEBase and named as p
    #p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    #p.set_payload((attachment).read())
    # encode into base64
    #encoders.encode_base64(p)

    #p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # attach the instance 'p' to instance 'msg'
    #msg.attach(p)
    # creates SMTP session
    #s = smtplib.SMTP_SSL('smtp.gmail.com')
    #s = smtplib.SMTP('smtp.gmail.com', 587)
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()


    # start TLS for security
    #s.ehlo()
    #s.starttls()

    # Authentication
    print(send_from)
    #s.login(send_from, "flyryksfluycnyhl")
    s.login(send_from, "sumw bbpr gkzf uaao")


    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(send_from, send_to, text)

    # terminating the session
    #s.close()
    #s.ehlo()
    s.quit()

def footballclubs(request):
    print("footballclubs entry..")
    with connection.cursor() as cursor:
        select_q = "select * from saikat_rsvp.sp_rsvp_food"
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
                select_f = "select * from saikat_rsvp.sp_food_update as t1 where t1.rsvp_userid = '{0}'".format(each_row["ID"])
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
                select_b = "select * from saikat_rsvp.sp_food_update as t1 inner join saikat_rsvp.sp_barcode_scan as t2 where t1.id = t2.food_update_id and t1.rsvp_userid = '{0}'".format(each_row["ID"])
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

def invalidation(request,code):
    print("here... invalidation {0}".format(code))
    file_hist_data = []
    #file_hist_data.append("ok")

    with connection.cursor() as cursor:
        update_q = "update saikat_rsvp.sp_barcode_scan as t1 set food_service='invalid' where t1.barcode_num = '{0}'".format(code)
        print(update_q)
        cursor.execute(update_q)
        connection.commit()
        select_q = "select t1.id as TID, t2.id as food_update_id,t3.id as id,food_service,barcode_num,Name_Pri,Email,food_type,filename from saikat_rsvp.sp_barcode_scan as t1 inner join saikat_rsvp.sp_food_update as t2 inner join saikat_rsvp.sp_rsvp_food as t3  where t1.food_update_id = t2.id and t2.rsvp_userid = t3.id and t1.barcode_num = '{0}'".format(code)
        cursor.execute(select_q)
        print(select_q)
        res_sel = dictfectchall(cursor)
        print(res_sel)
        print("length {0}".format(len(res_sel)))
        if len(res_sel) > 0:
            details_info = []
            for each_row in res_sel:
                print(each_row["food_update_id"])
                details = {}
                print(each_row["Name_Pri"])
                details['name'] = each_row["Name_Pri"]
                details['email'] = each_row["Email"]
                details['id'] = each_row["TID"]
                details['food_update_id'] = each_row["food_update_id"]
                details['rsvpid'] = each_row["id"]
                details['barcode_num'] = each_row["barcode_num"]
                details['filename'] = each_row["filename"]
                details['food_type'] = each_row["food_type"]
                details['food_service'] = each_row["food_service"]

                file_hist_data.append(details)
    return render(request, 'partial_page.html', {'file_hist_data':file_hist_data});

def fetchmember(request,ID):
    print("here... fetchmember {0}".format(ID))
    file_hist_data = []
    global gform
    form = DataForm(request.POST)
    with connection.cursor() as cursor:
        select_q = "select t1.id as TID, t2.id as food_update_id,t3.id as id,food_service,barcode_num,Name_Pri,Email,food_type,filename from saikat_rsvp.sp_barcode_scan as t1 inner join saikat_rsvp.sp_food_update as t2 inner join saikat_rsvp.sp_rsvp_food as t3  where t1.food_update_id = t2.id and t2.rsvp_userid = t3.id and t3.id = '{0}'".format(ID)
        cursor.execute(select_q)
        print(select_q)
        res_sel = dictfectchall(cursor)
        print(res_sel)
        print("length {0}".format(len(res_sel)))
        if len(res_sel) > 0:
            details_info = []
            for each_row in res_sel:
                print(each_row["food_update_id"])
                details = {}
                print(each_row["Name_Pri"])
                details['name'] = each_row["Name_Pri"]
                details['email'] = each_row["Email"]
                details['id'] = each_row["TID"]
                details['food_update_id'] = each_row["food_update_id"]
                details['rsvpid'] = each_row["id"]
                details['barcode_num'] = each_row["barcode_num"]
                details['filename'] = each_row["filename"]
                details['food_type'] = each_row["food_type"]
                details['food_service'] = each_row["food_service"]

                file_hist_data.append(details)

            #return JsonResponse(data={'barcode_data': details_info})
            print(file_hist_data)
            return render(request, 'partial_page.html', {'file_hist_data':file_hist_data});
            #return JsonResponse({"file_hist_data": file_hist_data})
    #return HttpResponse("Success!")

def scancode(request,code):
    print("here... {0}".format(code))
    with connection.cursor() as cursor:
        select_q = "select * from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}' and food_service = 'invalid'".format(code)
        cursor.execute(select_q)
        print(select_q)
        res_sel = cursor.fetchall()
        print(res_sel)
        print("length {0}".format(len(res_sel)))
        if len(res_sel) > 0:
            details_info = []
            cursor.execute("select food_update_id,food_service,food_type,barcode_num from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
            res = dictfectchall(cursor)
            print("done")
            for each_row1 in res:
                print(each_row1["food_update_id"])
                cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
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
                    details['foods'] = "invalidcoupon"
                    details["total_dinner"] = details['Dinner_veg'] + details['Dinner_nveg'] + details['Dinner_kid']
                    details["barcode_num"] = each_row1["barcode_num"]
                    details["food_update_id"] = each_row1["food_update_id"]
                    details_info.append(details)
            return JsonResponse(data={'barcode_data': details_info})

        else:
            select_q = "select * from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}' and food_service = 'Y'".format(code)
            cursor.execute(select_q)
            print(select_q)
            res_sel = cursor.fetchall()
            print(res_sel)
            print("length {0}".format(len(res_sel)))
            if len(res_sel) > 0:
                details_info = []
                cursor.execute("select food_update_id,food_service,food_type, barcode_num from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
                res = dictfectchall(cursor)
                print("done")
                for each_row1 in res:
                    print(each_row1["food_update_id"])
                    cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
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
                        details["total_dinner"] = details['Dinner_veg'] + details['Dinner_nveg'] + details['Dinner_kid']
                        details["barcode_num"] = each_row1["barcode_num"]
                        details["food_update_id"] = each_row1["food_update_id"]
                        details_info.append(details)
                return JsonResponse(data={'barcode_data': details_info})
            else:
                update_q = "update saikat_rsvp.sp_barcode_scan as t1 set food_service='Y' where t1.barcode_num = '{0}'".format(code)
                print(update_q)
                cursor.execute(update_q)
                connection.commit()


                details_info = []
                cursor.execute("select food_update_id,food_service,food_type,barcode_num from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
                res = dictfectchall(cursor)
                print("done")
                for each_row1 in res:
                    print(each_row1["food_update_id"])
                    cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
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
                        details["total_dinner"] = details['Dinner_veg'] + details['Dinner_nveg'] + details['Dinner_kid']
                        details["barcode_num"] = each_row1["barcode_num"]
                        details["food_update_id"] = each_row1["food_update_id"]
                        details_info.append(details)

                return JsonResponse(data={'barcode_data': details_info})
    #return HttpResponse("Success!")


def viewcode(request,code):
    print("viewcode here... {0}".format(code))
    with connection.cursor() as cursor:
        select_q = "select * from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}' and food_service = 'invalid'".format(code)
        cursor.execute(select_q)
        print(select_q)
        res_sel = cursor.fetchall()
        print(res_sel)
        print("length {0}".format(len(res_sel)))
        if len(res_sel) > 0:
            details_info = []
            cursor.execute("select food_update_id,food_service,food_type,barcode_num from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
            res = dictfectchall(cursor)
            print("done")
            for each_row1 in res:
                print(each_row1["food_update_id"])
                cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
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
                    details['foods'] = "invalidcoupon"
                    details["total_dinner"] = details['Dinner_veg'] + details['Dinner_nveg'] + details['Dinner_kid']
                    details["barcode_num"] = each_row1["barcode_num"]
                    details["food_update_id"] = each_row1["food_update_id"]
                    details_info.append(details)
            return JsonResponse(data={'barcode_data': details_info})

        else:
            select_q = "select * from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}'".format(code)
            cursor.execute(select_q)
            print(select_q)
            res_sel = cursor.fetchall()
            print(res_sel)
            print("length {0}".format(len(res_sel)))
            if len(res_sel) > 0:
                details_info = []
                cursor.execute("select food_update_id,food_service,food_type, barcode_num from saikat_rsvp.sp_barcode_scan as t1 where t1.barcode_num = '{0}'".format(code))
                res = dictfectchall(cursor)
                print("done")
                for each_row1 in res:
                    print(each_row1["food_update_id"])
                    cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t2.ID = '{0}'".format(each_row1["food_update_id"]))
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
                        details['foods'] =  each_row1["food_service"]
                        details["total_dinner"] = details['Dinner_veg'] + details['Dinner_nveg'] + details['Dinner_kid']
                        details["barcode_num"] = each_row1["barcode_num"]
                        details["food_update_id"] = each_row1["food_update_id"]
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

def viewinfo(request):
    data = "barcodeinfo"
    return render(request, 'viewinfo.html',{'data': data});

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

        name_info = str(gform.data['name_field'])



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
                    cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
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
                    cursor.execute("select Name_Pri,Email,Lunch_all,Dinner_veg,Dinner_nveg,Dinner_kid,Volunteering,lunch,dinnerv,dinnernv,dinnerkid,t2.id as foodid from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
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
                                update_q = "update saikat_rsvp.sp_food_update as t1 inner join saikat_rsvp.sp_rsvp_food as t2 set lunch='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                print(update_q)
                                cursor.execute(update_q)
                                connection.commit()

                                while fod_head_count > 0:
                                    data_barcode = ""
                                    value = random.randint(1000000000000, 9999999999999)
                                    print("value = {0}".format(value))
                                    #img_name = f'qr_{time.time()}'
                                    #img_name = each_row["Name_Pri"] + "_" + img_name + "_lunch_" + str(fod_head_count)
                                    filename_map = {}
                                    '''for num in b_data:
                                        data_barcode = data_barcode + str(ord(num))'''




                                    data_barcode = data_barcode + str(value) + str(ord(str(fod_head_count)))
                                    for num in temp:
                                        data_barcode = data_barcode + str(ord(num))
                                    print("data_barcode {0}".format(data_barcode))
                                    EAN = barcode.get_barcode_class('ean13')
                                    ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                    img_name = each_row["Name_Pri"].replace(" ", "_") + "_" + str(ean) + "_lunch.png"
                                    '''EAN = barcode.get_barcode_class('ean13')
                                    ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                    img_name = each_row["Name_Pri"] + "_" + str(ean) + "_lunch"
                                    print("ean {0}".format(ean))
                                    #buffer = BytesIO()
                                    #ean.write(buffer)
                                    filename_map["lunch_" + str(fod_head_count)] = ean.save(f'{settings.MEDIA_ROOT/img_name}')'''

                                    barcode_text  = each_row["Name_Pri"] + '-' + temp + '-10-21-Day1-' + str(ean)
                                    # original image
                                    barcode_image = code128.image(ean, height=100)
                                    # empty image for code and text - it needs margins for text
                                    w, h = barcode_image.size
                                    margin = 20
                                    new_w = w
                                    new_h = h + (2*margin) # margin top and bottom
                                    # empty image with white border and new size
                                    new_image = Image.new('RGB', (new_w, new_h), (255, 255, 255))
                                    # put barcode on new image - with top margin
                                    new_image.paste(barcode_image, (0, margin))
                                    # object to draw text
                                    draw = ImageDraw.Draw(new_image)
                                    # draw text
                                    #fnt = ImageFont.truetype("arial.ttf", 40)
                                    draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                    # save in file
                                    new_image.save(settings.MEDIA_ROOT/img_name, 'PNG')
                                    filename_map["lunch_" + str(fod_head_count)] = settings.MEDIA_ROOT/img_name
                                    filename.append(filename_map)
                                    fod_head_count = fod_head_count - 1
                                    image_file = Image.open(settings.MEDIA_ROOT/img_name) # open colour image
                                    image_file = image_file.convert('L') # convert image to black and white
                                    data = decode(image_file)

                                    ean1 = str(data[0][0]).replace("b'","").replace("'","")
                                    insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service, filename) VALUES ('{0}', 'lunch', '{1}','N', '{2}')".format(id,ean1, img_name)
                                    print("insertq {0}".format(insertq))
                                    cursor.execute(insertq)
                                    connection.commit()
                            elif temp == "Dinner" and (each_row["dinnerv"] == 'N' and each_row["dinnernv"] == 'N' and each_row["dinnerkid"] == 'N'):
                                update_q = "update saikat_rsvp.sp_food_update as t1 inner join saikat_rsvp.sp_rsvp_food as t2 set dinnerv='Y',dinnernv='Y',dinnerkid='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                print(update_q)
                                cursor.execute(update_q)
                                connection.commit()
                                fod_head_count_dinner = each_row["Dinner_veg"]+ each_row["Dinner_nveg"]+ each_row["Dinner_kid"]
                                #fod_head_count_dinner = each_row["Dinner_veg"]+ each_row["Dinner_nveg"]
                                dinner_map = {"veg": each_row["Dinner_veg"],
                                              "nveg": each_row["Dinner_nveg"],
                                              "kid": each_row["Dinner_kid"]
                                              }

                                vcount = dinner_map["veg"]
                                nvcount = dinner_map["nveg"]
                                kcount = dinner_map["kid"]
                                #kcount = 0
                                while fod_head_count_dinner > 0:
                                    data_barcode = ""
                                    value = random.randint(1000000000000, 9999999999999)
                                    print("value = {0}".format(value))
                                    #img_name_d = f'qr_{time.time()}'
                                    #img_name_d = each_row["Name_Pri"] + "_" + img_name_d
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
                                        #img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                        #img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_veg"
                                        img_name_d = each_row["Name_Pri"].replace(" ", "_") + "_" + str(ean) + "_dinner_veg.png"
                                        barcode_text  = each_row["Name_Pri"] + '-' + temp + '-10-21-Day1-' + str(ean)
                                        barcode_image = code128.image(ean, height=100)
                                        # empty image for code and text - it needs margins for text
                                        w, h = barcode_image.size
                                        margin = 20
                                        new_w = w
                                        new_h = h + (2*margin) # margin top and bottom
                                        # empty image with white border and new size
                                        new_image = Image.new('RGB', (new_w, new_h), (255, 255, 255))
                                        # put barcode on new image - with top margin
                                        new_image.paste(barcode_image, (0, margin))
                                        # object to draw text
                                        draw = ImageDraw.Draw(new_image)
                                        # draw text
                                        #fnt = ImageFont.truetype("arial.ttf", 40)
                                        draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                        # save in file
                                        new_image.save(settings.MEDIA_ROOT/img_name, 'PNG')
                                        filename_map["dinner_veg_" + str(vcount)] = settings.MEDIA_ROOT/img_name_d
                                        filename.append(filename_map)

                                        image_file = Image.open(settings.MEDIA_ROOT/img_name) # open colour image
                                        image_file = image_file.convert('L') # convert image to black and white
                                        data = decode(image_file)

                                        ean1 = str(data[0][0]).replace("b'","").replace("'","")

                                        insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service, filename) VALUES ('{0}', 'dinner_veg', '{1}','N', '{2}')".format(id,ean1,img_name_d)
                                        vcount = vcount - 1
                                    elif(nvcount > 0):

                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        print("ean {0}".format(ean))
                                        #img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                        #img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_veg"
                                        img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_nveg.png"
                                        barcode_text  = each_row["Name_Pri"] + '-' + temp + '-10-21-Day1-' + str(ean)
                                        barcode_image = code128.image(ean, height=100)
                                        # empty image for code and text - it needs margins for text
                                        w, h = barcode_image.size
                                        margin = 20
                                        new_w = w
                                        new_h = h + (2*margin) # margin top and bottom
                                        # empty image with white border and new size
                                        new_image = Image.new('RGB', (new_w, new_h), (255, 255, 255))
                                        # put barcode on new image - with top margin
                                        new_image.paste(barcode_image, (0, margin))
                                        # object to draw text
                                        draw = ImageDraw.Draw(new_image)
                                        # draw text
                                        #fnt = ImageFont.truetype("arial.ttf", 40)
                                        draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                        # save in file
                                        new_image.save(settings.MEDIA_ROOT/img_name_d, 'PNG')
                                        filename_map["dinner_nveg_" +str(nvcount)] = settings.MEDIA_ROOT/img_name_d
                                        filename.append(filename_map)

                                        image_file = Image.open(settings.MEDIA_ROOT/img_name_d) # open colour image
                                        image_file = image_file.convert('L') # convert image to black and white
                                        data = decode(image_file)
                                        ean1 = str(data[0][0]).replace("b'","").replace("'","")


                                        insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service,filename) VALUES ('{0}', 'dinner_nveg', '{1}','N', '{2}')".format(id,ean1,img_name_d)
                                        nvcount = nvcount - 1
                                    elif(kcount > 0):
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        print("ean {0}".format(ean))
                                        #img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                        #img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_veg"
                                        img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_kid.png"
                                        barcode_text  = each_row["Name_Pri"] + '-' + temp + '-10-21-Day1-' + str(ean)
                                        barcode_image = code128.image(ean, height=100)
                                        # empty image for code and text - it needs margins for text
                                        w, h = barcode_image.size
                                        margin = 20
                                        new_w = w
                                        new_h = h + (2*margin) # margin top and bottom
                                        # empty image with white border and new size
                                        new_image = Image.new('RGB', (new_w, new_h), (255, 255, 255))
                                        # put barcode on new image - with top margin
                                        new_image.paste(barcode_image, (0, margin))
                                        # object to draw text
                                        draw = ImageDraw.Draw(new_image)
                                        # draw text
                                        #fnt = ImageFont.truetype("arial.ttf", 40)
                                        draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                        # save in file
                                        new_image.save(settings.MEDIA_ROOT/img_name_d, 'PNG')
                                        filename_map["dinner_kid_" +str(kcount)] = settings.MEDIA_ROOT/img_name_d
                                        filename.append(filename_map)

                                        image_file = Image.open(settings.MEDIA_ROOT/img_name_d) # open colour image
                                        image_file = image_file.convert('L') # convert image to black and white
                                        data = decode(image_file)
                                        ean1 = str(data[0][0]).replace("b'","").replace("'","")



                                        insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service,filename) VALUES ('{0}', 'dinner_kid', '{1}','N', '{2}')".format(id,ean1,img_name_d)
                                        kcount = kcount - 1
                                    fod_head_count_dinner = fod_head_count_dinner - 1

                                    print("insertq {0}".format(insertq))
                                    cursor.execute(insertq)
                                    connection.commit()
                return render(request, 'index.html', {'form':form, 'details_info':details_info,'img_name':filename,'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']})

            elif('autogenerate' in request.POST):
                name_info_list = []
                with connection.cursor() as cursor:
                    cursor.execute("select Name_Pri,Email from saikat_rsvp.sp_rsvp_food where Email = 'ghosh.soumen86@gmail.com'")
                    #cursor.execute("select Name_Pri,Email from saikat_rsvp.sp_rsvp_food")
                    res_email_list = dictfectchall(cursor)
                    for each_email in res_email_list:
                        name_info_list.append(each_email["Email"])
                for name_info in name_info_list:
                    #name_info = str(gform.data['name_field'])
                    temp = FOOD_CHOICES[request.POST['food_field']]
                    print("temp_data +++ {0}".format(temp))

                    barcode1 = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)
                    #bar = barcode.get_barcode(name=b_type, code=b_data, writer=ImageWriter())
                    #barcode_file = bar.render() # creates a PIL class image object
                    #print(barcode_file)
                    #out = generate_file(barcode_file) # generate the file
                    #print(out)
                    details_info = []
                    filename = []

                    with connection.cursor() as cursor:
                        cursor.execute("select Name_Pri,Email,Email2,Membership,Lunch_all,Dinner_veg,Dinner_nveg,Dinner_kid,Volunteering,lunch,dinnerv,dinnernv,dinnerkid,t2.id as foodid from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
                        #cursor.execute("select Name_Pri,Email,Lunch_all,Dinner_veg,Dinner_nveg,Dinner_kid,Volunteering,lunch,dinnerv,dinnernv,dinnerkid,t2.id as foodid from saikat_rsvp.rsvp_food as t1 inner join saikat_rsvp.food_update as t2 where t1.id = t2.rsvp_userid and t1.Email = '{0}'".format(name_info))
                        res = dictfectchall(cursor)
                        print("done+++")
                        if res and len(res) > 0:
                            print(filename)
                            for each_row in res:
                                print(each_row["Name_Pri"])
                                details = {}
                                details['name'] = each_row["Name_Pri"]
                                details['email'] = each_row["Email"]
                                details['email2'] = each_row["Email2"]
                                details['membership'] = each_row["Membership"]
                                details['Lunch_all'] = each_row["Lunch_all"]
                                details['Dinner_veg'] = each_row["Dinner_veg"]
                                details['Dinner_nveg'] = each_row["Dinner_nveg"]
                                details['Dinner_kid'] = each_row["Dinner_kid"]
                                details['Volunteering'] = each_row["Volunteering"]
                                details['lunch'] = each_row["lunch"]
                                fod_head_count = each_row["Lunch_all"]
                                id = each_row["foodid"]
                                details_info.append(details)
                                file_list = []
                                if temp == "Lunch" and each_row["lunch"] == 'N':
                                    update_q = "update saikat_rsvp.sp_food_update as t1 inner join saikat_rsvp.sp_rsvp_food as t2 set lunch='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                    print(update_q)
                                    cursor.execute(update_q)
                                    connection.commit()

                                    while fod_head_count > 0:
                                        data_barcode = ""
                                        value = random.randint(1000000000000, 9999999999999)
                                        print("value = {0}".format(value))
                                        #img_name = f'qr_{time.time()}'
                                        #img_name = each_row["Name_Pri"] + "_" + img_name + "_lunch_" + str(fod_head_count)
                                        filename_map = {}
                                        '''for num in b_data:
                                            data_barcode = data_barcode + str(ord(num))'''




                                        data_barcode = data_barcode + str(value) + str(ord(str(fod_head_count)))
                                        for num in temp:
                                            data_barcode = data_barcode + str(ord(num))
                                        print("data_barcode {0}".format(data_barcode))
                                        EAN = barcode.get_barcode_class('ean13')
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        img_name = each_row["Name_Pri"].replace(" ", "_") + "_" + str(ean) + "_lunch.png"
                                        '''EAN = barcode.get_barcode_class('ean13')
                                        ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                        img_name = each_row["Name_Pri"] + "_" + str(ean) + "_lunch"
                                        print("ean {0}".format(ean))
                                        #buffer = BytesIO()
                                        #ean.write(buffer)
                                        filename_map["lunch_" + str(fod_head_count)] = ean.save(f'{settings.MEDIA_ROOT/img_name}')'''

                                        barcode_text  = details['email'].split("$")[0]  + '-' + temp + '-Day1-' + details['membership'].split("(")[0]
                                        # original image
                                        barcode_image = code128.image(ean, height=100)
                                        # empty image for code and text - it needs margins for text
                                        w, h = barcode_image.size
                                        margin = 20
                                        new_w = w
                                        new_h = h + (2*margin) # margin top and bottom
                                        # empty image with white border and new size
                                        new_image = Image.new('RGB', (new_w, new_h), (255, 255, 255))
                                        # put barcode on new image - with top margin
                                        new_image.paste(barcode_image, (0, margin))
                                        # object to draw text
                                        draw = ImageDraw.Draw(new_image)
                                        # draw text
                                        #fnt = ImageFont.truetype("arial.ttf", 40)
                                        draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                        # save in file
                                        new_image.save(settings.MEDIA_ROOT/img_name, 'PNG')
                                        filename_map["lunch_" + str(fod_head_count)] = settings.MEDIA_ROOT/img_name
                                        filename.append(filename_map)
                                        files = os.path.join(settings.MEDIA_ROOT,img_name)
                                        file_list.append(files)
                                        fod_head_count = fod_head_count - 1
                                        image_file = Image.open(settings.MEDIA_ROOT/img_name) # open colour image
                                        image_file = image_file.convert('L') # convert image to black and white
                                        data = decode(image_file)

                                        ean1 = str(data[0][0]).replace("b'","").replace("'","")
                                        insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service, filename) VALUES ('{0}', 'lunch', '{1}','N', '{2}')".format(id,ean1, img_name)
                                        print("insertq {0}".format(insertq))
                                        cursor.execute(insertq)
                                        connection.commit()

                                    send_from = "ghosh.moumita38@gmail.com"
                                    send_to = "secretary@saikat.org"
                                    #send_to = "ghosh.soumen86@gmail.com"
                                    subject = "[Saikat] Sharod Utsav 2023 | Food Coupons | Day 1 Lunch | " + details['membership'].split("(")[0] + " : " + name_info.split("$")[0] + ", " + details['email2']
                                    text = "Dear " + each_row["Name_Pri"]  + "," + "\n" + "We are excited to share the Digital Food Coupons for Durga Puja 2023. These coupons have been provided based on your Membership/Passes purchased and RSVP responses." + "\n" + "\n" \
+ "If you have any questions or concerns regarding the number, type or day of coupons you've received, we kindly ask you to visit our welcome desk during the event, where our team will be happy to assist you." + "\n" + "\n"  \
+ "We are not able honor requests for any changes over emails." + "\n" + "\n"  \
+ "You may forward the email(s) to your family and friends or print them for easier access for seniors. If you prefer physical coupons you can contact the welcome desk during the event to get paper coupons instead." + "\n" + "\n" \
+ "For Annual members and those who have availed “Both Days” or “All 3 Days” passes, you may collect wristbands for cultural event on October 22 from the Welcome desk." + "\n" + "\n"  \
+ "We are eagerly looking forward to providing you with a delightful experience at Durga Puja 2023." + "\n" + "\n" \
+ "Regards,\n" + "Saikat EC"
                                    if len(file_list) > 0:
                                        send_mail(send_from, send_to, subject, text, file_list)
                                        print("send_mail done")
                                    else:
                                        print("file_list len = {0}".format(len(file_list)))
                                elif temp == "Dinner" and (each_row["dinnerv"] == 'N' and each_row["dinnernv"] == 'N' and each_row["dinnerkid"] == 'N'):
                                    update_q = "update saikat_rsvp.sp_food_update as t1 inner join saikat_rsvp.sp_rsvp_food as t2 set dinnerv='Y',dinnernv='Y',dinnerkid='Y' where t2.id = t1.rsvp_userid and t2.Email = '{0}'".format(name_info)
                                    print(update_q)
                                    cursor.execute(update_q)
                                    connection.commit()
                                    fod_head_count_dinner = each_row["Dinner_veg"]+ each_row["Dinner_nveg"]+ each_row["Dinner_kid"]
                                    #fod_head_count_dinner = each_row["Dinner_veg"]+ each_row["Dinner_nveg"]
                                    dinner_map = {"veg": each_row["Dinner_veg"],
                                                  "nveg": each_row["Dinner_nveg"],
                                                  "kid": each_row["Dinner_kid"]
                                                  }

                                    vcount = dinner_map["veg"]
                                    nvcount = dinner_map["nveg"]
                                    kcount = dinner_map["kid"]
                                    #kcount = 0
                                    while fod_head_count_dinner > 0:
                                        data_barcode = ""
                                        value = random.randint(1000000000000, 9999999999999)
                                        print("value = {0}".format(value))
                                        #img_name_d = f'qr_{time.time()}'
                                        #img_name_d = each_row["Name_Pri"] + "_" + img_name_d
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
                                            #img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                            #img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_veg"
                                            img_name_d = each_row["Name_Pri"].replace(" ", "_") + "_" + str(ean) + "_dinner_veg.png"
                                            barcode_text  = details['email'] .split("$")[0] + '-' + temp + 'A' +'-Day1-' + details['membership'].split("(")[0]
                                            barcode_image = code128.image(ean, height=100)
                                            # empty image for code and text - it needs margins for text
                                            w, h = barcode_image.size
                                            margin = 20
                                            new_w = w
                                            new_h = h + (2*margin) # margin top and bottom
                                            # empty image with white border and new size
                                            new_image = Image.new('RGB', (new_w, new_h), (0, 255, 255))
                                            # put barcode on new image - with top margin
                                            new_image.paste(barcode_image, (0, margin))
                                            # object to draw text
                                            draw = ImageDraw.Draw(new_image)
                                            # draw text
                                            #fnt = ImageFont.truetype("arial.ttf", 40)
                                            draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                            # save in file
                                            new_image.save(settings.MEDIA_ROOT/img_name_d, 'PNG')
                                            filename_map["dinner_veg_" + str(vcount)] = settings.MEDIA_ROOT/img_name_d
                                            filename.append(filename_map)
                                            files = os.path.join(settings.MEDIA_ROOT,img_name_d)
                                            file_list.append(files)

                                            image_file = Image.open(settings.MEDIA_ROOT/img_name_d) # open colour image
                                            image_file = image_file.convert('L') # convert image to black and white
                                            data = decode(image_file)

                                            ean1 = str(data[0][0]).replace("b'","").replace("'","")

                                            insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service, filename) VALUES ('{0}', 'dinner_veg', '{1}','N', '{2}')".format(id,ean1,img_name_d)
                                            vcount = vcount - 1
                                            print("insertq {0}".format(insertq))
                                            cursor.execute(insertq)
                                            connection.commit()
                                        elif(nvcount > 0):

                                            ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                            print("ean {0}".format(ean))
                                            #img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                            #img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_veg"
                                            img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_nveg.png"
                                            #barcode_text  = each_row["Name_Pri"] + '-' + temp + '-10-21-Day1-' + str(ean)
                                            barcode_text  = details['email'].split("$")[0]  + '-' + temp + 'A' +'-Day1-' + details['membership'].split("(")[0]
                                            barcode_image = code128.image(ean, height=100)
                                            # empty image for code and text - it needs margins for text
                                            w, h = barcode_image.size
                                            margin = 20
                                            new_w = w
                                            new_h = h + (2*margin) # margin top and bottom
                                            # empty image with white border and new size
                                            new_image = Image.new('RGB', (new_w, new_h), (0, 255, 255))
                                            # put barcode on new image - with top margin
                                            new_image.paste(barcode_image, (0, margin))
                                            # object to draw text
                                            draw = ImageDraw.Draw(new_image)
                                            # draw text
                                            #fnt = ImageFont.truetype("arial.ttf", 40)
                                            draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                            # save in file
                                            new_image.save(settings.MEDIA_ROOT/img_name_d, 'PNG')
                                            filename_map["dinner_nveg_" +str(nvcount)] = settings.MEDIA_ROOT/img_name_d
                                            filename.append(filename_map)
                                            files = os.path.join(settings.MEDIA_ROOT,img_name_d)
                                            file_list.append(files)

                                            image_file = Image.open(settings.MEDIA_ROOT/img_name_d) # open colour image
                                            image_file = image_file.convert('L') # convert image to black and white
                                            data = decode(image_file)
                                            ean1 = str(data[0][0]).replace("b'","").replace("'","")


                                            insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service,filename) VALUES ('{0}', 'dinner_nveg', '{1}','N', '{2}')".format(id,ean1,img_name_d)
                                            nvcount = nvcount - 1
                                            print("insertq {0}".format(insertq))
                                            cursor.execute(insertq)
                                            connection.commit()
                                        elif(kcount > 0):
                                            ean = EAN(f'{int(str(data_barcode))}', writer=ImageWriter())
                                            print("ean {0}".format(ean))
                                            #img_name_d = img_name_d + '_dinner_veg_' + str(vcount)
                                            #img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_veg"
                                            img_name_d = each_row["Name_Pri"] + "_" + str(ean) + "_dinner_kid.png"
                                            barcode_text  = details['email'].split("$")[0]  + '-' + temp + 'K' +'-Day1-' + details['membership'].split("(")[0]
                                            barcode_image = code128.image(ean, height=100)
                                            # empty image for code and text - it needs margins for text
                                            w, h = barcode_image.size
                                            margin = 20
                                            new_w = w
                                            new_h = h + (2*margin) # margin top and bottom
                                            # empty image with white border and new size
                                            new_image = Image.new('RGB', (new_w, new_h), (255, 255, 0))
                                            # put barcode on new image - with top margin
                                            new_image.paste(barcode_image, (0, margin))
                                            # object to draw text
                                            draw = ImageDraw.Draw(new_image)
                                            # draw text
                                            #fnt = ImageFont.truetype("arial.ttf", 40)
                                            draw.text( (10, new_h-10), barcode_text, fill=(0, 0, 0))#, font=fnt)  #
                                            # save in file
                                            new_image.save(settings.MEDIA_ROOT/img_name_d, 'PNG')
                                            filename_map["dinner_kid_" +str(kcount)] = settings.MEDIA_ROOT/img_name_d
                                            filename.append(filename_map)
                                            files = os.path.join(settings.MEDIA_ROOT,img_name_d)
                                            file_list.append(files)

                                            image_file = Image.open(settings.MEDIA_ROOT/img_name_d) # open colour image
                                            image_file = image_file.convert('L') # convert image to black and white
                                            data = decode(image_file)
                                            ean1 = str(data[0][0]).replace("b'","").replace("'","")



                                            insertq = "INSERT INTO saikat_rsvp.sp_barcode_scan (food_update_id, food_type, barcode_num,food_service,filename) VALUES ('{0}', 'dinner_kid', '{1}','N', '{2}')".format(id,ean1,img_name_d)
                                            print("insertq {0}".format(insertq))
                                            cursor.execute(insertq)
                                            connection.commit()
                                            kcount = kcount - 1
                                        fod_head_count_dinner = fod_head_count_dinner - 1


                                    send_from = "ghosh.moumita38@gmail.com"
                                    send_to = "secretary@saikat.org"
                                    #send_to = "ghosh.soumen86@gmail.com"
                                    subject = "[Saikat] Sharod Utsav 2023 | Food Coupons | Day 1 Dinner | " + details['membership'].split("(")[0] + " : " + name_info.split("$")[0] + ", " + details['email2']
                                    text = "Dear " + each_row["Name_Pri"]  + "," + "\n" + "We are excited to share the Digital Food Coupons for Durga Puja 2023. These coupons have been provided based on your Membership/Passes purchased and RSVP responses." + "\n" + "\n" \
+ "If you have any questions or concerns regarding the number, type or day of coupons you've received, we kindly ask you to visit our welcome desk during the event, where our team will be happy to assist you." + "\n" + "\n"  \
+ "We are not able honor requests for any changes over emails." + "\n" + "\n"  \
+ "You may forward the email(s) to your family and friends or print them for easier access for seniors. If you prefer physical coupons you can contact the welcome desk during the event to get paper coupons instead." + "\n" + "\n" \
+ "For Annual members and those who have availed “Both Days” or “All 3 Days” passes, you may collect wristbands for cultural event on October 22 from the Welcome desk." + "\n" + "\n"  \
+ "We are eagerly looking forward to providing you with a delightful experience at Durga Puja 2023." + "\n" + "\n" \
+ "Regards,\n" + "Saikat EC"
                                    if len(file_list) > 0:
                                        send_mail(send_from, send_to, subject, text, file_list)
                                        time.sleep(5)
                                        print("send_mail done")
                                    else:
                                        print("Dinner file_list len = {0}".format(len(file_list)))
                                elif temp == "Lunch" and each_row["lunch"] == 'Y':
                                    nameimg = 'lunch.jpg'
                                    filename_map = {}
                                    filename_map["idata"] = settings.MEDIA_ROOT/nameimg
                                    filename.append(filename_map)

                return render(request, 'index.html', {'form':form, 'details_info':details_info,'img_name':filename,'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']})

            #return render(request, 'index.html', {'img_name': filename,'form':form})
    else:
        with connection.cursor() as cursor:
            cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid ")
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
     select_q = "select * from saikat_rsvp.sp_rsvp_food"
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
                    cursor.execute("select * from saikat_rsvp.sp_food_update as t1 inner join saikat_rsvp.sp_barcode_scan as t2 where t1.id = t2.food_update_id and t2.food_type = '{0}'".format(temp))
                    res = dictfectchall(cursor)
                    print("done")
                    for each_row in res:
                        details = {}
                        cursor.execute("select * from saikat_rsvp.sp_rsvp_food as t1 inner join saikat_rsvp.sp_food_update as t2 where t1.id = t2.rsvp_userid and t2.id = '{0}'".format(each_row['food_update_id']))
                        res1 = dictfectchall(cursor)
                        if (temp == "Lunch"):
                            details['coupon'] = each_row["lunch"]
                        if (temp == "Dinner_veg"):
                            details['coupon'] = each_row["dinnerv"]
                        if (temp == "Dinner_nveg"):
                            details['coupon'] = each_row["dinnernv"]
                        if (temp == "Dinner_kid"):
                            details['coupon'] = each_row["dinnerkid"]
                        details['name'] = res1[0]["Name_Pri"]
                        details['email'] = res1[0]["Email"]
                        details['food_type'] = temp
                        details['barcode_num'] = each_row["barcode_num"]
                        details['food_update_id'] = each_row['food_update_id']
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
                if(temp == 'Dinner_nveg'):
                    coupon_not_given =  dinner_nveg_count - coupon_given
                if(temp == 'Dinner_kid'):
                    coupon_not_given =  dinner_kid_count - coupon_given
                return render(request, 'dashboard.html', {'form':form, 'details_info':details_info,'lunch_count':lunch_count,'dinner_veg_count':dinner_veg_count,'dinner_nveg_count':dinner_nveg_count,'dinner_kid_count':dinner_kid_count,
                                                          'food_type':temp,'coupon_not_given':coupon_not_given,'coupon_given':coupon_given,'food_serviced':food_serviced,'food_not_serviced':food_not_serviced})
            else:
                return render(request, 'dashboard.html',{'form':form})
     return render(request, 'dashboard.html',{'form':form, 'lunch_count':lunch_count,'dinner_veg_count':dinner_veg_count,'dinner_nveg_count':dinner_nveg_count,'dinner_kid_count':dinner_kid_count})

def member(request):
     context = {}
     global gform
     form = DataForm(request.POST)
     gform = form
     details_info = []
     if request.method == 'POST':
            if 'search' in request.POST:
                print("hello dashboard {0}".format(request.POST['name1_field']))
                select_q = "select * from saikat_rsvp.sp_rsvp_food where Name_Pri like '%{0}%'".format(request.POST['name1_field'])
                print(select_q)
                with connection.cursor() as cursor:
                     cursor.execute(select_q)

                     res_sel = dictfectchall(cursor)
                     print("length {0}".format(len(res_sel)))
                     for each_row in res_sel:
                        details = {}
                        details['ID'] = each_row['ID']
                        details['name'] = each_row["Name_Pri"]
                        details['email'] = each_row["Email"]
                        details['Lunch_all'] = each_row["Lunch_all"]
                        details['Dinner_veg'] = each_row['Dinner_veg']
                        details['Dinner_nveg'] = each_row['Dinner_nveg']
                        details['Dinner_kid'] = each_row['Dinner_kid']
                        details_info.append(details)
                return render(request, 'member.html', {'form':form, 'details_info':details_info});

     return render(request, 'member.html',{'form':form})
