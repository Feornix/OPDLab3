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

def checkSpaces(login):
    for i in range(0,len(login)):
        if login[i] == " ":
            return True
    return False

def checkNotEnglishLatters(login, password):
    for i in login:
        if not i.isascii():
            return True
    for j in password:
        if not j.isascii():
            return True
    return False

def checkSymbols(login):
    for i in login:
        if i == "&" or i == "=" or i == "+" or i == "<" or i == ">" or i=="," or i=="\'" or i=="@":
            return True
    return False



def checkAuthorisation(lines, login, password):
    for i in range(0, len(lines), 2):
        if login + "\n" == lines[i]:
            if password + "\n" == lines[i + 1]:
                return True
    return False

def checkRegistration(login, password):
    if checkEmptyForms(login, password):
        return False
    elif checkSpaces(login):
        return False
    elif checkNotEnglishLatters(login, password):
        return False
    elif checkSymbols(login):
        return False
    else:
        return True

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
        if checkRegistration(login, password)==False:
            output = "Введён некорректный логин или пароль"
        elif trigger==False:
            file.write(login+"\n")
            file.write(password+"\n")
        else:
            output = "Такой пользователь уже существует"
        file.close()
    return render_template("registration.html", result = output)


if __name__=="__main__":
    app.run(debug=True)
