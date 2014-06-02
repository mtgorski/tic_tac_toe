Tic-tac-toe
=========================
Play a game of tic-tac-toe against an AI that never loses. 

Context
-------------------------
I started this project for a job application. Before I submitted it, they changed their requirements. I originally wrote it with a CLI and that's the version of the project that's public. But now I'm converting it to a web app (with either Django or Google App Engine) per the requirements. I'm sharing it becuase I wanted a public code sample that's more recent than some of my other ones. 

This is the first project I've done with automated unit testing. I learned and experimented with unit test organization during the course of the project. I settled on the following test naming convention. 

-Source code: src/module_name.py. 

-Test code: src/tests/test_module_name.py. 

-Use one TestCase class per function or method under test. 

-If a function does_thing is under test name the class FunctionNameFunction. 

-If does_thing method of the class Name is under test name the class DoesThingMethodNameClass. 

-Each test method must start with test_ to use the unittest framework. 

-Each test method should end with a description of the circumstance under test and the expected result. For example, 
OnTwoIntegersReturnsNone. 

The naming convention ensures that all pertinent information is displayed when the tests are run. Unittest output will be:
test_OnTwoIntegersReturnsNone (test_module_name.DoesThingMethodNameClass). Thus, you immediately know which function/method was tested, the module in which it's found, the class of which it's a method (if relevant), and the test which passed/failed. 

AI algorithm
-----------------------
The AI will never lose. This is achieved with the following algorithm. The strategy looks at all of the boards that could result from its next move and chooses one that is acceptable. A board is acceptable if:
1) The strategy wins or ties on that board.
2) It's the opponent's turn and any play the opponent can make leads to an acceptable board. 
3) It's the strategy's turn and the play made by it leads to an acceptable board. 

To Use
----------------------
After cloning the respository run src/main.py with Python 2.7. 
