#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oauth, logging
from google.appengine.ext import webapp,db
from google.appengine.ext.webapp import util
from django.utils import simplejson

class TwitterUser(db.Model):
    id = db.IntegerProperty()
    username = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    picture = db.LinkProperty()
    token = db.StringProperty(required=True)
    secret = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    service = db.StringProperty(required=True)

class TwitterHandler(webapp.RequestHandler):

    _application_key = "FiYXwjgiCMelSLCZgvT5Rw" 
    _application_secret = "7rvRhpWz2UWD8sSe8wt3rNDTehP6og6w6cZOTgRCc"  

    def get(self, mode=""):
        try:
            self._get(mode)
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            self.response.out.write("Twitter is over capacity.")
            
    def _get(self,mode):
        logging.debug(mode)
        if mode == "join":
            client = self._get_client("%s/script/verify_join")
            return self.redirect(client.get_authorization_url())

        if mode == "quit":
            client = self._get_client("%s/script/verify_quit")
            return self.redirect(client.get_authorization_url())

        if mode == "verify_join":
            client = self._get_client("%s/script/verify_join")
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
            twitter_user = TwitterUser.all().filter('id =', user_info['id']).get()
            if not twitter_user:
                twitter_user = TwitterUser(**user_info)
                twitter_user.put()
                logging.debug(twitter_user.name)
            return self.redirect('%s/registration.html' % self.request.host_url)

        if mode == "verify_quit":
            client = self._get_client("%s/script/verify_quit")
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
            twitter_user = TwitterUser.all().filter('id =', user_info['id']).get()
            if twitter_user:
                twitter_user.delete()
            return self.redirect('%s/registration.html' % self.request.host_url)
      
    def _get_client(self,url=""):
        callback_url = url % self.request.host_url
        logging.debug(oauth)
        
        return oauth.TwitterClient(self._application_key, self._application_secret, 
                                   callback_url)
          
class Api(webapp.RequestHandler):
    def get(self, mode=""):
        
        callback =  self.request.get('callback')
        logging.debug(callback)

        results = []
        if mode == 'entrant':
            for data in TwitterUser.all().order('date'):
                results.append({
                    'id' : data.id,
                    'username' : data.username,
                    'name' : data.name,
                    'picture' : data.picture
                    })
        self.response.content_type = 'application/json'
        results = {'result' : results}
        if callback :
            self.response.out.write("%s(%s)" % (callback,simplejson.dumps(results, ensure_ascii=False)))
        else :
            self.response.out.write("%s" % simplejson.dumps(results, ensure_ascii=False))
        
def main():
    application = webapp.WSGIApplication([(r'/script/api/(.*)',Api),
                                          ('/script/(.*)', TwitterHandler)],
                                         debug=True)
    logging.getLogger().setLevel(logging.DEBUG)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
