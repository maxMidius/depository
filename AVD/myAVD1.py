#!/usr/local/bin/python
#-----------------------
# vi: sw=4 ts=4 expandtab
#-------------------------

import os, sys
import dash
import dash_core_components as dcc
import dash_html_components as dhtml

externalScripts=[
    { 
              'src' : "https://cdnjs.cloudflare.com/ajax/libs/svg.js/3.0.16/svg.js",
      'crossorigin' : "anonymous"
    } , 
    {
          'src' : "https://code.jquery.com/jquery-3.5.1.js" ,
  'crossorigin' : "anonymous"
    }

]
externalStyles=[
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://www.w3schools.com/w3css/4/w3.css"
]
app=dash.Dash(__name__, external_scripts=externalScripts, external_stylesheets=externalStyles)
app.layout = dhtml.Div(id='div1', children='''
This is dvi1
''')


if __name__ == "__main__" :
    app.run_server(debug=True, port=8080)
