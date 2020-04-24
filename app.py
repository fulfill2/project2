import os
import pymysql
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect, abort, session, jsonify

app = Flask(__name__, 
            static_folder="static",
            template_folder="views")
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key = 'sookbun'

db = pymysql.connect(
    user='root',
    passwd='123456',
    host='localhost',
    db='songs',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

def get_menu():
    cursor = db.cursor()
    cursor.execute("select id, songtitle from content")
    menu = [f"<li><a href='/{row['id']}'>{row['songtitle']}</a></li>"
            for row in cursor.fetchall()]
    return '\n'.join(menu)
    
def get_template(filename):
    with open('views/' + filename, 'r', encoding="utf-8") as f:
        template = f.read()
        
    return template

@app.route("/")
def index():    
    if 'user' in session:
        title = 'Welcome ' + session['user']['name']
        menu = get_menu()
        button_name = "logout"
    else:
        title = 'Welcome'
        menu = ""
        button_name = "login"
        
    message = '노래 가사집에 오신 것을 환영합니다.'
    return render_template('template.html',
                           id="",
                           title=title,
                           lyrics =message,
                           url = "",
                           menu=menu,
                           button_name = button_name)
                       

@app.route("/<id>")
def html(id):
    cursor = db.cursor()
    cursor.execute(f"select * from content where id = '{id}'")
    topic = cursor.fetchone()
    
    if topic is None:
        abort(404)

    return render_template('template.html',
                           id=topic['id'],
                           title=topic['songtitle'],
                           lyrics=topic['lyrics'],
                           url =topic['url'],
                           menu=get_menu(),
                           button_name = "logout"
                          )


@app.route("/delete/<id>")
def delete(id):
    cursor = db.cursor()
    cursor.execute(f"delete from content where songtitle='{id}'")
    db.commit()
    
    return redirect("/")

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cursor = db.cursor()
        sql = f"""
            insert into content (songtitle, lyrics, created, url, author_id)
            values ('{request.form['title']}', '{request.form['lyrics']}',
                    '{datetime.now()}', '{request.form['url']}', '4')
        """
        cursor.execute(sql)
        db.commit()

        return redirect('/')
    
    return render_template('create.html', 
                           title='신규 추가', 
                           menu=get_menu(),
                           )

@app.route("/login", methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute(f"""
            select id, name, password from author 
            where name = '{request.form['id']}'""")
        user = cursor.fetchone()
        
        if user is None:
            message = "<p>회원이 아닙니다.</p>"
        else:
            cursor.execute(f"""
            select id, name, password from author 
            where name = '{request.form['id']}' and 
                  password = SHA2('{request.form['password']}', 256)""")
            user = cursor.fetchone()
            
            if user is None:
                message = "<p>패스워드를 확인해 주세요</p>"
            else:
                # 로그인 성공에는 메인으로
                session['user'] = user
                return redirect("/")
    
    return render_template('login.html', 
                           message=message, 
                           menu=get_menu())

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route("/favicon.ico")
def favicon():
    return abort(404)

######################
## restful API

@app.route("/api/author", methods=['get', 'post'])
def author_list():
    cursor = db.cursor()
    
    if request.method == 'GET':
        cursor.execute("select * from author")    
        return render_template('template.html',
           id="",
           title=title,
           content=jsonify(cursor.fetchall()),
           menu=get_menu())
    elif request.method == 'POST':
        sql = f"""insert into author (name, password)
                  values ('{request.form['name']}',
                  SHA2('{request.form['password']}', 256))"""
        cursor.execute(sql)
        db.commit()
        
        return render_template('template_members.html',
                       id="",
                       title=title,
                       content=content,
                       menu=get_menu(),
                       link = "/",
                       message ="")
    
    return abort(405)

@app.route("/api/author/<author_id>", methods=['get', 'put', 'delete'])
def author(author_id):
    cursor = db.cursor()
    if request.method == 'GET':
        return render_template('template_members.html',
                       id="",
                       title=title,
                       content=content,
                       menu=get_menu(),
                       link = "/",
                       message ="회원정보수정에 성공하였습니다.")
#         cursor.execute(f"select * from author where id = {author_id}")
#         author = cursor.fetchone()

#         if author:
#             return render_template('template_members.html',
#                    id="",
#                    title=title,
#                    content=content,
#                    menu=get_menu())
#         else:
#             return abort(404)

    elif request.method == 'PUT':
        sql = f"""update author set
                  name = '{request.form['name']}',
                  password = SHA2('{request.form['password_new']}', 256)
                  where id = '{author_id}'"""

        cursor.execute(sql)
        db.commit()
        return render_template('template_members.html',
                               id="",
                               title=title,
                               content=content,
                               menu=get_menu(),
                               link = "/main",
                               message ="회원정보수정에 성공하였습니다.")
    
    elif request.method == 'DELETE':
        cursor.execute(f"delete from author where id = '{author_id}'")
        db.commit()
        return render_template('template_members.html',
                               id="",
                               title=title,
                               content=content,
                               menu=get_menu(),
                               link = "/main",
                               message ="회원정보 삭제에 성공하였습니다.")
    
    return abort(405)



app.run(port=8000)