#-*-coding:utf-8 -*-

import random
from flask import Flask,request
from flask import jsonify
import utils
import audio_recognition
#import barcode
import time

#app = Flask(__name__,static_url_path='',root_path='/home/luben/data/college/robot/Robot_Smart_Shopping_Cart/UserInterface')    
app = Flask(__name__,static_url_path='',root_path='/home/cart/Robot_Smart_Shopping_Cart/UserInterface')    
#静态模板index.html等都放在‘/home/ronny/mywebsite/static/'下。　路由不用再加’/static/index.html‘而是'index.html'就好
@app.route('/')
def index():
	return app.send_static_file('map.html')

@app.route('/Ajax_Audio')
def Ajax_Audio():
	test = request.args.get('mode')
	print('Audio recognition...')
	path = audio_recognition.speechrecognition()	
	#path = 0
	result = {'path':path}
	return jsonify(result)

@app.route('/predictLocation')
def dataFromAjax():
	test = request.args.get('mode')
	#x,y = utils.getRandomXY(0,95,0,91)
	#x,y = 6,1
	index = utils.predPosition()-1
	x=[1,1,1,1,2,3,4,5,6,7,7,7,7,6,5,4,3,2]
	y=[4,3,2,1,1,1,1,1,1,1,2,3,4,4,4,4,4,4]
	#index = random.randint(0,5)
	#print(x,y)
	result = {'x':x[index],'y':y[index]}
	#result = ['aa',5]
	return jsonify(result)

@app.route('/Ajax_Barcode')
def Ajax_Barcode():
    #barcodeData = barcode.barcode()
    #result = {'barcodeData':barcodeData}
    #return jsonify(result)
    return 0
#有一個route處理語音辨識的訊息，回傳目的地在網頁顯示目標
#不斷發ajax要求後端目前的座標
#不斷發ajax要求後端目前的優惠訊息


if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0',port=8081,debug=False)
