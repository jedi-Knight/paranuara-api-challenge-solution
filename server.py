from bottle import route, run, error
from app import App

app = App()

@route('/')
def index():
    return app.index()

@route('/company/<company_name>')
def company_users(company_name):
    return app.company_users(company_name)

@route('/user/<user_name>')
def user(user_name):
    return app.user(user_name)

@route('/user/<user_name_1>/<user_name_2>')
def two_users(user_name_1, user_name_2):
    return app.two_users(user_name_1, user_name_2)

@error(404)
def error404(error):
    return 'Endpoint not implemented. Please refer to API docs for available endpoints.'

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)