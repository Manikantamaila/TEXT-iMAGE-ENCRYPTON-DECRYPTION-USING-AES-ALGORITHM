from flask import Flask, request, render_template,session, flash
import mysql.connector
import pandas as pd
import random
# from random import *
import secrets
from flask_mail import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


app=Flask(__name__)
app.secret_key='Lakshmi'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/owner")
def owner():
    return render_template("owner.html")

@app.route("/ownerhome")
def ownerhome():
    return render_template("ownerhome.html")

@app.route('/regback',methods=['POST','GET'])
def regback():
    if request.method=='POST':
        # print("gekjhiuth")
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        pno=request.form['pno']
        print(addr)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image"
        )
        mycursor = mydb.cursor()

        sql="select * from owner"
        result=pd.read_sql_query(sql,mydb)
        email1=result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","success")
            return render_template('owner.html')
        if(pwd==cpwd):
            sql = "INSERT INTO owner (name,email,pwd,addr,pno) VALUES (%s,%s,%s,%s,%s)"
            val = (name,email,pwd,addr,pno)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered","warning")
            return render_template('ownerlogin.html')
        else:
            flash("Password and Confirm Password not same")
    return render_template('owner.html')

@app.route("/ownerlogin")
def ownerlogin():
    return render_template("ownerlogin.html")


@app.route('/loginback',methods=['POST', 'GET'])
def loginback():
    if request.method == "POST":

        email = request.form['email']

        password1 = request.form['pwd']
        print('p')
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="test_image")
        cursor = mydb.cursor()

        sql = "select * from owner where email='%s' and pwd='%s' " % (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        global name
        # name = results[0][1]
        # print(name)
        # session['fname'] = results[0][1]
        session['email'] = email
        # session['r']=r

        if len(results) > 0:

                # session['user'] = username
                # session['id'] = results[0][0]
                # print(id)
                # print(session['id'])
            flash("Welcome ", "primary")
            return render_template('ownerhome.html', msg=results[0][1])
        else:
            return render_template('ownerlogin.html', msg="invalid value")

    return render_template('ownerlogin.html')

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/upimg")
def upimg():
    return render_template("upimg.html")


@app.route("/upimgback",methods=["POST","GET"])
def upimgback():
    if request.method=="POST":
        imgname = request.form['imgname']
        file = request.form['file']
        mypath = os.path.join("img_files/" + file)
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="test_image"
            )
            mycursor = mydb.cursor()
            from datetime import datetime
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            # print(t)
            email = session.get('email')
            empPicture = convertToBinaryData(mypath)

            data="This is a collection of both secure hash functions (such as SHA256 and RIPEMD160), and various encryption algorithms " \
                 "(AES, DES, RSA, ElGamal, etc.). The package is structured to make adding new modules easy. This section is essentially" \
                 " complete, and the software interface will almost certainly not change in an incompatible way in the future; all that " \
                 "remains to be done is to fix any bugs that show up. If you encounter a bug, please report it in the Launchpad bug"
            insert_blob_tuple = (imgname, empPicture, now, email,data)
            sql_insert_blob_query = "INSERT INTO img_files(imgname,file,date,email,image) VALUES(%s,%s,%s,%s,AES_ENCRYPT(%s,'lakshmi'))"
            print(insert_blob_tuple)
            result = mycursor.execute(sql_insert_blob_query, insert_blob_tuple)
            print("Image and file inserted successfully as a BLOB into python_employee table", result)
            mydb.commit()
        except mysql.connector.Error as error:
            print("Failed inserting BLOB data into MySQL table {}".format(error))
        flash("file uploaded successfully", "success")
        return render_template('upload.html')
        flash("Something wrong", "danger")
        return render_template("upimg.html")
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

@app.route("/upfile")
def upfile():
    return render_template("upfile.html")

