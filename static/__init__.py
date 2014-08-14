from flask import Flask, request,render_template, redirect
from forms import gunform
from main import *
from handgun import handgun
from handgundb import *
app = Flask(__name__)


@app.route("/", methods = ['GET','POST'])
def gunlist():
    form = None
    if request.method == 'POST':
	form = gunform(request.form)
	if form.validate():	
	    handgunlist = process_data(form)
	    guncount = len(handgunlist)

	    return render_template("results.html",handgunlist = handgunlist, guncount = guncount)
    else:
        form = gunform()
    return render_template("gunform.html",form=form)

@app.route('/details/<model>/',methods=['GET'])
def showgun(model):
    gunitem = get_gun(model)
    return render_template("details.html",gun = gunitem)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):

    return render_template('500.html'),500


if __name__ == "__main__":
    app.run()
