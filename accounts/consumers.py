from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

import json

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from accounts.models import User


class UserCountConsumer(WebsocketConsumer):
    def connect(self):
        print('Connected')
        self.token = {'token': self.scope['url_route']['kwargs']['token']}
        try:
            valid_data = VerifyJSONWebTokenSerializer().validate(self.token)
            self.user = valid_data['user']
            print(self.user)
            self.update_user_status(self.user, True)
        except:
            print('Expired')
        self.accept()

    def disconnect(self, close_code):
        print('Disconnect')
        print(self.user)
        self.update_user_status(self.user, False)

    def websocket_receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

# async def websocket_connect(self, event):
#     # Called when a new websocket connection is established
#     print("connected", event)
#     try:
#         print(self.scope['user'])
#     except:
#         print('Not happening')
#     user = Token.objects.get(key=self.scope['token']).user
#     self.update_user_status(user, True)
#
# async def websocket_receive(self, event):
#     # Called when a message is received from the websocket
#     # Method NOT used
#     print("received", event)
#
# async def websocket_disconnect(self, event):
#     # Called when a websocket is disconnected
#     print("disconnected", event)
#     user = self.scope['user']
#     self.update_user_status(user, False)
#
    def update_user_status(self, user, status):
        print(User.objects.get(pk=user.pk).is_active)
        User.objects.filter(pk=user.pk).update(is_admin=status)
        print(User.objects.get(pk=user.pk).is_active)
