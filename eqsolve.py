from flask import Flask, request, jsonify,session, g, redirect, url_for, abort, \
     render_template, flash
import requests
import json
import re
import cmath
import sqlite3
import os

app = Flask(__name__)

def solveQuad(eq1):

    lhseq1 = eq1.split("=")[0]
    print(lhseq1)
    rhseq1 = eq1.split("=")[1]

    rhsset = set()


    a = re.findall("[\-]?[0-9]*x[2"+u'\u00B2'+"]",lhseq1)
    if(not a):
        a = re.findall("[\-]?[0-9]*x",rhseq1)
        rhsset.add('x2')

    b = re.findall("[\-]?[0-9]*x(?:[^2"+u'\u00B2'+"]|$)",lhseq1)
    if(not b):
        b = re.findall("[\-]?[0-9]*x(?:[^2"+u'\u00B2'+"]|$)",rhseq1)
        rhsset.add('x')

    c = re.findall("(?:^|[^x])[\-]?[0-9]+(?:[^x]|$)",lhseq1)
    if(not c):
        c = re.findall("(?:^|[^x])[\-]?[0-9]+(?:[^x]|$)",rhseq1)
        rhsset.add('1')


    if(a[0] == 'x'+u'\u00B2' or a[0] == 'x2'):
        a = 1
    else:
        a = int(a[0][:-2])
    if('x2' in rhsset):
        a = a*-1

    print(b)

    if(b[0] == 'x'):
        b = 1
    elif(b[0][-1] == 'x'):
        b = int(b[0][:-1])
    else:
        b = int(b[0][:-2])
    if('x' in rhsset):
        b = b*-1
    
    if(not c):
        c = 0
    elif(c[0][-1] <= '9' and c[0][-1] >= '0' ):
        c = int(c[0])
    else:
        c = int(c[0][:-1])
    if('1' in rhsset):
        c = c*-1
    
    print(a,b,c)

    d = (b**2) - (4*a*c)

    # find two solutions
    sol1 = str((-b-cmath.sqrt(d))/(2*a))
    sol2 = str((-b+cmath.sqrt(d))/(2*a))

    return((sol1,sol2))

