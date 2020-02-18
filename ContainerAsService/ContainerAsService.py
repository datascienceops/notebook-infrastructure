from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    uid = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Email()])
    cname = TextField('Name:', validators=[validators.required()])
    memreq = TextField('Name:', validators=[validators.required()])
    cpureq = TextField('Name:', validators=[validators.required()])
    nsselection = TextField('Name:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print(request.form)
    if(request.form != {}):
        print(form.errors)
        if request.method == 'POST':
            name = request.form['name']
            uid = request.form['uid']
            email = request.form['email']
            cname = request.form['cname']
            cpuselection = request.form['cpuselection']
            memselection = request.form['memselection']
            nsselection = request.form['nsselection']

        if form.validate():
            # Save the comment here.
            flash('Starting Container Launch')
            # TODO: To add code for launching container here
        else:
            err_str = ""
            if form.errors:
                for err in form.errors:
                    err_str += " " + str(err) + " : "
                    err_str += str(form.errors[err][0])
            flash('Error - ' + str(err_str))

        return render_template('index.html', form=form)
    else:
        print("Empty input, no button clicked yet")
        return render_template('index.html', form=form)
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)