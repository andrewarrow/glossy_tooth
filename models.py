from google.appengine.ext import db

class ImageData(db.Model):
  unique_id = db.StringProperty()
  filename = db.StringProperty()  
  data = db.BlobProperty()

class ImageMetaData(db.Model):
  unique_id = db.StringProperty()
  filename = db.StringProperty()
  width = db.IntegerProperty()
  height = db.IntegerProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
