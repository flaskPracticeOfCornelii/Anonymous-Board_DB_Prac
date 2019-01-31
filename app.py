from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect('board.sqlite3')
    cur = conn.cursor()
    
    sql = "SELECT * FROM posts"
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    
    return render_template("index.html",data=data)
    
    
@app.route("/create",methods=["POST"])
def create():
    
    title = request.form.get('title')
    content = request.form.get('content')
    query("create","posts",title=title,content=content)
    
    return redirect("/")
    

@app.route("/delete", methods=["POST"])
def delete():
    article_id = request.form.get("id")
    query("delete",'posts',id=article_id)
    
    return redirect("/")


    
@app.route("/edit",methods=["POST"])
def edit():
    article_id = request.form.get("id")
    data = query("select_all","posts",id=article_id)
    
    return render_template("revise.html",title=data[0][1],content=data[0][2],article_id=article_id)
    
@app.route("/revise/<int:article_id>")
def revise(article_id):

    title = request.args.get('title')
    content = request.args.get('content')

    query("update","posts","title",title,id=article_id)
    query("update","posts","content",content,id=article_id)
    
    return redirect("/")
    
    
    
    
def query(query_name,table_name,*args,**kwargs):
    conn = sqlite3.connect('board.sqlite3')
    cur = conn.cursor()
    data = None
    
    if query_name == "select_all":
        sql = "SELECT * FROM {} where id = {}".format(table_name,kwargs['id'])
        cur.execute(sql)
        data = cur.fetchall()
        
    elif query_name == "select_one":
        sql = "SELECT * FROM {} WHERE id = {}".format(table_name,kwargs['id'])
        cur.execute(sql)
        data = cur.fetchone()
        
    elif query_name == "create":
        sql = "INSERT INTO {} (title, content) VALUES ('{}','{}')".format(table_name,kwargs['title'],kwargs['content'])
        cur.execute(sql)
        conn.commit()
    
    elif query_name == "update":
        sql = "UPDATE {} SET {}='{}' WHERE id = {}".format(table_name,args[0],args[1],kwargs['id'])
        cur.execute(sql)
        conn.commit()
        
    elif query_name == "delete":
        sql = "DELETE FROM {} WHERE id = {}".format(table_name,kwargs['id'])
        cur.execute(sql)
        conn.commit()
        
    conn.close()
    
    return data
