
#we could import this from somewhere else - but no need
config = {'log_level': 'DEBUG', 'db_uri': 'sqlite:///:memory:' } 
log_level = config.get('log_level', 'DEBUG')

import logging 
logger = logging.getLogger(__name__)
logging.basicConfig(level=log_level)
logger.debug( config )

'''
bottle is awesome! And Gevent is awesome too!
Also faster than flask, especially when sessions aren't needed
'''

import bottle
app = bottle.app()

if log_level == 'DEBUG': 
    bottle.debug(True) #doesn't cache templates


'''
Bottle plugin for our DB connection
I thought dataset package looked cool so I made a plugin for bottle
http://dataset.readthedocs.org/en/latest/
'''
from services.dataset_plugin import DataSetPlugin
db_uri = config.get('db_uri')
dataset_plugin = DataSetPlugin(db_uri)
bottle.install(dataset_plugin)


#Where the magic happens
import controllers


def main():
    host = config.get('host') or '127.0.0.1'
    port = config.get('port') or '8085'
    #If gevent is installed use that as our server
    #server = 'gevent'
    #try: from gevent import monkey; monkey.patch_all()
    #except: server = 'wsgiref'
    server = 'wsgiref'
    kwargs = {'app': app, 'host': host, 'port': port,
                     'server': server,
                     'debug': True, 'reloader': False}
    bottle.run(**kwargs)


if __name__ == "__main__":
    main()