def solveSimul(eq1, eq2):
    
    lhseq1 = eq1.split("=")[0]
    print(lhseq1)
    rhseq1 = eq1.split("=")[1]

    lhseq2 = eq2.split("=")[0]
    print(lhseq2)
    rhseq2 = eq2.split("=")[1]

    rhsset = set()


    x1 = re.findall("[\-]?[0-9]*x",lhseq1)
    if(not x1):
        x1 = re.findall("[\-]?[0-9]*x",rhseq1)
        rhsset.add('x1')
    if(x1[0] == 'x'):
        x1[0] = '1x'
        
        
    x2 = re.findall("[\-]?[0-9]*x",lhseq2)
    if(not x2):
        x2 = re.findall("[\-]?[0-9]*x",rhseq2)
        rhsset.add('x2')
    if(x2[0] == 'x'):
        x2[0] = '1x'

    y1 = re.findall("[\-]?[0-9]*y",lhseq1)
    if(not y1):
        y1 = re.findall("[\-]?[0-9]*y",rhseq1)
        rhsset.add('y1')
    if(y1[0] == 'y'):
        y1[0] = '1y'

    y2 = re.findall("[\-]?[0-9]*y",lhseq2)
    if(not y2):
        y2 = re.findall("[\-]?[0-9]*y",rhseq2)
        rhsset.add('y2')
    if(y2[0] == 'y'):
        y2[0] = '1y'

    d1 = re.findall("[\-]?[0-9]+[^a-z]?$",lhseq1)
    if(not d1):
        d1 = re.findall("[\-]?[0-9]+[^a-z]?$",rhseq1)
        rhsset.add('d1')
    if(not d1):
        d1[0] = 0

    d2 = re.findall("[\-]?[0-9]+(?:[^a-z]|$)",lhseq2)
    if(not d2):
        d2 = re.findall("[\-]?[0-9]+(?:[^a-z]|$)",rhseq2)
        rhsset.add('d2')
    if(not d2):
        x1[0] = 1

    print(rhsset)


    print("x1:",x1,"y1:",y1,"x2:",x2,"y2:",y2, "d1:",d1,"d2:",d2)

    e1 = []
    e2 = []

    
    e1.append(int(x1[0][:-1]))
    if('x1' in rhsset):    
        e1[-1] *= -1
    e1.append(int(y1[0][:-1]))
    if('y1' in rhsset):    
        e1[-1] *= -1
    e1.append(int(d1[0][:]))
    if('d1' in rhsset):    
        e1[-1] *= -1

    e2.append(int(x2[0][:-1]))
    if('x2' in rhsset):    
        e2[-1] *= -1
    e2.append(int(y2[0][:-1]))
    if('y2' in rhsset):    
        e2[-1] *= -1
    e2.append(int(d2[0][:]))
    if('d2' in rhsset):    
        e2[-1] *= -1

    e1[-1] *= -1
    e2[-1] *= -1

    m1 = e1[0]/e1[1]
    m2 = e2[0]/e2[1]
    c1 = e1[2]/e1[1]
    c2 = e2[2]/e2[1]

    print(m1,m2,c1,c2)
    
    

    print(e1,e2)

    if(e2[1] == 0):
        print("error")

    mf = e1[1]/e2[1]

    e1[0] = e1[0] - (mf*e2[0])
    e1[2] = e1[2] - (mf*e2[2])
    e1[1] = e1[1] - (mf*e2[1])

    if(e1[0] == 0):
        print("error")

    mf = e2[0]/e1[0]

    e2[1] = e2[1] - (mf*e1[1])
    e2[2] = e2[2] - (mf*e1[2])
    e2[0] = e2[0] - (mf*e1[0])

    x = e1[2]/e1[0]
    y = e2[2]/e2[1]

   


    print(x,y)
    return((x,y,m1,m2,c1,c2))


@app.route("/")
def index():
    return(render_template("login.html"))

@app.route("/signup", methods =['POST','GET'])
def signup():
    email = request.form.get("email","").lower()
    passwd = request.form.get("pass","").lower()
    conn = sqlite3.connect('equation.db')
    conn.execute("INSERT INTO LOGIN VALUES('"+email+"','"+passwd+"');")
    conn.commit()
    conn.close()
    return jsonify(signup = "Successful", email = email)


