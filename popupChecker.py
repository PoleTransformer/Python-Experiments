import requests
import time
import re
webhookUrl = "https://ptb.discord.com/api/webhooks/862514856002453549/ojYx0Ktj69n_tk6zxPuSLmauewyjkJ4gveZ32t6qTv1TN1Csi2t2aYi7oFMx4nDN0oI_"
lastOutput = ''
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
data = {'tz':''}
while True:
	url = "https://caseytree.site/index.php"
	try:
		r = requests.post(url, data=data, headers=headers, timeout=5)
		if lastOutput == r.text:
			print ("same popup as last time")
		elif r.text == "":
			print("empty response")
		else:
			print ("different popup")
			lastOutput = r.text
			print(r.text)
			match = re.findall("\"(.*?)\"", lastOutput)
			encodedURL = match[8]
			listOfCharCodes = encodedURL.split(",")
			listOfCharCodes.reverse();
			fixedCharCodes = [i[::-1] for i in listOfCharCodes]
			for x in fixedCharCodes:
				x[::-1]
			outputURL = ""
			for x in fixedCharCodes:
				outputURL += chr(int(x))
			message = "!add {0}/CEDfdfffdgfgfgdfgdfgfMPr88CtySS/#\n {0}/EDfdfffdgfgfgdfgdfgfMPr88CtySS/#\n {0}/CHfdfffdgfgfgdfgdfgfMPr88CtySS/#\n {0}/FFfdfffdgfgfgdfgdfgfMPr88CtySS/#\n {0}/MAfdfffdgfgfgdfgdfgf-188CtySS/#".format(outputURL)
			print (message)
			webhookData = {
				"content" : message
			}
			try:
				sendWebhook = requests.post(webhookUrl, json = webhookData, timeout=1)
			except requests.exceptions.RequestException as e:
				print("Error sending webhook:", e)
	except requests.exceptions.RequestException as e:
		print ("There's an error:", e)
	time.sleep(1)