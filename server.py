from bottle import route, run
from app import App


@route('/')
def index():
    return App().index()

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)