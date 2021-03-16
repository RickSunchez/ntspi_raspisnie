import requests
from bs4 import BeautifulSoup
import json

def get_schedule_from_ntspi():
	r = requests.get("https://www.ntspi.ru/student/rasp/")

	soup = BeautifulSoup(r.text,  "html.parser")

	table = soup.find_all("table")
	raspisanie = table[2]

	arr = []
	base = "https://www.ntspi.ru"
	tmp = {
		"text": "",
		"link": ""
	}

	for tr in raspisanie.find_all("tr"):
		idx = 0

		for td in tr.find_all("td"):
			if len(arr) == idx:
				arr.append([])
			if td.find("a"):
				for a in td.find_all("a"):
					if a:
						node = tmp.copy()

						link = base + a.get("href")
						node["text"] = a.text
						node["link"] = link

						arr[idx].append(node)
			elif len(td.text) > 0:
				if td.text != "\n\n":
					node = tmp.copy()
					node["text"] = td.text
					arr[idx].append(node)

			idx += 1

	return arr;