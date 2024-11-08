from flask import Flask, render_template

app = Flask(__name__, template_folder='./build', static_folder='./build/static')

@app.route('/a')
def route_a():
  return render_template('index.html')

@app.route('/b')
def route_b():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)
