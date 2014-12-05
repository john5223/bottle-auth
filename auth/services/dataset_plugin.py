import logging
logger = logging.getLogger(__name__)

import dataset
import inspect
from bottle import HTTPError


class DataSetPlugin(object):
    name = 'dataset'
    api = 2

    def __init__(self, db_uri=None, autocommit=True, dictrows=True,
                 keyword='db'):
         self.db = None
         self.db_uri = db_uri or 'sqlite:///:memory:'
         self.autocommit = autocommit
         self.dictrows = dictrows
         self.keyword = keyword

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, DataSetPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another dataset plugin with "\
                "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context.config.get('dataset') or {}
        db_uri = conf.get('dbfile', self.db_uri)
        autocommit = conf.get('autocommit', self.autocommit)
        dictrows = conf.get('dictrows', self.dictrows)
        keyword = conf.get('keyword', self.keyword)
        # Test if the original callback accepts a 'db' keyword.
        # Ignore it if it does not need a database handle.
        args = inspect.getargspec(context.callback)[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            # Connect to the database
            if not self.db:
                self.db = dataset.connect(db_uri)
            kwargs[keyword] = self.db
            try:
                rv = callback(*args, **kwargs)
                if autocommit:
                    pass
            except Exception, e:
                #db.rollback()
                raise e
                raise HTTPError(500, "Database Error", e)
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper

