from wtforms import Form, TextField, RadioField, DecimalField, BooleanField, SelectMultipleField, SelectField
from wtforms.validators import Required

class gunform(Form):
	guntype = RadioField('guntype', choices=[('Semiauto','Semiautomatic'),('Revolver','Revolver'),('Any','Any')], default='Any', validators = [Required()]) 
	maxprice = DecimalField('Max Price',default = 0)
	keywords = TextField('Keywords')
	safety = BooleanField(description='Safety')
	rail = BooleanField(description = "Rail")
	decocker = BooleanField(description="Decocker")

	#action checkboxes
	sa = BooleanField('SA',description = 'Single')
	da = BooleanField('DA',description = 'Double')
	dao = BooleanField('DAO',description = 'DAO')
	striker = BooleanField('Striker', description = "Striker")
	sada = BooleanField('SA/DA', description = "SA/DA")
	anyaction = BooleanField('any', description = "Any")

	#caliber checkboxes
	c380 = BooleanField('.380 ACP', description = '.380 ACP')
	c22 = BooleanField('.22 LR', description = '.22 LR')
	c38 = BooleanField('.38 Spl', description = '.38 Spl')
	c357 = BooleanField('.357 Magnum', description = '.357 Magnum')
	c9 = BooleanField('9mm', description = '9mm')
	c40 = BooleanField('.40 S&W', description = '.40 S&W')
	c45 = BooleanField('.45 ACP', description = '.45 ACP')
	c10 = BooleanField('10mm', description = '10mm')
	c50 = BooleanField('50 AE',description = '50 AE')
	c918 = BooleanField('9x18mm Makarov',description = '9x18mm Makarov')
	c357sig = BooleanField('.357 SIG',description = '.357 SIG')
	cany = BooleanField('any', description = 'Any')

	#size checkboxes
	compact = BooleanField('Compact', description = "Compact")
	subcompact = BooleanField('Subcompact', description = "Subcompact")
	full = BooleanField('Full', description = "Full")
	anysize = BooleanField('Any', description = "Any")

class Submitform(Form):
	manufacturer = TextField('manufacturer',validators=[Required()])
	model = TextField('model',validators=[Required()])
	action = RadioField('action',choices=[('Striker','Striker'),('SA','SA'),('DA','DA'),('SA/DA','SA/DA'),('DAO','DAO')])
	guntype = RadioField('guntype', choices=[('Semiautomatic','Semiautomatic'),('Revolver','Revolver')],default="Semiautomatic", validators = [Required()]) 
	caliber = TextField('caliber',validators = [Required()])
	size = RadioField('size',choices=[('Full','Full'),('Compact','Compact'),('Subcompact','Subcompact'),('Other','Other')])
	minprice = DecimalField('minprice')
	maxprice = DecimalField('maxprice')
	comments = TextField('comments')
	photo = TextField('photo')
	capacity = TextField('capacity')