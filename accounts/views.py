from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from cryptography.fernet import Fernet
import json
from datetime import datetime
from accounts.controllers import UserController
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    controller = UserController()

    def list(self, request, *args, **kwargs):
        return self.controller.get_all_user(request)

    def create(self, request, *args, **kwargs):
        return self.controller.create_user(request)

    def destroy(self, request, pk=None, *args, **kwargs):
        return self.controller.delete_user(request, pk)

    def retrieve(self, request, pk=None, *args, **kwargs):
        return self.controller.get_user(request, pk)

    def update(self, request, pk=None, *args, **kwargs):
        return self.controller.update_user(request, pk)

    @action(detail=False, url_path="activate/(?P<id>[^/.]+)")
    def activate_account(self, request, id=None):
        try:
            res_status = "Error"
            msg = "Error in de-coding token.Please provide valid email id and details while creating account."
            # To get key
            file = open('accounts/key.key', 'rb')
            key = file.read()  # The key will be type bytes
            f = Fernet(key)
            file.close()
            # To de-crypt msg
            data = id.encode()
            decrypted = f.decrypt(data)
            decoded_data = decrypted.decode()
            decoded_data = json.loads(decoded_data)
            # To get user Data
            user = User.objects.get(email=decoded_data['email'], username=decoded_data['username'])
            if user:
                if decoded_data['expiry_time'] >= (datetime.now().strftime("%b %d %Y %H %M %S %p")):
                    msg = "Account activated successfully."
                    user.is_temp_active = True
                    user.save()
                    res_status = "success"
                else:
                    msg = "Link has expired.Please click on below link to get new activation link."
            else:
                msg = "Invalid user credential."
        except Exception as e:
            print(e, ">>>>>>>")


        # return Response({"hi": "hi", "msg": msg})
        decoded_data.update({"msg":msg, "res_status":res_status})
        return render(request, "activate.html", context=decoded_data)
