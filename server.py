from bottle import route, run, request
from app import App

app = App()

@route('/')
def index():
    return app.index()

@route('/company/<company_name>')
def company_people(company_name):
    return app.company_people(company_name)

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)