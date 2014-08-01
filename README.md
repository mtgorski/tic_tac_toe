Tic-tac-toe
=========================
Play a game of tic-tac-toe against an AI that never loses. 

Application
-------------------------
[Play it here](http://matt-tac-toe.herokuapp.com/)

Heroku puts apps to sleep if they haven't been used in a while, so it might take longer than usual to load. 

Context
-------------------------
I started this project for a job application. Originally it started with a CLI but when the requirements changed I converted it to a Django application. Now I'm just working on it for fun. I'm sharing it because I wanted a public code sample that's more recent than some of my other ones. 

AI algorithm
-----------------------
The AI will never lose. This is achieved with the following algorithm. The strategy looks at all of the boards that could result from its next move and chooses one that is acceptable. A board is acceptable if any of the following hold:

1) The strategy wins or ties on that board.

2) It's the opponent's turn and any play the opponent can make leads to an acceptable board. 

3) It's the strategy's turn and the play made by it leads to an acceptable board. 

Future improvements
------------------------
I plan on adding at least one additional AI strategy and tracking win/loss/tie statistics for the various AI strategies. 

Using a local copy
----------------------
0. Clone the repo

1. setup and activate a virtual environment

2. pip install -r requirements.txt

3. export SECRET_KEY="somestring"

4. touch local\_settings.py

5. In local\_settings.py set the variables DEBUG and TEMPLATE\_DEBUG to True 

6. python manage.py runserver











