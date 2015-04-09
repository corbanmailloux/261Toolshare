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

##Dislaimer
This project was made for a class and should not be trusted as a real system.

##Installation
In order to run ToolShare you must have Python 3 with Django 1.5 (For help installing Django, visit the [Django Docs](https://docs.djangoproject.com/en/1.5/intro/install/)). Please run the `runserver.bat` file in order to launch the server. 
Open your web browser (Google Chrome recommended) to the URL [http://localhost/](http://localhost/). 
To kill the server, press <kbd>Ctrl</kbd>+<kbd>Break</kbd>.

NOTE:
If you use want to use the command line to run the django test server instead of a batch file, then navigate to the 'project261' folder and run: 

```
python manage.py runserver 80 --insecure
```


##Testing Instructions
A fairly empty test database is located at `/Test DB/django.db`. 

To run unit tests navigate to `/project261` and in command line run: 

```
python manage.py test toolshare
```

##Admin View
To conduct administrative tasks such as approving the creation of a new Sharezone or user, go to the standard login page and login with the following credentials:
- Username: `admin`
- Password: `admin`

Then click the "Admin Panel" button to the upper right of your ToolShare page.


##Known Bugs and Disclaimers
No bugs are known at this time. Please submit issues and/or pull requests for any bugs found during your ToolShare experience.
