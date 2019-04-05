Open a git bash terminal with the cloned repo from Bitbucket.

Set up a virtual environment in that folder.

Pip install all packages in requirement.txt in the virtual environment.

Activate the virtual environment, for windows system:
$source venv/Scripts/activate

To collect data from Bickbucket API, type in terminal:
$python DataCollection_main.py

To generate dashboard, type in terminal:
$python Dashboard_main.py

Once the program finish running, copy the http link to a browser, for example:
the first dashboard:
http://127.0.0.1:5000/

the second dashboard:
http://127.0.0.1:5000/2

the third dashboard:
http://127.0.0.1:5000/3



