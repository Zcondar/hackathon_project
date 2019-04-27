from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('pickoriginal.html',a="pizza.jpg",b="chicken_wings.jpg")
    # return render_template('apage.html',a=1,b=2)

@app.route('/pickoriginal', methods=['post'])
def apage():

    result = request.form['button']
    # data = request.form
    # left = int(request.form['left'])
    # right = int(request.form['right'])
    # print(data)
    print(result)
    # if result == left:
    #     a = left + 1
    #     b = right
    # elif result == right:
    #     a = left
    #     b = right + 1
    # else:
    #     a=0
    #     b=0
    #     print("Error!")
    a = "Bento_Box.jpg"
    b = "Bimbimbap.jpg"

    return render_template('pickoriginal.html',a=a,b=b)


if __name__ == "__main__":
    app.run(debug=True)