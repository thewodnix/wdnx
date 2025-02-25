from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index/<name>')
def index(name):
    param = {}
    param['title'] = f'{name}'
    return render_template('base.html', **param)

@app.route('/training/<prof>')
def trainig(prof):
    param = {}
    param['prof'] = f'{prof}'
    return render_template('training.html', **param)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
