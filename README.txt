  ________         ___               __    ___         __    _______     __ 
 /_  __/ /  ___   / _ )_______ ___ _/ /__ / _/__ ____ / /_  / ___/ /_ __/ / 
  / / / _ \/ -_) / _  / __/ -_) _ `/  '_// _/ _ `(_-</ __/ / /__/ / // / _ \
 /_/ /_//_/\__/ /____/_/  \__/\_,_/_/\_\/_/ \_,_/___/\__/  \___/_/\_,_/_.__/
============================================================================
                          \`.    ______          ________               
.--------------.___________) \  /_  __/__  ___  / / __/ /  ___ ________ 
|//////////////|___________[ ]   / / / _ \/ _ \/ /\ \/ _ \/ _ `/ __/ -_)
`--------------'           ) (  /_/  \___/\___/_/___/_//_/\_,_/_/  \__/
                           '-'

Installation:
In order to install ToolShare R2, please unzip the ToolShare.zip file. In order
to run R2 you must have Python 3 with Django 1.5 (For help installing Django, 
visit https://docs.djangoproject.com/en/1.5/intro/install/). In the unzipped 
folder, double-click the runserver.bat file in order to launch the server. Open
your web browser (Google Chrome recommended), and go to the URL “localhost”. 

NOTE: If you use want to use the command line to run the django test server 
instead of a batch file, then navigate to the ‘project261’ folder and run:
	`python manage.py runserver 80 --insecure`

Testing Instructions:
A fairly empty test database will be located in the top directory of the 
unzipped folder under /Test DB/. To run unit tests navigate to /project261 
and in command line run: 
	`python manage.py test toolshare`

Admin View:
To conduct administrative tasks such as approving the creation of a new 
Sharezone or user, go to the standard login page and login with the username 
“admin” and the default password “admin” (without quotes). Then click the 
“Admin Panel” button to the upper right of your ToolShare page.

Additional Files:
The following files will be in the same directory as this ReadMe:
Project Plan.doc
Test Plan Tracker.xlsx
Requirements - Toolshare.doc
Design.doc

Known Bugs and Disclaimers:
No bugs are known at this time. Please contact the team with a description of
any bugs found in your use of the ToolShare R2 experience.
