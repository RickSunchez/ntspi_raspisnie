from get_from_ntspi import get_schedule_from_ntspi
import json
import requests
import time

with open("secret.json", "r") as file:
	secret = json.load(file);

base = "https://api.telegram.org/bot" + secret["key"];
schedule = get_schedule_from_ntspi()

FACULTET_KEYBOARD = []
facultet_list = []

for elem in schedule:
	facultet = elem[0]["text"]
	FACULTET_KEYBOARD.append([facultet])
	facultet_list.append(facultet)

def getUpdates(offset):
	link = base + "/getUpdates"
	resp = requests.get(
		link,
		params={
			"offset": offset,
			"limit": 1
		}
	)

	return resp.json()

def sendMessage(chatID, text, rm=[[]], _type="keyboard"):
	link = base + "/sendMessage"

	reply_markup = json.dumps({
		"keyboard": rm,
		"one_time_keyboard": True
	})
	if _type == "inline":
		reply_markup = json.dumps(rm)

	resp = requests.get(
		link,
		params={
			"chat_id": chatID,
			"text": text,
			"reply_markup": reply_markup
		}
	)

def send_facultet_list(chatID):
	sendMessage(chatID, "Выберите файкультет", FACULTET_KEYBOARD)

def send_schedule(chatID, facultet):
	idx = facultet_list.index(facultet)
	active = schedule[idx][1:]

	SCHEDULE_KEYBOARD = {
		"inline_keyboard": [],
		"resize_keyboard": True
	}

	for group in active:
		SCHEDULE_KEYBOARD["inline_keyboard"].append(
			[
				{
					"text": group["text"],
					"url": group["link"]
				}
			]
		)

	sendMessage(chatID, "Выберите группу", SCHEDULE_KEYBOARD, "inline")
	print(SCHEDULE_KEYBOARD)

offset = 0

while True:
	data = getUpdates(offset)

	if len(data["result"]) > 0:
		answer = data["result"][0]
	else:
		continue

	message = answer["message"]
	chatID = message["chat"]["id"]
	text   = message["text"]

	if text == "/start":
		send_facultet_list(chatID)

	if text in facultet_list:
		send_schedule(chatID, text)

	offset = answer["update_id"]+1
	time.sleep(1)