@app.route('/upfileback',methods=['POST','GET'])
def upfileback():
    print("gekjhiuth")
    if request.method=='POST':
        print("gekjhiuth")
        fname=request.form['fname']
        # prm=request.form['prm']
        # sname=request.form['sname']
        file=request.form['file']
        dd="text_files/"+file
        f = open(dd, "r")
        data = f.read()

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image"
        )
        mycursor = mydb.cursor()

        from datetime import datetime
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        currentDay = datetime.now().strftime('%d/%m/%Y')
        status = 'Request'
        print(t)
        email = session.get('email')
        sql = "INSERT INTO upload_files (fname,files,date,email) VALUES (%s,AES_ENCRYPT(%s,'lakshmi'),%s,%s)"

        val = (fname, data, now, email)
        mycursor.execute(sql, val)
        mydb.commit()
        flash("file uploaded successfully", "success")
        return render_template('upload.html')
    flash("Something wrong", "danger")
    return render_template('upload.html')

@app.route("/viewfiles")
def viewfiles():
    hists = ['IMAGE FILES', 'TEXT FILES']
    return render_template("viewfiles.html", hists=hists)

@app.route("/vtf")
def vtf():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from upload_files where email='%s'" %(session['email'])
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    # x = x.drop(['file'], axis=1)
    x = x.drop(['id'], axis=1)
    x = x.drop(['email'], axis=1)
    # x = x.drop(['file_name'], axis=1)

    return render_template("vtf.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/vif")
def vif():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from img_files where email='%s'" %(session['email'])
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    # x = x.drop(['image'], axis=1)
    x = x.drop(['id'], axis=1)
    x = x.drop(['email'], axis=1)
    x = x.drop(['file'], axis=1)

    return render_template("vif.html", col_name=x.columns.values, row_val=x.values.tolist())


@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/reguser',methods=['POST','GET'])
def reguser():
    if request.method=='POST':
        print("gekjhiuth")
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        pno=request.form['pno']
        print(addr)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image"
        )
        mycursor = mydb.cursor()

        sql="select * from owner"
        result=pd.read_sql_query(sql,mydb)
        email1=result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","success")
            return render_template('owner.html')
        if(pwd==cpwd):
            sql = "INSERT INTO user (name,email,pwd,addr,pno) VALUES (%s,%s,%s,%s,%s)"
            val = (name,email,pwd,addr,pno)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered","warning")
            return render_template('userlog.html')
        else:
            flash("Password and Confirm Password not same")
    return render_template('user.html')


@app.route('/userback',methods=['POST', 'GET'])
def userback():
    if request.method == "POST":

        email = request.form['email']

        password1 = request.form['pwd']
        print('p')
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="test_image")
        cursor = mydb.cursor()

        sql = "select * from user where email='%s' and pwd='%s' " % (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        global name
        # name = results[0][1]
        # print(name)
        # session['fname'] = results[0][1]
        session['email'] = email
        # session['r']=r

        if len(results) > 0:

                # session['user'] = username
                # session['id'] = results[0][0]
                # print(id)
                # print(session['id'])
            flash("Welcome ", "primary")
            return render_template('userhome.html', msg=results[0][1])
        else:
            return render_template('userlog.html', msg="invalid value")

    return render_template('userlog.html')


@app.route("/userhome")
def userhome():
    return render_template("userhome.html")

@app.route("/userlog")
def userlog():
    return render_template("userlog.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search1")
def search1():
    return render_template("search1.html")

@app.route("/search1back",methods=['POST','GET'])
def search1back():
    print("dfhlksokhso")
    if request.method == 'POST':
        print("gekjhiuth")
        #fname = request.form['fname']
        fname = request.form['fname']

        print("Reading BLOB data from python_employee table")
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image",
            charset='utf8'
        )
        mycursor = mydb.cursor()

        sql = "select * from upload_files where fname LIke '%"+fname+"%' "
        x = pd.read_sql_query(sql, mydb)
        print("^^^^^^^^^^^^^")
        print(type(x))
        print(x)
        # x = x.drop(['file'], axis=1)
        x = x.drop(['email'], axis=1)
        x = x.drop(['date'], axis=1)
        # x = x.drop(['file'], axis=1)

        # x["View Data"] = " "
        # x["Send Request"] = ""

        return render_template("search1back.html", col_name=x.columns.values, row_val=x.values.tolist())
    return render_template("searchback.html")


