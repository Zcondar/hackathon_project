from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('apage.html',a=0,b=0)

@app.route('/apage', methods=['post'])
def apage():

    test = request.form['button']
    data = request.form
    print(request.form['test'])
    print(data)
    print(test)
    a = 1
    b = 2
    return render_template('apage.html',a=a,b=b)


if __name__ == "__main__":
    app.run(debug=True)