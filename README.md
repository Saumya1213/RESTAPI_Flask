Running The Project

	1.) create a virtual environment and activate it: 
	
	    i) python -m venv env 
	
	    ii) .\env\Scripts\activate 
	
	
	
	2.) Inside the env install the below dependencies:
	
	    i) pip install flask
	
	    ii) pip install pyjwt
	
	    iii) pip install mysql-connector-python
	
	
	
	3.) In your virtual environment run the below command:
	
	    i) $env:PYTHONDONTWRITEBYTECODE=1;$env:FLASK_APP="app";$env:FLASK_ENV = "development";$env:FLASK_DEBUG=1;
	
	
	
	4.) To start the server run the below command:
	
	    i) flask run
