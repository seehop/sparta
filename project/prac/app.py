from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
## http://localhost:5000
@app.route('/test', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    print(title_receive)
    return jsonify({'result': 'success', 'msg': title_receive})

## http://localhost:5000/greeting?name=sohee&age=29
@app.route('/greeting', methods=['GET'])
def greeting():
    name = request.args.get('name')
    age = request.args.get('age')
    print(name)
    print(age)
    msg= 'Hi! ' + name +'(' + age + ")"
    return jsonify({'result':'success', 'msg':msg})

## GET과 비교
@app.route('/greeting', methods=['POST'])
def greeting_post():
    name = request.form['name']
    age = request.form['age']
    print(name, age)
    msg = "안녕하세요 " + name + "님. 당신은" + age + " 살이군요!"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)