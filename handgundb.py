from peewee import *
from handgun import *
import json
import config
db = MySQLDatabase('handguns',host = 'localhost', user=config.username,password=config.password)

class Handguns(Model):
	manufacturer = TextField()
	model = TextField()
	caliber = TextField()
	guntype = TextField()
	maxprice = IntegerField()
	minprice = IntegerField()
	action = TextField()
	size = TextField()
	capacity = TextField()
	comments = TextField()
	photo = TextField()

	class Meta:
		database = db

db.connect()
Handguns.create_table(True)

def get_gun(model):
	gun = None
	try:
		gun = Handguns.get(Handguns.model == model)
	except: return None
	gun = handgun(model = gun.model,
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
	return gun

def update_gun(model,newgun):
	gun = Handguns.get(Handguns.model == model)
	gun.model = newgun.model
	gun.manufacturer = newgun.manufacturer
	gun.size = newgun.size
	gun.capacity=newgun.capacity
	gun.comments = newgun.comments
	gun.guntype=newgun.guntype
	gun.action = newgun.action
	gun.caliber = newgun.caliber
	gun.minprice = newgun.minprice
	gun.save()

def add_gun_to_db(handgun):
	Handguns.create(manufacturer = handgun.manufacturer,
					model = handgun.model,
					caliber = handgun.caliber,
					guntype = handgun.guntype,
					minprice = handgun.minprice,
					maxprice = handgun.maxprice,
					action = handgun.action,
					size = handgun.size,
					capacity = handgun.capacity,
					comments = handgun.comments,
					photo = handgun.photo)

def update_photos():
	photos = {}
	allguns = Handguns.select()
	with open ("/var/www/FlaskApp/FlaskApp/static/photos.json",'r') as f:
	#with open ("photos.json",'r') as f:
	
		photos.update(json.load(f))
	for gun in allguns:
		gunphoto = "placeholder"
		if " " not in gun.model:
			gunphoto = gun.model.lower()
		else:
			for model,filename in photos.iteritems(): 
				if model in gun.model.lower():
					gunphoto = filename
					break
			
		gun.photo=gunphoto
		gun.save()

def print_all_guns():
	for handgun in Handguns.select():
		print handgun.id, handgun.manufacturer, handgun.model, handgun.maxprice
	print "Total guns: %d " % Handguns.select().count()

#parse_wiki_page()
#print_all_guns()

#gunlist = get_guns_by_comment('safety')
#for gun in gunlist:
#	print gun.id, gun.model, gun.size
#print "Found %d guns. " % gunlist.count()
