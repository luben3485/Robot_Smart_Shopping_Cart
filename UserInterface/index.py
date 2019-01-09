#-*-coding:utf-8 -*-

import random
from flask import Flask,request
from flask import jsonify
import utils
import audio_recognition
import barcode

app = Flask(__name__,static_url_path='',root_path='/home/cart/Robot_Smart_Shopping_Cart/UserInterface')    
#静态模板index.html等都放在‘/home/ronny/mywebsite/static/'下。　路由不用再加’/static/index.html‘而是'index.html'就好
@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/Ajax_Audio')
def Ajax_Audio():
	test = request.args.get('mode')
	print('Audio recognition...')
	path = audio_recognition.speechrecognition()	
	result = {'path':path}
	return jsonify(result)

@app.route('/dataFromAjax')
def dataFromAjax():
	test = request.args.get('mode')
	#x,y = utils.getRandomXY(0,95,0,91)
	R1,R2,R3 = utils.RSSI_ave()
	D1 = utils.RssiToDistance(R1) 
	D2 = utils.RssiToDistance(R2) 
	D3 = utils.RssiToDistance(R3) 
	print("Distance D1:%f D2:%f D3:%f" %(D1,D2,D3))	
	x,y = utils.trilateration(D1,D2,D3)
	#print("location")
	print("real coordinate x: %f y: %f" %(x,y))
	#map_w = 6.6
	#map_l = 10.5
	map_w = 4
	map_l = 4
	#print(x,y)
	x_ = 100*x/map_l
	y_ = 100*y/map_w

	if x_ < 0 :
		x_ = 2
	elif x_ > 100:
		x_ = 85
	if y_ < 0 :
		y_ = 0
	elif y_ > 100:
		y_ = 85

	print("web map x: %f y: %f" %(x_,y_))
	result = {'x':x_,'y':y_}
	#result = ['aa',5]
	return jsonify(result)

@app.route('/Ajax_Barcode')
def Ajax_Barcode():
    barcodeData = barcode.barcode()
    result = {'barcodeData':barcodeData}
    return jsonify(result)

#有一個route處理語音辨識的訊息，回傳目的地在網頁顯示目標
#不斷發ajax要求後端目前的座標
#不斷發ajax要求後端目前的優惠訊息


if __name__ == '__main__':
	app.run(threaded=True,debug=False)
	#app.run(host='0.0.0.0',port=8081,debug=False)
