from flask import Flask, request,render_template, redirect
from forms import gunform, Submitform
from main import *
from handgun import handgun
from handgundb import *
app = Flask(__name__)


@app.route("/old", methods = ['GET','POST'])
def gunlist():
    form = None
    if request.method == 'POST':
        form = gunform(request.form)
        if form.validate():	
            handgunlist = process_data(form)
            db.close()
    	    guncount = len(handgunlist)
    	    return render_template("results.html",handgunlist = handgunlist, guncount = guncount)
    else:
        form = gunform()
    return render_template("gunform.html",form=form)

@app.route('/details/<model>/',methods=['GET'])
def showgun(model):
    gunitem = get_gun(model)
    return render_template("details.html",gun = gunitem)

@app.route('/',methods=['GET','POST'])
def mergedform():
    form = None
    guncount = 0
    handgunlist=[]
    if request.method == 'POST':
        form = gunform(request.form)
        if form.validate(): 
            handgunlist = process_data(form)
            db.close()
            guncount = len(handgunlist)
            return render_template("form.html",form=form,handgunlist = handgunlist, guncount = guncount)
    else:
        form = gunform()
    return render_template("form.html",form=form,guncount=0)

@app.route('/glossary/')
def glossary():
    return render_template("glossary.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/submit/',methods=['GET','POST'])
def submit():
    form = None
    if request.method == 'POST':
        form = Submitform(request.form)
        if form.validate(): 
            pass
            #return render_template("submit.html")
    else:
        form = Submitform()
    return render_template("submitform.html",form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):

    return render_template('500.html'),500


if __name__ == "__main__":
    app.run()
