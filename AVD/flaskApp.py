#!/usr/local/bin/python3
#------------------------------------------
# vi: sw=4 ts=4 expandtab
#------------------------------------------
from flask import Flask, render_template, url_for
from markupsafe import escape
app = Flask(__name__)

@app.route("/") 
def rootPage( ) : 
    return ("Hello World")

@app.route("/avd/<avdName>") 
@app.route("/avd/") 
def renderAvd(avdName="myAVD" ) : 
    return ( render_template(f"{avdName}.html") )

if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True)
    
