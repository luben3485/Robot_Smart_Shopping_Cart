 
import speech_recognition as sr

def speechrecognition():
	# Record Audio
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
 
	# Speech recognition using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		result = r.recognize_google(audio, language='zh-TW')
		print("You said: " + result)
		product = ['蘋果','洗髮精','泡麵','衣服']	
		for i in range(len(product)):
			find_value = result.find(product[i])
			if find_value != -1:
				return i
		return -1	
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
		
def main():
	speechrecognition()

if __name__ == '__main__':
	main()
