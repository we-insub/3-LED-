#Flask 웹상태, api서버를 만드는데 특화된 웹 프레임워크 (Web Framework)
#(웹프레임워크 동적페이지,웹,등 보조용 app의 프레임워크)
#편한 라이브러리 제공 하는 툴
import os #os운영체제 제어할수있는것 os모듈 불러오기
from flask_sqlalchemy import SQLAlchemy
#flask_sqlalchemy 를 사용하기위해 flask_sqlalchemy 패키지를 임포트했다.
#즉 SQLAlchemy 패키지에서 falsk_sqlalchemy 를 사용할것이다
from flask import Flask, render_template
#flask 패키지에서 flask모듈을 사용하며 웹페에지 컨텐츠에 대한
#템플리트를 사용할수 있게 하는것.
from gpiozero import LEDBoard
#LEDbord 에서 gpiozero 사용할것,
import datetime # datetime 날짜 시간 라이브러리



app = Flask(__name__)
# app이라는 변수로 flask모듈을 쓸수 있도록 ?... 즉 (__name__) 자리에 falsk가 오는것인가?
# 플라스크 인스턴스 생성\
leds = LEDBoard(14, 15, 18)
#leds = 14 15 18 번 핀을 꼽고 (li형)

led_states = {
        'red':0,
        'green':0,
        'yellow':0
}
#빨 초 노 는 기본값이 0 으로 선언이 되어있어 전원 off인상태로 선언

db = SQLAlchemy()
#calss이름에 보이는  Mysuer (db.model)즉 db.model 은 SQLAlchemy에 저장이 된다
class Myuser(db.Model):
    __tablename__ = 'leddb' # leddb라고 정의한 테이블에 아래 키들이 맵핑 선언
    id = db.Column(db.Integer, primary_key=True)
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    yellow = db.Column(db.Integer)
    time = db.Column(db.String(30))
    # Column - DB Table 에서 인련의 데이터값과 테이블에서 열을 말한다.
    # 데이터 값을 단일 구조 데이터 값으로 받아들인다.
    # Integer - 데이터베이스 자료형이 정수이지만 null 값이 필요한경우 사용

# ex) 192.168.1.57:5000/red/0
@app.route('/<color>/<int:state>',methods=['GET','POST'])
# @app.route 함수 코드를 바꾸지않고 안의 내용만 바꾸는것
# @은 작성자 를 나타낸다
# ()괄호의 조건을 만나게되면 메소드에 잡고, 자료를 올리게 된다 (저장)
def led_switch(color, state):
    global led_states
    led_states[color] = state
    leds.value = tuple(led_states.values())
    # global 전역변수 사용
    # color, state 결과가 튜플로 저장된다
    # 튜플형 led_states[color] 은 state를 받아들인다
    # 리스트 값으로 찍힌 값을튜플로 형 변환

    myuser = Myuser()
    myuser.time = str(now = datetime.datetime.now.strftime('%m %d %I %m'))
    # 미국 기준으로 시간이 뜨는데 timezon 라이브러리를 이용하여 한국시간으로 변경을 하고자
    # 시도해보았으나 실력 미숙으로 실패

        myuser.red = led_states['red']
        myuser.yellow = led_states['yellow']
        myuser.green = led_states['green']
        # red의 값이 들어온다면 red에 입력해라

    db.session.add(myuser)
    # DB Table myuser 생성
    db.session.commit()
    # commit

    return render_template('testled.html', led_states=led_states)
    # testlen.html의 결과값은 template에 저장하여라

@app.route('/all/<int:state>', methods=['GET', 'POST'])
def all_on_off(state):
    myuser = Myuser()
    global led_states

    if state is 0:
        led_states = {
            'red': 0,
            'green': 0,
            'yellow': 0
        }
        myuser.red = 0
        myuser.yellow = 0
        myuser.green = 0
        myuser.time = str(now = datetime.datetime.now.strftime('%m %d %I %m'))

    elif state is 1:
        led_states = {
            'red': 1,
            'green': 1,
            'yellow': 1
        }
        myuser.red = 1
        myuser.yellow = 1
        myuser.green = 1
        myuser.time = str(now = datetime.datetime.now.strftime('%m %d %I %m'))

    db.session.add(myuser)
    db.session.commit()

    leds.value = tuple(led_states.values())
    return render_template('index.html', led_states=led_states)

if __name__ == "__main__":

    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    # db 파일의 경로 path상에서 나오는 경로가아닌, 데이터베이스 자체에 경로에 접속하는 경로
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # db 정보가 바뀌면 정보 업데이트를 바로 해주는 명령어
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # event 처리를 하지 않겠다 선언. (불안전해서 사용하지않음)
    app.config['SECRET_KEY'] = 'yellowmango'
    # db에 접근할때 key를 갖고 있는 보안

    db.init_app(app)
    db.app = app
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # 웹 앱 실행요청