@app.route('/req/<s1>/<s2>')
def req(s1=0,s2=''):
    print("gekjhiuth")



    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image"
        )
    mycursor = mydb.cursor()


    # status = 'Request'
    email = session.get('email')
    sql = "INSERT INTO request_text (fid,fname,email) VALUES (%s,%s,%s)"

    val = (s1, s2, email)
    mycursor.execute(sql, val)
    mydb.commit()
    flash("Request sended to Cloud Server", "success")
    return render_template('reg.html')

@app.route("/search2")
def search2():
    return render_template("search2.html")

@app.route("/search2back",methods=['POST','GET'])
def search2back():
    print("dfhlksokhso")
    if request.method == 'POST':
        print("gekjhiuth")
        #fname = request.form['fname']
        imgname = request.form['imgname']

        print("Reading BLOB data from python_employee table")
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image",
            charset='utf8'
        )
        mycursor = mydb.cursor()

        sql = "select * from img_files where imgname LIke '%"+imgname+"%' "
        x = pd.read_sql_query(sql, mydb)
        print("^^^^^^^^^^^^^")
        print(type(x))
        print(x)
        x = x.drop(['image'], axis=1)
        x = x.drop(['email'], axis=1)
        x = x.drop(['date'], axis=1)
        x = x.drop(['file'], axis=1)

        # x["View Data"] = " "
        # x["Send Request"] = ""

        return render_template("search2back.html", col_name=x.columns.values, row_val=x.values.tolist())
    return render_template("searchback.html")

@app.route('/req1/<s1>/<s2>')
def req1(s1=0,s2=''):
    print("gekjhiuth")



    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image"
        )
    mycursor = mydb.cursor()


    # status = 'Request'
    email = session.get('email')
    sql = "INSERT INTO request_img(fid,imgname,email) VALUES (%s,%s,%s)"

    val = (s1, s2, email)
    mycursor.execute(sql, val)
    mydb.commit()
    flash("Request sended to Cloud Server", "success")
    return render_template('req1.html')

# @app.route('/req2/<s1>/<s2>')
# def req2(s1=0,s2=''):
#     print("gekjhiuth")
#
#
#
#     mydb = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             passwd="",
#             database="test_image"
#         )
#     mycursor = mydb.cursor()
#
#
#     # status = 'Request'
#     email = session.get('email')
#     sql = "INSERT INTO request_img(fid,fname,email) VALUES (%s,%s,%s)"
#
#     val = (s1, s2, email)
#     mycursor.execute(sql, val)
#     mydb.commit()
#     flash("Request sended to Cloud Server", "success")
#     return render_template('req2.html')
#
#

@app.route("/cloud")
def cloud():
    return render_template("cloud.html")

@app.route('/cloudback',methods=['POST', 'GET'])
def cloudback():
    print("aaaaaaaaaaaaaaa")
    if request.method == 'POST':
        print("aaaaaaaaaaaaaaa")


        username = request.form['email']
        password1 = request.form['pwd']
        if username == 'cloud@gmail.com' and password1 == 'cloud' :
            flash("Sucessfully Login to the Page", "primary")
            return render_template('cloudhome.html')
        else:
            flash("Invali Email / Password", "primary")

            return render_template('cloud.html')

    return render_template('cloud.html')

@app.route("/cloudhome")
def cloudhome():
    return render_template("cloudhome.html")

@app.route("/vowners")
def vowners():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from owner "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['pwd'], axis=1)
    # x = x.drop(['id'], axis=1)
    # x = x.drop(['pno'], axis=1)

    return render_template("vowners.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/vreq")
