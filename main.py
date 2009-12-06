import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import models
import urllib

class ImageHandler(webapp.RequestHandler): 
  def get(self,unique_id):
    query = db.GqlQuery('SELECT * FROM ImageData WHERE unique_id = :1', unique_id)
    list = query.fetch(1)

    if len(list) == 0:
      self.error(404)
      return
      
    image = list[0]    
    parts = image.filename.split('.')
    extension = parts[len(parts)-1]
    
    if extension == 'png':
      self.response.headers['Content-Type'] = 'image/png'
    if extension == 'jpeg' or extension == 'jpg':
      self.response.headers['Content-Type'] = 'image/jpeg'
    if extension == 'gif':
      self.response.headers['Content-Type'] = 'image/gif'
    
    self.response.headers['Cache-Control'] = 'public, max-age=900000'
    self.response.headers.add_header("Expires", "Thu, 01 Dec 2014 16:00:00 GMT")
    self.response.out.write(image.data)


class MainHandler(webapp.RequestHandler):
  def get(self,path):
    self.response.out.write(template.render('index.html', {}))

def main():
  application = webapp.WSGIApplication([('/image/(.*)', ImageHandler),
                                        ('/(.*)', MainHandler)
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
