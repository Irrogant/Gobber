GOBBER

_________________________________________________________________________________________________________________________________________________________________


The application is created using Django 4.0.2 and Python 3.8.10 in Linux. It can be launched in the terminal by locating the “Gobber” folder and running the command
	python3 manage.py runserver.
Open up a browser window (preferably Chrome) and go to 
	http://localhost:8000/gobber/.

The application Gobber consists of various security flaws based on the 2021 OWASP Top Ten list (https://owasp.org/www-project-top-ten/). This application was implemented in a secure manner to begin with, and reverse-engineered to make it flawed and insecure. Therefore, some flaws overlap and extend over multiple lines of code, and cannot be pinpointed down to a single line. To ease the understanding of the flaws and fixes, there are sections of code marked as “fixes” that can be uncommented for the application to execute securely, and sections marked as “flaws” that can be commented out if the corresponding fixes has been uncommented.

_________________________________________________________________________________________________________________________________________________________________

FLAW 1:
This is a flaw of type A01, broken access control. Gobber allows for bypassing access control checks by modifying the URL.
Four fix-sections can be found at line #33, #62, #71, #135 in views.py.

To not allow any disguised gremlins or gold thieves inside, the goblins have a guardian at the cave entrance. The guardian will only let visitors inside if they know the secret password. However, there is a big flaw in this security, as the visitor easily can jump past the guardian and access the chat by typing the URL
	gobber/chats.

FIX:
One way to fix this flaw is by using sessions. A session key can be initialized in both the access and chats view, to check if the visitor is allowed inside. If they have been at the access view and have entered the correct password their session key has been set to True:
	request.session['access'] = True.
This allows them access to the chats view. If the session key is set to False, they will be redirected to the access view and have to enter the right password in order to update the session key.

_________________________________________________________________________________________________________________________________________________________________


FLAW 2:
This is a flaw of type A07, identification and authentication failures. Gobber permits brute force and other automated attacks.
Three fix-sections can be found at line #15, #39, #52 in views.py.

While the goblin guardian might look frightening, there is another flaw with his guarding. The current system allows for the visitor to try as many passwords as they want, at any rate they want. This allows for brute-force attacks and other trial-and-error password-guessing attempts.

FIX:
This flaw can also be fixed using sessions. By initializing a session counter, it can keep track of the amount of times a visitor has tried to enter a password and slow down their attempts to do so. In this example fix, the 
	time.sleep()
function is used to delay password guessing after three attempts. Furthermore, e.g., Captcha could be initialized to slow down and prevent automated attacks.

_________________________________________________________________________________________________________________________________________________________________


FLAW 3:
This is a flaw of type A03, injection. Gobber uses dynamic queries, and user-input-data is not sanitized.
The flaw-section can be found at line #80 in views.py and the fix-section at line #117 in the same file.

The application has a fully functional ModelForm setup to take user input and save it to a database. However, a goblin has messed up with the implementation by making the application run raw SQL queries that handle user input and insert it into the database. This not only prevents chatters from using certain special characters in their messages, such as apostrophes (‘), but also allows for SQL injections. For example, by typing 
	I am from the future, sell all gold!','2033-11-13 11:13:13') --
in the chat box, a goblin can claim to be a time traveler. And this is a rather innocent example compared to more damaging injection attacks.

FIX:
This flaw can be easily fixed by not allowing raw SQL queries, and especially not handling user input in them. It could be possible to clean the input data before passing it on the query, but the ModelForm setup which is already in use allows for an easy way to save the form input directly to the database by typing
	form.save().
A much safer way to handle user input, as the data is treated as strings and cannot manipulate the query.

_________________________________________________________________________________________________________________________________________________________________


FLAW 4:
This is a flaw of type A04, insecure design. Gobber have easily accessible and insufficiently protected credentials.
The flaw-section can be found at line #93 in settings.py.

Every goblin cave needs a goblin administrator. The Gobber administrator account is a big security risk, as it uses default login details. Any visitor can easily sign into it by going to 
	gobber/admin
and entering the default username and password, “admin” and “admin”.  The visitor gets access to all chat messages and can modify them. They are also able to see and modify the password required to enter the chat cave.

FIX:
The easiest fix would be to change the default password and username to more complex ones. For example, in the terminal:
	python3 manage.py changepassword admin.
The latest versions of Django offer password validation when initialized, to prevent easily breachable passwords from being used  — but that seems to have been commented out in the settings, perhaps by a disguised gremling.

_________________________________________________________________________________________________________________________________________________________________


FLAW 5:
This is a flaw of type A05, security misconfiguration. Gobber fails in security hardening by not handling errors properly and displaying sensitive information to users.
Three fix-sections can be found at line #27 in settings.py, line #25, #95 in views.py.

The goblins like debugging so much they forgot to turn it off when publishing the application. Having debugging turned on displays error messages which may contain sensitive information that can be seen by visitors. Apart from debugging settings, there are also some flaws with error-handling inside the code. User input is not sanitized or validated before being handled in the code, and executed database queries may cause errors which should be taken into account..

FIX:
The first of the issues have a rather easy fix: turn debugging off. Error handling on the other hand, requires a bit more thoughtfulness. Whenever executing code that could generate errors, try and excepts should be used for customizing error messages and making the overall error-handling easier. Another fixing would be to add 
	form.is.valid()
to make sure the user input fits the requirements and does not generate any errors. By understanding the causes behind errors not only makes it easier to prevent them, but also control them. This lays a much safer ground for any application.

_________________________________________________________________________________________________________________________________________________________________