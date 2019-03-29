from flask import Flask, render_template
from build_dashboard import render_dashboard
from transform import *
from dashboard import *


print('                                 ')
print('--------------------------------Initiate Flask applicaiton-----------------------------')
app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hly881206!@localhost:5432/dashboard'
# db.init_app(app)


print('@app.route("/")')
@app.route("/")
def load_dashboard():
  return render_template("dashboard.html")


if __name__ == "__main__":
    print('----------------------------The name is main-----------------------------------------')

    print('                                 ')
    print('-------------------------------Transforming the data--------------------------------')
    Data_transform()

    print('                                 ')
    print('-------------------------------Build the dashboard-------------------------------')
    Render_dashboard()

    print('                                 ')
    print('----------------------------Load dashboard in Browser-----------------------------------------')
    app.run(debug = True)