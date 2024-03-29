# cyber-project

LINK: https://github.com/jusmari/cyber-project

The project should start with basic Django installation. Navigate to the directory and command “python manage.py runserver”. Then navigate in your browser to the URL http://localhost:8000/app/. The database should get initiated with testing data.

The app does not allow registering, so log in with
Username: GoodSpy
Password: GoodSpyPassword

FLAW 1:
https://github.com/jusmari/cyber-project/blob/318a5385b96ff4efb6ef7821ed5fb8d267b4e92c/cyber_site/views.py#L17

This is a flaw of Broken Access Control. https://owasp.org/Top10/A01_2021-Broken_Access_Control/

The app shows all super secret missions to all logged in spies. A logged in spy should see only their own missions and not others, but the access control is broken.

Fix the error by commenting row 17 and uncommenting row 19. Now the logged in spy should see only their secret missions.

The code now filters all missions by user id and shows current user only their missions. Since the user can not access to the backend a simple SQL filter should be secure.

FLAW 2:
https://github.com/jusmari/cyber-project/blob/318a5385b96ff4efb6ef7821ed5fb8d267b4e92c/cyber_site/views.py#L43

This is a flaw of Injection.
https://owasp.org/Top10/A03_2021-Injection/

The app uses raw SQL queries and does not sanitise user input at all. This flaw causes users to be able to create secret missions for other spies. Injections have other attack potential too. Malicious users can create great amounts of rows into the database with malicious information and cause denial of service. They can also potentially gain information from the database like exact software and version it is running on. It’s possible to affect the models and schema too, e.g. injecting SQL to drop tables or the whole database.

For example you can try to create a new mission with a description of

injected mission", 2, 2) –

This line of code makes the SQL query break by first completing the description string and then injecting the “2, 2)” part into the query. This causes a mission with Country_id=2, Spy_id=2 to be inserted in the database even when user GoodSpy’s id is not 2. The – double dash in the end makes the rest of the SQL query to be a comment and hence getting discarded by the SQL compiler. You can try this with different inputs and see what happens.

Fix the error by commenting out rows 43 - 46. Uncomment rows 49 and 50. Now the app creates new objects into the database with Django administered functions, which are sanitised. This allows us to insert user given information safely to the database.

FLAW 3:
https://github.com/jusmari/cyber-project/blob/318a5385b96ff4efb6ef7821ed5fb8d267b4e92c/cybersite/settings.py#L32

This is a flaw of Security Misconfiguration.
https://owasp.org/Top10/A05_2021-Security_Misconfiguration/

The app is always running in DEBUG mode, which leaks sensitive information to the users even in production. Sensitive debug data can be exploited in multiple ways. Django documentation states that DEBUG -mode should never be activated in production, but in default configuration sets it to always True. This is a real security flaw and should always be taken into account.

Fix the error by commenting row 32 and uncommenting row 35. Now the app reads DEBUG -mode from the system environment and defaults to False. In production there should not be a DEBUG -environment variable, so it’s not ever on.

FLAW 4:
https://github.com/jusmari/cyber-project/blob/318a5385b96ff4efb6ef7821ed5fb8d267b4e92c/cybersite/settings.py#L25

This is a flaw of Cryptographic Failures.
https://owasp.org/Top10/A02_2021-Cryptographic_Failures/

The app is using a too short and easily guessable security key. Also the key is pushed to version control, in this case GitHub. If the attacker is able to guess or immediately find your secret key, the Django in-built authentication system is greatly compromised. All of the cryptographic features are leaning on a safe and strong SECRET_KEY -variable.

SECRET_KEY is particularly used by Danjo in its built-in signer. Because in the web you can not trust anything that comes from the user, we need to be sure the data is valid and issued by the backend. Ensuring this is accomplished by the cryptographics backed up by the SECRET_KEY. More info can be read from https://docs.djangoproject.com/en/3.2/topics/signing/

Fix the flaw by commenting row 25 and uncommenting row 32. Now the app reads the SECRET_KEY from the system environment, which should contain a long and strong string key. Django documents have more information and best practices on the SECRET_KEY -variable https://docs.djangoproject.com/en/5.0/ref/settings/#secret-key

FLAW 5:
https://github.com/jusmari/cyber-project/blob/318a5385b96ff4efb6ef7821ed5fb8d267b4e92c/cybersite/settings.py#L39

This is a flaw of Security Logging and Monitoring Failures.
https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/

Here the developer has lazily allowed all hosts in the Django in-built ALLOWED_HOSTS -setting. Allowed hosts block connections from unknown hosts preventing many security issues, but also it enables Django to further log and monitor suspicious user operations. Getting requests from hosts not included in the ALLOWED_HOSTS -setting will raise a SuspiciousOperation error and trigger a log row for a security hazard. ALLOWED_HOSTS is primarily to combat the HTTP Host header attack and the additional security logging comes as a nice bonus.

To fix this flaw comment row 39 and uncomment row 40. This change makes the settings to read the production host url from the system environment variables, which makes it not a wild card in production. Note that when DEBUG is on ALLOWED_HOSTS automatically contains localhost and some local IP addresses, so this fix is visible only in production environments.
