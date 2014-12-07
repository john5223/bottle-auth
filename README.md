bottle-auth
===========

First install requirements:

    pip install -r pip-requirements.txt


To run web application server:

    python auth/simpleauth.py


To test application:

    nose tests/ -v


Description: 

This project uses bottle.
This project uses dataset ( http://dataset.readthedocs.org/en/latest/quickstart.html )
    - Ability to query SQL like NoSQL! Awesome!
    - Automatically creates table schemas and adds additional columns as necessary. 
    - Ability to still query directly (of course). 

This project has the ability to use gevent for async requests.


P.S. 
This project only uses two tables. Users and groups. 
I could have used a membership table to hold user->group relationships, but why complicate something uncomplicated. :) 
