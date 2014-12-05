import logging
logging.basicConfig(level=logging.DEBUG)
import json

from webtest import TestApp #Docs: http://webtest.pythonpaste.org/en/latest/
from auth import simpleauth


class test_auth:
           
    @classmethod
    def setUpClass(self):
        self.app = TestApp(simpleauth.app)

    @classmethod
    def tearDownClass(self):
        pass

    def test_users(self):

        headers = [('Content-type', 'application/json')]
        payload = { "first_name": "Joe",
		    "last_name": "Smith",
		    "userid": "jsmith",
		    "groups": ["admins", "users"] }


        #GET (test for error - user doesn't exist yet)
        get_user = self.app.get('/users/%s' % payload.get('userid'), status=404)
        user = get_user.json
        assert user.get('error')

        #POST
        create_user = self.app.post('/users/%s' % payload.get('userid'),
                                  content_type='application/json',
                                  headers=headers,
                                  params=json.dumps(payload))
        
        user = create_user.json.get('user') if create_user.json else None

        assert user
        assert user.get('userid') == payload.get('userid')

        #GET
        get_user = self.app.get('/users/%s' % payload.get('userid'))
        user = get_user.json
        assert user
        assert sorted(user.get('groups')) == sorted(payload.get('groups'))
        
        #PUT
        payload['groups'] = ['admins', 'users', 'new']
        update_user = self.app.put('/users/%s' % payload.get('userid'),
                                  content_type='application/json',
                                  headers=headers,
                                  params=json.dumps(payload))

        get_user = self.app.get('/users/%s' % payload.get('userid'))
        user = get_user.json
        assert user
        assert sorted(user.get('groups')) == sorted(payload.get('groups'))
        
        #DELETE
        delete_user = self.app.delete('/users/%s' % payload.get('userid'))
        assert delete_user.status == '200 OK'

    
    def test_groups(self):
        headers = [('Content-type', 'application/json')]
        payload = { "first_name": "Joe",
            "last_name": "Smith",
            "userid": "jsmith2",
            "groups": ["admins", "users"] }

        create_user = self.app.post('/users/%s' % payload.get('userid'),
                              content_type='application/json',
                              headers=headers,
                              params=json.dumps(payload))

        user = create_user.json.get('user') if create_user.json else None

        assert user
        assert user.get('userid') == payload.get('userid')

        for group in payload.get('groups'):
            resp = self.app.get('/groups/%s' % group)
            group_resp = resp.json
            assert group_resp
            assert group in group_resp

        self.app.delete('/groups/admins')
        self.app.get('/groups/admins', status=404)
        self.app.post('/groups/admins')
        self.app.get('/groups/admins', status=200)

        group_payload = {"userids": [payload.get('userid')]}
        update_groups = self.app.put('/groups/admins',
                                                     content_type='application/json',
                                                      headers=headers,
                                                      params=json.dumps(group_payload))
        assert update_groups.json.get('status') == 200

        get_user = self.app.get('/users/%s' % payload.get('userid'))
        user = get_user.json
        assert 'admins' in user.get('groups')
        delete_user = self.app.delete('/users/%s' % payload.get('userid'))