def vreq():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from request_text where status ='Accepted' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['action'], axis=1)
    x = x.drop(['id'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['pkey'], axis=1)

    sql1 = "select * from request_img where status ='Accepted' "
    y = pd.read_sql_query(sql1, mydb)
    print("^^^^^^^^^^^^^")
    print(type(y))
    print(y)
    # x = x.drop(['pwd'], axis=1)
    y = y.drop(['id'], axis=1)
    y = y.drop(['status'], axis=1)
    y = y.drop(['action'], axis=1)
    y = y.drop(['pkey'], axis=1)


    return render_template("vreq.html", col_name=x.columns.values, row_val=x.values.tolist(), col=y.columns.values, row=y.values.tolist())

@app.route("/kgc")
def kgc():
    return render_template("kgc.html")

@app.route('/kgcback',methods=['POST', 'GET'])
def kgcback():
    print("aaaaaaaaaaaaaaa")
    if request.method == 'POST':
        print("aaaaaaaaaaaaaaa")


        username = request.form['email']
        password1 = request.form['pwd']
        if username == 'kgc@gmail.com' and password1 == 'kgc' :
            flash("Sucessfully Login to the Page", "primary")
            return render_template('kgchome.html')
        else:
            flash("Invali Email / Password", "primary")

            return render_template('kgc.html')

    return render_template('kgc.html')

@app.route("/kgchome")
def kgchome():
    return render_template("kgchome.html")

@app.route("/vusers")
def vusers():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from user "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['pwd'], axis=1)
    x = x.drop(['id'], axis=1)
    # x = x.drop(['pno'], axis=1)

    return render_template("vusers.html", col_name=x.columns.values, row_val=x.values.tolist())


@app.route("/vdf")
def vdf():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from upload_files  "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    # x = x.drop(['pwd'], axis=1)
    x = x.drop(['files'], axis=1)
    # x = x.drop(['status'], axis=1)

    sql1 = "select * from img_files "
    y = pd.read_sql_query(sql1, mydb)
    print("^^^^^^^^^^^^^")
    print(type(y))
    print(y)
    # x = x.drop(['ima/e'], axis=1)
    y = y.drop(['file'], axis=1)
    y = y.drop(['image'], axis=1)


    return render_template("vdf.html", col_name=x.columns.values, row_val=x.values.tolist(), col=y.columns.values, row=y.values.tolist())

@app.route("/vur")
def vur():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()

    sql = "select * from request_text where status ='pending' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    x = x.drop(['action'], axis=1)
    x = x.drop(['fid'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['pkey'], axis=1)

    sql1 = "select * from request_img where status ='pending' "
    y = pd.read_sql_query(sql1, mydb)
    print("^^^^^^^^^^^^^")
    print(type(y))
    print(y)
    y = y.drop(['action'], axis=1)
    y = y.drop(['fid'], axis=1)
    y = y.drop(['status'], axis=1)
    y = y.drop(['pkey'], axis=1)


    return render_template("vur.html", col_name=x.columns.values, row_val=x.values.tolist(), col=y.columns.values, row=y.values.tolist())

@app.route('/accept/<s1>')
def accept(s1=0):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    status='Accepted'

    sql = "update request_text set status='%s' where id='%s' "%(status,s1)
    mycursor.execute(sql)
    mydb.commit()
    flash("Request Accepted and Send Information To KGC","primary")
    return render_template("accept.html")
@app.route('/accept1/<s1>')
def accept1(s1=0):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    status='Accepted'
    sql = "update request_img set status='%s' where id='%s' "%(status,s1)
    mycursor.execute(sql)
    mydb.commit()
    flash("Request Accepted and Send Information To KGC","primary")
    return render_template("accept1.html")


@app.route("/vreq1/<s1>/<s2>")
def vreq1(s1=0, s2=''):
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    global n,m,f
    n=s1
    email=s2
    otp1 = random.randint(000000, 999999)
    # skey = secrets.token_hex(4)
    # print(skey)
    otp="Your secret key is:"
    mail_content = otp + ' ' + str(otp1)
    sender_address = 'cse.takeoff@gmail.com'
    sender_pass = 'Takeoff@123'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Text and Image Encryption Decryption using AES Algorithm'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    action="Completed"

    sql = "update request_text set pkey='%s',action='%s' where id='%s' "%(otp1,action,n)
    mycursor.execute(sql)
    mydb.commit()
    flash("Send key to user through Mail ", "success")
    return render_template("vreq1.html")

@app.route("/vreq2/<s1>/<s2>")
def vreq2(s1=0, s2=''):
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    global n,m,f
    n=s1
    email=s2
    otp1 = random.randint(000000, 999999)
    # skey = secrets.token_hex(4)
    # print(skey)
    otp="Your secret key is:"
    mail_content = otp + ' ' + str(otp1)
    sender_address = 'cse.takeoff@gmail.com'
    sender_pass = 'Takeoff@123'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Text and Image Encryption Decryption using AES Algorithm'

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    action="Completed"
    sql = "update request_img set pkey='%s', action='%s' where id='%s' "%(otp1,action,n)
    mycursor.execute(sql)
    mydb.commit()
    flash("Send key to User  through Mail", "success")
    return render_template("vreq2.html")


@app.route("/down")
def down():
    print("Reading BLOB data from python_employee table")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test_image",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    email = session.get('email')

    sql = "select * from request_text where action ='Completed' and email='"+email+"' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    #mycursor.execute(sql, (id,))
    #record = mycursor.fetchall()
    x = pd.read_sql_query(sql, mydb)
    print("^^^^^^^^^^^^^")
    print(type(x))
    print(x)
    # x = x.drop(['pwd'], axis=1)
    # x = x.drop(['fid'], axis=1)
    x = x.drop(['status'], axis=1)
    x = x.drop(['action'], axis=1)
    x = x.drop(['pkey'], axis=1)
    x = x.drop(['email'], axis=1)


    sql1 = "select * from request_img where email='"+email+"' and action='Completed'"
    y = pd.read_sql_query(sql1, mydb)
    print("^^^^^^^^^^^^^")
    print(type(y))
    print(y)
    # x = x.drop(['pwd'], axis=1)
    # y = y.drop(['fid'], axis=1)
    y = y.drop(['status'], axis=1)
    y = y.drop(['action'], axis=1)
    y = y.drop(['pkey'], axis=1)
    y = y.drop(['email'], axis=1)


    return render_template("down.html",col_name=x.columns.values, row_val=x.values.tolist(), col=y.columns.values, row=y.values.tolist())

@app.route("/down1/<s1>/<s2>")
def down1(s1=0,s2=''):
    global g,f1
    g=s1
    f1=s2
    return render_template("down1.html",g=g,f1=f1)

@app.route("/down1back",methods=['POST','GET'])
def down1back():
    print("dfhlksokhso")
    if request.method == 'POST':
        print("gekjhiuth")
        pkey = request.form['pkey']
        id = request.form['id']
        fid = request.form['fid']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test_image",
            charset='utf8'
        )
        print(fid)

        mycursor = mydb.cursor()

        sql = "select count(*),aes_decrypt(files,'lakshmi') from upload_files,request_text where request_text.fid='"+fid+"' and upload_files.id='"+fid+"' and request_text.pkey='"+pkey+"'"
        x = pd.read_sql_query(sql, mydb)
        count=x.values[0][0]
        print(count)
        asss=x.values[0][1]
        # asss=asss.decode('utf-8')

        print("^^^^^^^^^^^^^")
        if count==0:
            flash("Enter Valid Key","danger")
            return render_template("down1.html")
        if count==1:
            return render_template("downfile.html", msg=asss)

        return render_template("down.html")

@app.route("/down2/<s1>/<s2>")
def down2(s1=0,s2=''):
    global g,f1
    g=s1
    f1=s2
    return render_template("down2.html",g=g,f1=f1)


@app.route("/down2back",methods=['POST','GET'])
def down2back():
    print("dfhlksokhso")
    if request.method == 'POST':
        print("gekjhiuth")
        pkey = request.form['pkey']
        id = request.form['id']
        fid = request.form['fid']
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="test_image",
                charset='utf8'
            )
            mycursor = mydb.cursor()
            sql_fetch_blob_query = "SELECT file from img_files,request_img where request_img.fid='"+fid+"' and img_files.id='"+fid+"' and request_img.pkey='"+pkey+"'"
            # val = (s1)
            print("ababababababa")
            print(sql_fetch_blob_query)
            # print(s1)
            mycursor.execute(sql_fetch_blob_query)
            record = mycursor.fetchall()
            image = record[0][0]
            # print(image)
            # print(len(image))
            # print(type(image))
            with open("static/abc.jpg", "wb") as img:
                img.write(image)
            # print(image)
        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))

        finally:
            if(mydb.is_connected()):
                mycursor.close()
                mydb.close()
                print("MySQL connection is closed")

    return render_template("viewimmg.html", img="/static/abc.jpg")

if __name__=='__main__':
    app.run(debug=True)

# SQL="SELECT file, AES_DECRYPT(file,'lakshmi') FROM upload_files"