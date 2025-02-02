from flask import redirect
import pandas as pd
from dtale.app import build_app
from dtale.views import startup
import os

if __name__ == '__main__':
    app = build_app(reaper_on=False)

    @app.route("/create-df")
    def create_df():
        script_dir = os.path.dirname(__file__)
        titanic_path = os.path.join(script_dir, 'assets', 'titanic.csv')
        df = pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
        df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'Salary': [50000, 60000, 70000, 80000, 90000]
    })
        df = pd.read_csv(titanic_path)
        instance = startup(data=df, ignore_duplicate=True)
        return redirect(f"/dtale/main/{instance._data_id}", code=302)

    @app.route("/")
    def hello_world():
        return 'Hi there, load data using <a href="/create-df">create-df</a>'

    app.run(host="0.0.0.0", port=8080)