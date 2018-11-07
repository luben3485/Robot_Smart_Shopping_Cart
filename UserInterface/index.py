#-*-coding:utf-8 -*-

import random
from flask import Flask,request
from flask import jsonify
import utils

app = Flask(__name__,static_url_path='',root_path='/home/luben3485/college/robot/website')    
#静态模板index.html等都放在‘/home/ronny/mywebsite/static/'下。　路由不用再加’/static/index.html‘而是'index.html'就好
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/dataFromAjax')
def dataFromAjax():
    test = request.args.get('mode')
    x,y = utils.getRandomXY(0,95,0,91)
    print(x,y)
    result = {'x':x,'y':y}
    #result = ['aa',5]
    return jsonify(result)


#有一個route處理語音辨識的訊息，回傳目的地在網頁顯示目標
#不斷發ajax要求後端目前的座標
#不斷發ajax要求後端目前的優惠訊息


if __name__ == '__main__':
	app.run()
	#app.run(host='0.0.0.0',port=8081,debug=False)
