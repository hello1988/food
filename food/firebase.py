# encoding=utf8
import pyrebase
import datetime
import time

from django.conf import settings

class Firebase():

    def datetime_timestamp(self):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)

    firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
    storage = firebase.storage()
    db = firebase.database()

    def uploadImg(self, event, imagePath, imgName):
        line_id = event.source.sender_id
        firebase_folder = 'food'
        return self.uploadImgWithToken(firebase_folder, line_id, imagePath, imgName)

    def uploadImgWithToken(self, firebase_folder, line_id, imagePath, imgName ):
        timestamp = self.datetime_timestamp()

        # imagePathForFirebase = firebase_folder + userToken + str(timestamp) + imgName
        imagePathForFirebase = '{}/{}/{}'.format( firebase_folder, line_id, imgName)
        saveImgStatusJson = self.storage.child(imagePathForFirebase).put(imagePath)
        urlToken =  saveImgStatusJson['downloadTokens']
        # url = self.storage.child("userImages/" + imgName).get_url()
        imageUrl = self.storage.child(imagePathForFirebase).get_url(urlToken)
        # https://firebasestorage.googleapis.com/v0/b/storage-url.appspot.com/o/images%2Fexample.jpg?alt=media

        return imageUrl