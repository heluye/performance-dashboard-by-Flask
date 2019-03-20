from flask import Flask, render_template
from build_dashboard import render_dashboard

from transform import *
from dashboard import *
from BitBucketAPIcall import *
# import config

print('                                 ')
print('--------------------------------Initiate Flask applicaiton-----------------------------')
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hly881206!@localhost:5432/dashboard'
# db.init_app(app)

# authorname_list = ['Mari Mizoguchi','Melinda Song', 'Edmond Wong', 'Emma Liu','Vicky Lee']
# time_start = '2019-02-20'
# time_end = '2019-03-20'

# URL=  config.URL
# ENDPOINT1 = config.ENDPOINT1
# ACCESS_TOKEN = config.ACCESS_TOKEN
# time_start = config.time_start
# time_end = config.time_end
# authorname_list=config.authorname_list


print('@app.route("/")')
@app.route("/")
def load_dashbord():
    return render_template("index.html")

# @app.route("/about")
# def about():
#   return render_template("commits_streak2.html")

print('@app.route("/dashboard")')
@app.route("/dashboard")
def dashboard():
  return render_template("dashboard.html")


if __name__ == "__main__":
    print('                                 ')
    print('----------------------------The name is main-----------------------------------------')

    print('                                 ')
    print('-------------------------------Making Bitbucket API calls-------------------------')
    BitBucketAPIcall()

    print('                                 ')
    print('-------------------------------Transforming the data--------------------------------')
    Data_transform()

    print('                                 ')
    print('-------------------------------Rendering the dashboard-------------------------------')
    Render_dashboard()

    print('                                 ')
    print('----------------------------Run the app-----------------------------------------')
    app.run(debug = True)