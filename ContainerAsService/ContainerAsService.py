from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Email()])
    cname = TextField('Name:', validators=[validators.required()])
    memreq = TextField('Name:', validators=[validators.required()])
    cpureq = TextField('Name:', validators=[validators.required()])
    nsselection = TextField('Name:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print(request.form)
    name=None
    email=None
    cname=None
    cpureq=None
    memreq=None
    nsselection=None
    if(request.form != {}):
        print(form.errors)
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            cname = request.form['cname']
            cpureq = request.form['cpureq']
            memreq = request.form['memreq']
            nsselection = request.form['nsselection']

        if form.validate():
            # Save the comment here.
            flash('Starting Container Launch')
            # TODO: To add code for launching container here
            uid = name.lower().replace(" ", "-")
            replacement_dict = {
                                   "$$uid$$": uid,
                                    "$$ns$$": nsselection,
                                    "$$cname$$": cname,
                                    "$$email$$": email,
                                    "$$memreq$$": memreq,
                                    "$$cpureq$$": cpureq
            }
            print("Replacement params are: "+ str(replacement_dict))
            with open('podTemplates/jupyterhub.yml') as jfile:
                replaced_file = jfile.read()
                for key in replacement_dict:
                    replaced_file = replaced_file.replace(key, replacement_dict[key])
                print("Replaced File Content: " + replaced_file)
            newfilename = "podFiles/jupyter-" + uid
            with open(newfilename, 'w+') as nfile:
                nfile.write(replaced_file)
            print("Saved POD spec on local, starting kubernetes POD creation")
            cmd = "kubectl create -f " + newfilename
            print("Running command: " + cmd)
            stream = os.popen(cmd)
            output = stream.read()
            print(output)
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
    app.run(host="0.0.0.0", port=9000, debug=True)