@app.route("/login", methods =['POST','GET'])
def login():
    email = request.form.get("email","").lower()
    passwd = request.form.get("pass","").lower()
    print(email,passwd)
    conn = sqlite3.connect('equation.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM LOGIN WHERE email='"+email+"';")
    rows = cur.fetchall(); 

    for row in rows:
        print(type(row[1]), type(passwd))
        if(str(row[1]) == str(passwd)):
            print("CHECK")
            return jsonify(login = "Successful", email=email)
    conn.close()
    return jsonify(login = "Unsuccessful",)


    
@app.route("/checkUser",methods = ['POST','GET'])
def checkUser():
    email = request.form.get('email',"").lower()
    # print("!",email,"!")
    conn = sqlite3.connect('equation.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM LOGIN WHERE email='"+email+"';")
    rows = cur.fetchall(); 

    for row in rows:
        print("USER EXISTS")
        return jsonify(userExists = "true")
    print("USER NOT EXISTS")
    return jsonify(userExists = "false")
    
        
    


@app.route("/solveEq",methods = ["GET","POST"])
def solveEq():
    #a = request.form['a']

    eq1 = request.form.get('eq1','').lower().replace(" ","")
    eq2 = request.form.get('eq2','').lower().replace(" ","")
    email = request.cookies.get('email','')
   
    print(eq1)
    print(eq2)

    x,y,m1,m2,c1,c2 = solveSimul(eq1,eq2)
    print("|||||",x,y,"||||")

    conn = sqlite3.connect('equation.db')
    conn.execute("INSERT INTO HISTORY VALUES ('"+email+"','"+eq1+"','"+eq2+"');")

    conn.commit()


    return jsonify(x = x, y = y, m1 = m1, c1 = c1, m2 = m2, c2 = c2) 

@app.route("/solveEqQuad", methods=['GET','POST'])
def eqSolveQuad():
    eq1 = request.form.get('eq1','').lower().replace(" ","")
    email = request.cookies.get('email','')

    print(eq1)

    sol1,sol2 = solveQuad(eq1)
    if(eq1.split("=")[1]):

        conn = sqlite3.connect('equation.db')
        conn.execute("INSERT INTO HISTORY VALUES ('"+email+"','"+eq1+"','""');")

        conn.commit()

    return jsonify(x = sol1, y = sol2) 


@app.route("/history",methods=['POST','GET']) 
def history():
    # email = request.form.get("email","").lower()
    email = request.cookies.get('email','')
    if(email == ''):
        return "<h1>PLEASE LOGIN TO VIEW HISTORY</h1>"
    conn = sqlite3.connect('equation.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM HISTORY WHERE email='"+email+"';")
    rows = cur.fetchall(); 
    arr = []
    for row in rows:
        arr.append((row[1],row[2]))
    print(arr)
    return(render_template("history.html",items = arr))

# @app.route("/ocr",methods=['POST','GET'])
def ocr(FilePath):
    LicenseCode = 'B4AB8B6D-6C89-4C60-88E1-C236A66A0E27';
    UserName =  'webtech';
    RequestUrl = "http://www.ocrwebservice.com/restservices/processDocument?gettext=true&newline=1";

    # FilePath = "simul.png"

    with open(FilePath, 'rb') as image_file:
        image_data = image_file.read()
    r = requests.post(RequestUrl, data=image_data, auth=(UserName, LicenseCode))
    jobj = json.loads(r.content)

    ext = str(jobj["OCRText"][0][0]).lower().replace(" ","")

    ext = ext.split("\n")

   
    
    if(len(ext) >=2  and ext[1] != ""):
        x,y,m1,m2,c1,c2 = solveSimul(ext[0],ext[1] )
        print(x,y)
        return((ext,x,y,m1,m2,c1,c2))

    else:
        sol1,sol2 = solveQuad(ext[0]) 
        print(sol1, sol2)
        return((ext,sol1,sol2))

    

@app.route("/upload",methods=['POST','GET'])
def upload():
    return(render_template("upload.html"))

# from flask_restful import reqparse
@app.route("/image",methods=['POST','GET'])
def image():

    email = request.cookies.get('email','')

    
   

    img = request.files.get('image', None)
    # print(img)




    

    img.save("IMGTEST.png")

    res = ocr("IMGTEST.png")

    if(len(res) == 3):
        conn = sqlite3.connect('equation.db')
        if (email!=''):
            conn.execute("INSERT INTO HISTORY VALUES ('"+email+"','"+res[0][0]+"','""');")
            conn.commit()
        return render_template("login.html",text = res[0], x = res[1], y = res[2])
        # return(jsonify(text = res[0], sol1 = res[1], sol2 = res[2]))
    
    conn = sqlite3.connect('equation.db')
    if (email!=''):
        conn.execute("INSERT INTO HISTORY VALUES ('"+email+"','"+res[0][0]+"','"+res[0][1]+"');")
        conn.commit()
    return render_template("login.html",text = res[0], x = res[1], y = res[2], m1 = res[3], m2 = res[4], c1 = res[5], c2 = res[6])
    # return (jsonify(text = res[0], x = res[1],y = res[2], m1 = res[3], m2 = res[4], c1 = res[5], c2 = res[6]))



    #cv2.imshow(img)
    


    



if __name__ == "__main__":
    app.run(debug = True)