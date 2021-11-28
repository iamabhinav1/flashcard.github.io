from flask import Flask;
from flask import render_template,request

import sqlite3
import os

from flask import g
from datetime import datetime
app= Flask (__name__)


@app.before_request
def before_request():
    g.db = sqlite3.connect("RATING.db")

@app.route("/")
def defaultHome():
    return render_template('home.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=["POSt","GET"])
def login():
    if request.method=="POST":
        userName= request.form['name']
        userPassword=request.form['password']
        if userName=='admin' and userPassword=='admin123':   
            connection= sqlite3.connect(database="RATING.db")
            
            cursor = connection.cursor()
            cursor.execute("SELECT Review FROM RATING")
            cur=connection.cursor()
            
            entry=cursor.fetchall()
            print(entry)

            num=len(entry)
            print("num=")
            print(num)
            average=0
            for i in range(0, num):
               
                average+=int(entry[i][0])
            
            print(average)
            
            if(num>0):
                average=average/num

            connections= sqlite3.connect(database="RCAPITAL.db")
            cursor1 = connections.cursor()
            cursor1.execute("SELECT Review FROM RATING")
            
            
            entry=cursor1.fetchall()
            

            num=len(entry)
            
            average1=0
            for i in range(0, num):
               
                average1+=int(entry[i][0])
            
           
            
            if(num>0):
                average1=average1/num

    
            return(render_template('dashboard.html',ans=average, ans1=average1))
        else:
            return render_template("home.html")

    else:
        userName = request.args.get('name')
        return render_template('login.html', name=userName)


@app.route("/Capital")
def side():
    return render_template('Capital.html')
@app.route("/request")
def result(request):
    g=request.GET['r']
    g=int(g)
    return(render_template(request,'flipflashcard.html',{'ans':g}))


@app.route("/dashboard")
def dashboard(request):
    connection= sqlite3.connect(database="RATING.db")
    sql_select_Query = "select * from RATING"
    cursor1 = connection.cursor()
    cursor1.execute(sql_select_Query)
    # get all records
    records = cursor1.fetchall()
    print("Total number of rows in table: ", cursor1.rowcount)

    
    return(render_template(request,'dashboard.html',{'ans1':cursor1.rowcount}))



@app.route("/flipflashcard")
def main():
    return render_template('flipflashcard.html')

import time
import datetime

@app.route("/flipflashcard", methods=["POST"])
def flipflashcard():
    Review=request.form['Review']
   

    timestamp = time.time()
    #timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    connection= sqlite3.connect(database="RATING.db")
    cursor= connection.cursor()
    
    query="INSERT INTO Rating VALUES({r},{t})".format(r=Review,t=timestamp)
    
    
    cursor.execute(query)
    connection.commit()
    return render_template('flipflashcard.html')

@app.route("/Capital", methods=["POST"])
def Capital():
    Review=request.form['Review']
    connection= sqlite3.connect(database="RCAPITAL.db")
    cursor= connection.cursor()
    query1="INSERT INTO RATING VALUES({r})".format(r=Review)
    cursor.execute(query1)
    connection.commit()
    return render_template('Capital.html')

@app.route("/dashboard")
def dashboard1(request):
    
    
    connection= sqlite3.connect(database="RCAPITAL.db")
    sql_select_Query = "select * from RATING"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    # get all records
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)
    return(render_template(request,'dashboard.html',{'ans':cursor.rowcount}))




    
if __name__ == '__main__':
    app.run(debug=True)