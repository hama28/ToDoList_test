import logging
from flask import Flask, abort, request, render_template, redirect, session
import ds
import login


app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)
app.secret_key = 'm9XE4JH5dBOQK4o4'


@app.route('/')
def home():
    return render_template('index.html')


# ----- 通常ページ -----
@app.route('/todo')
def todo():
    data = ds.get_all()
    message = "ToDoList にようこそ！"
    return render_template('todo.html',
                    message=message,
                    data=data)

@app.route('/todo/check/<key_id>', methods=['POST'])
def check(key_id=None):
    entity = ds.get_by_id(key_id)
    if not entity:
        abort(404)
        return entity
    entity['check'] = "1"
    ds.update(entity)
    return redirect('/todo')
# ---------------


# ----- ログインページ -----
@app.route('/todo/login')
def login():
    return render_template('login.html')

@app.route('/todo/check_login', methods=['POST'])
def check_login():
    # フォームの値の取得
    name, pw = (None, None)
    if 'name' in request.form:
        name = request.form['name']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (name is None) or (pw is None):
        return redirect('/todo')
    # ログインチェック
    if try_login(name, pw) == False:
        return """
        <h1>ユーザー名かパスワードが間違っています</h1>
        <p><a href="/todo/login">ログインフォームに戻る</a></p>
        """
    # 管理ページにリダイレクト
    return redirect('/todo/admin')

# ログイン処理を行う
def try_login(name, pw):
    entity = login.get_by_id()
    # ユーザー名があっているかチェック
    if entity['name'] != name:
        return False
    # パスワードがあっているかチェック
    if entity['pw'] != pw:
        return False
    # ログイン処理を実行
    session['login'] = name
    return True

# ログインしているかチェック
def is_login():
    if 'login' in session:
        return True
    return False
# ---------------


# ----- 管理者ページ -----
@app.route('/todo/admin')
def admin():
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/todo/login">ログインする</a></p>
        """
    data = ds.get_all()
    message = "ToDoList admin"
    return render_template('admin.html',
                    message=message,
                    data=data)

@app.route('/todo/add', methods=['POST'])
def add():
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/todo/login">ログインする</a></p>
        """
    addtodo = request.form.get('addtodo', '')
    if addtodo == '':
        return redirect('/todo/admin')
    things = addtodo
    check = "0"
    ds.insert(things, check)
    return redirect('/todo/admin'), 201

@app.route('/todo/delete/<key_id>', methods=['POST'])
def delete(key_id=None):
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/todo/login">ログインする</a></p>
        """
    ds.delete(key_id)
    return redirect('/todo/admin'), 204

@app.route('/todo/logout')
def logout_page():
    # ログアウト処理の実行
    try_logout()
    return """
    <h1>ログアウトしました</h1>
    <p><a href="/todo">ToDoリストに戻る</a></p>
    """

# ログアウトする
def try_logout():
    session.pop('login', None)
    return True
# ---------------


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)