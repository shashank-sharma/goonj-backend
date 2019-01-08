from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

import json

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from accounts.models import User


class UserCountConsumer(WebsocketConsumer):
    def connect(self):
        print('Connected')
        self.user = ''
        self.token = ''
        try:
            self.token = {'token': self.scope['url_route']['kwargs']['token']}
            valid_data = VerifyJSONWebTokenSerializer().validate(self.token)
            self.user = valid_data['user']
            print(self.user)
            self.update_user_status(self.user, True)
            self.accept()
        except:
            print('Expired')
            self.close()

    def disconnect(self, close_code):
        print('Disconnect')
        if self.user:
            self.update_user_status(self.user, False)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def update_user_status(self, user, status):
        User.objects.filter(pk=user.pk).update(is_online=status)
