CMS
===

Installation
------------
You should have Python2.7.x installed on your machine. 

Install mysqlclient from the .extra folder using:

    $ python -m ensurepip install .\.extra\whl\mysqlclient-1.3.13-cp27-cp27m-win32.whl

or	

    $ python -m ensurepip install .\.extra\whl\mysqlclient-1.3.13-cp27-cp27m-win_amd64.whl	

Install required packages from .extra\requirements.txt using:

    $ python -m ensurepip install -r .\.extra\requirements.txt
    
Install the required software:

    .\.extra\wkhtmltox-0.12.5-1.msvc2015-win64

Create a database named 'CMS'

Run the app using:

    $ python .\app.py
