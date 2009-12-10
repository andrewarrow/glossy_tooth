import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext.webapp import template
import os
import sys
import models
import re
import uuid

class UploadHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('upload.html', {}))

class UploadPostHandler(webapp.RequestHandler):
  def post(self):
    lines = str(self.request).split("\n")
    for line in lines:
      if line.startswith('Content-Disposition') and line.find('filename=') > -1:
        filename = line.split(';')[2][11:-2]
    
    filename = self.request.get('filename')
    unique_id = str(uuid.uuid1())
    if self.request.get('unique_id'):
      unique_id = self.request.get('unique_id')
      
    filename = re.sub('[^a-z0-9\.]', '_', filename.lower())
    
    query = db.GqlQuery('SELECT * FROM ImageData WHERE unique_id = :1', unique_id)
    list = query.fetch(1)

    if len(list) == 0: 
      image = images.Image(self.request.get('img'))
      image_data = models.ImageData(data=self.request.get('img'),
                                    unique_id=unique_id,
                                    filename=filename)
      image_meta_data = models.ImageMetaData(filename=filename,
                                    unique_id=unique_id,
                                    width=image.width,
                                    height=image.height)
      image_data.put()
      image_meta_data.put()
      self.response.out.write(unique_id+"\n")
      self.response.out.write(str(image.width)+"\n")
      self.response.out.write(str(image.height))
    else:
      self.redirect('/upload', permanent=False)
    
def main():
  application = webapp.WSGIApplication([('/upload_post', UploadPostHandler),
                                        ('/upload', UploadHandler),
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
