from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('apage.html',a=1,b=2)

@app.route('/apage', methods=['post'])
def apage():

    result = int(request.form['button'])
    # data = request.form
    left = int(request.form['left'])
    right = int(request.form['right'])
    # print(data)
    if result == left:
        a = left + 1
        b = right
    elif result == right:
        a = left
        b = right + 1
    else:
        a=0
        b=0
        print("Error!")

    return render_template('apage.html',a=a,b=b)

if __name__ == "__main__":
    app.run(debug=True)