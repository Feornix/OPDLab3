from flask import Flask, render_template, request

app = Flask(__name__)

def userAlreadyExist(lines, login):
    for i in range(0, len(lines), 2):
        if lines[i] == login + "\n":
            return True
    return False

def checkEmptyForms(login, password):
    if login == "" or password == "":
        return True
    return False

def checkAuthorisation(lines, login, password):
    for i in range(0, len(lines), 2):
        if login + "\n" == lines[i]:
            if password + "\n" == lines[i + 1]:
                return True
    return False

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", result="")

@app.route('/registration')
def regpage():
    return render_template("registration.html", result = "")

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def authorisation():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        output = "Неверный логин или пароль"
        file = open("data/data.txt", "r")
        lines = file.readlines()
        if checkAuthorisation(lines, login, password):
            output = "Вы успешно вошли, " + login
        file.close()
    return render_template("index.html", result = output)

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        trigger = False
        output = "Вы успешно зарегистрировались"
        login = request.form["login"]
        password = request.form["password"]
        file = open("data/data.txt", "r+")
        lines = file.readlines()
        trigger = userAlreadyExist(lines, login)
        if checkEmptyForms(login, password):
            output = "Все поля должны быть заполнены"
        elif trigger==False:
            file.write(login+"\n")
            file.write(password+"\n")
        else:
            output = "Такой пользователь уже существует"
        file.close()
    return render_template("registration.html", result = output)


if __name__=="__main__":
    app.run(debug=True)
