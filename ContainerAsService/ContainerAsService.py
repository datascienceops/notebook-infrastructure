from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
import subprocess

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
def home():
    return render_template('newindex.html')

@app.route("/container-request", methods=['GET', 'POST'])
def containerrequest():
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
            logs = "Failed in handling your request"
            # list of strings representing the command
            args = ['kubectl', 'create', '-f', newfilename]
            command_errs = False
            try:
                # stdout = subprocess.PIPE lets you redirect the output
                res = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError:
                print("Error while triggering kubectl command")
                command_errs = True

            if not command_errs:
                res.wait()  # wait for process to finish; this also sets the returncode variable inside 'res'
                if res.returncode != 0:
                    command_errs = True
                    print("Failed while executing kubectl command")
                    errors = res.stderr.read()
                    errors = str(errors, 'utf-8')
                    logs = "Terminal Logs: {}".format(errors)
                else:
                    print("Successfully completed execution")
                    result = res.stdout.read()
                    result = str(result, 'utf-8')
                    logs = "Terminal Logs: {}".format(result)
                print(logs)
            if command_errs:
                err_str = logs
                flash('Error - ' + str(err_str))
            else:
                flash('Successfully created resource')
        else:
            err_str = ""
            if form.errors:
                err_str+= "Incomplete form or invalid inputs"
            flash('Error - ' + str(err_str))

        return render_template('index.html', form=form)
    else:
        print("Empty input, no button clicked yet")
        return render_template('index.html', form=form)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)