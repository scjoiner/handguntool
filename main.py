from handgun import handgun
from handgundb import *
import json

def get_max_price(pricestring):
	pricestring = pricestring.replace('-',' ').split()
	max_price = 0
	for item in pricestring:
		if '$' in item:
			current_price = "".join(c for c in item.partition('$')[2].partition('.')[0] if c.isdigit())
			if current_price.isdigit() and int(current_price) > int(max_price):
				max_price = current_price
	return max_price

def get_min_price(pricestring):
	pricestring = pricestring.replace('-',' ').split()
	min_price = 99999
	for item in pricestring:
		if '$' in item:
			current_price = "".join(c for c in item.partition('$')[2].partition('.')[0] if c.isdigit())
			if current_price.isdigit() and int(current_price) < int(min_price):
				min_price = current_price
	return min_price

#loads handguns from database
def build_gun_list():
	gunlist = []
	for gun in Handguns.select():
		newgun = handgun(model = gun.model,
						manufacturer = gun.manufacturer,
						caliber = gun.caliber,
						size = gun.size,
						guntype = gun.guntype,
						action = gun.action,
						capacity = gun.capacity,
						minprice = gun.minprice,
						maxprice = gun.maxprice,
						comments = gun.comments,
						photo = gun.photo)
		gunlist.append(newgun)
	return gunlist

def parse_wiki_page():
	gunslist = []
	handguns = []
	with open("gunlist.txt") as f:
		gunlist_txt = f.read().replace("*","")
	gunlist = gunlist_txt.split('\n---\n')
	for item in gunlist:
		if "###" in item or "Manufacturer" not in item: continue #skip headings
		semiline = ""
		manufacturer, model, price, caliber, size, action, semi, capacity,comments = "","","","","","",False,"",""
		lines = item.split('\n')
		for line in lines:
			if 'Manufacturer:' in line:
				manufacturer = line.partition(':')[2]
			elif 'Model:' in line:
				model = line.partition(': ')[2]
			elif 'Price:' in line or 'MSRP:' in line or 'Street:' in line:
				price = line.partition(': ')[2]
			elif 'Caliber:' in line:
				caliber = line.partition(': ')[2]
			elif 'Size:' in line:
				size = line.partition(': ')[2]
			elif 'Action:' in line:
				action = line.partition(': ')[2]
			elif 'Capacity:' in line:
				capacity = line.partition(': ')[2]
			elif 'Type:' in line:
				semiline = line.partition(': ')[2]
			elif 'Comments:' in line:
				comments = str(line.partition(': ')[2])

		maxprice = get_max_price(price)
		minprice = get_min_price(price)

		if "full" in size.lower():
			size = "Fullsize"
		elif "sub" in size.lower():
			size = "Subcompact"
		elif "compact" in size.lower():
			size = "Compact"
		else:
			size = "Other"

		if "semi" in semiline.lower():
			guntype = "Semiauto"
		elif "revolver" in semiline.lower():
			guntype = "Revolver"
		else:
			continue
		
		if "striker" in action.lower():
			action = "Striker"
		elif "sa/da" in action.lower() or "da/sa" in action.lower():
			action = "SA/DA"
		elif "dao" in action.lower():
			action = "DAO"
		elif "sa" in action.lower() or "single" in action.lower():
			action = "SA"
		elif "da" in action.lower() or "double" in action.lower():
			action = "DA"
		else:
			action = "Other"

		if not comments: comments = "None"
		newgun = handgun(model = model,
						manufacturer = manufacturer,
						caliber = caliber,
						size = size,
						guntype = guntype,
						action = action,
						capacity = capacity,
						minprice = minprice,
						maxprice = maxprice,
						comments = comments,
						photo = "")
		handguns.append(newgun)
		if get_gun(model) is None:
			add_gun_to_db(newgun)
		else:
			update_gun(model,newgun)
	return handguns

def process_data(form):
	#handguns = parse_wiki_page()
	#update_photos()
	handguns = build_gun_list()
	gunlist = []
	actions = []
	calibers = []
	sizes = []
	keywords = []
	price = 0

	#actions
	if form.anyaction.data:
		actions = "Any"
	else:
		for field in [form.striker,form.sa,form.da,form.sada,form.dao]:
			if field.data:
				actions.append(str(field.description))
	#sizes
	if form.anysize.data:
		sizes = "Any"
	else:
		for field in [form.full,form.compact,form.subcompact]:
			if field.data:
				sizes.append(str(field.description))
	#price
	if form.maxprice.data > 0:
		price = form.maxprice.data

	#caliber
	if form.cany.data:
		calibers = "Any"
	else:
		for field in [form.c50,form.c357sig,form.c918,form.c22,form.c380,form.c9,form.c40,form.c45,form.c10,form.c38,form.c357]:
			if field.data:
				calibers.append(str(field.description))
	
	#type
	guntype = form.guntype.data

	#keywords
	if form.keywords.data:
		keywords = form.keywords.data.split(',')
	gunlist = match_guns(handguns, guntype,actions,sizes,calibers,price,keywords)
	return gunlist

def match_guns(handguns, guntype,actions,sizes,calibers,price,keywords):
	matches = []
	typematch, actionmatch, sizematch, calibermatch, pricematch = False, False, False, False, False
	keymatch = False
	for gun in handguns:

		if guntype == "Any" or gun.guntype == guntype:
			typematch = True
		else:
			continue

		if actions == "Any" or actions == [] or any(action == gun.action for action in actions):
			actionmatch = True
		else: 
			continue

		if sizes == "Any" or sizes == [] or any(size in gun.size for size in sizes):
			sizematch = True
		else:
			continue

		if calibers == "Any" or calibers == [] or any(caliber in gun.caliber for caliber in calibers):
			calibermatch = True
		else: 
			continue

		if price == 0 or price >= float(gun.minprice):
			pricematch = True
		else:
			continue

		if keywords == [] or any (str(word.lower()) in str(gun.comments.lower()) for word in keywords):
			keymatch = True
		else:
			continue		

		if all([typematch,actionmatch,sizematch,calibermatch,pricematch,keymatch]):
			matches.append(gun)

	return matches	
