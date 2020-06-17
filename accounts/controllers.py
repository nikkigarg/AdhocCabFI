from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, ProfileSerializer


class UserController:

    def get_all_user(self, request):
        try:
            req_status = "sucess"
            code = status.HTTP_200_OK
            msg = "Users data fetched successfully."
            users = User.objects.filter(is_active=True)
            serializer = UserSerializer(users, many=True)
            data = serializer.data
        except Exception as e:
            print(e)
            req_status = "error"
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            msg = "Unable to fetch Users data."
            data = {}
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def create_user(self, request):
        try:
            req_status = "error"
            msg = "Unable to create User account."
            data = {}
            code = status.HTTP_500_INTERNAL_SERVER_ERROR

            req_data = request.data
            profile_data = req_data.get('profile_data', {})
            serializer = UserSerializer(data=req_data)
            if serializer.is_valid():
                user_obj = serializer.save()
                profile_res = self.save_profile_data(user_obj.profile, profile_data)
                req_status = "sucess"
                code = status.HTTP_200_OK
                msg = "User account created successfully."
                data = {'user_id': user_obj.id, 'name': user_obj.first_name}
                if profile_res['req_status']:
                    data.update({'profile_data':profile_res['data']})
                msg += profile_res['msg']
            else:
                code = status.HTTP_400_BAD_REQUEST
                msg = "Bad Request." + str(serializer.errors)
        except Exception as e:
            # msg = str(e)
            print(str(e))
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def delete_user(self, request, pk=None):
        try:
            req_status = "sucess"
            code = status.HTTP_204_NO_CONTENT
            msg = "User data deleted successfully."
            user = User.objects.get(id=pk, is_active=True)
            user.is_active = False
            user.is_temp_active = False
            user.save()
        except Exception as e:
            print(e, "<<<<<<<<")
            req_status = "error"
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            msg = "Error in deleting User." + str(e)
        return Response({"code": code, "req_status": req_status, "data": {}, "msg": msg})

    def get_user(self, request, pk=None):
        try:
            req_status = "sucess"
            code = status.HTTP_302_FOUND
            msg = "User data fetched successfully."
            # queryset = User.objects.filter(is_active=True)
            user = get_object_or_404(User, pk=pk, is_active=True)
            serializer = UserSerializer(user)
            data = serializer.data
            if user.profile:
                profile_serializer = ProfileSerializer(user.profile)
                data.update({'profile_data': profile_serializer.data})
        except Exception as e:
            print(e)
            req_status = "error"
            code = status.HTTP_404_NOT_FOUND
            msg = "Unable to fetch User data." + str(e)
            data = {}
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def update_user(self, request, pk=None):
        try:
            req_status = "error"
            msg = "Unable to update User account."
            data = {}
            code = status.HTTP_500_INTERNAL_SERVER_ERROR

            req_data = request.data
            profile_data = req_data.get('profile_data', {})
            user = User.objects.get(id=pk, is_active=True)
            serializer = UserSerializer(user, data=req_data)
            if serializer.is_valid():
                user_obj = serializer.save(updated_on=datetime.now())

                profile_res = self.save_profile_data(user_obj.profile, profile_data)
                req_status = "sucess"
                code = status.HTTP_201_CREATED
                msg = "User account updated successfully."
                data = {'user_id': user_obj.id, 'name': user_obj.first_name}
                if profile_res['req_status']:
                    data.update({'profile_data':profile_res['data']})
                msg += profile_res['msg']
            else:
                code = status.HTTP_400_BAD_REQUEST
                msg = "Bad Request." + str(serializer.errors)
        except Exception as e:
            # msg = str(e)
            print(str(e))
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def save_profile_data(self, profile_instance, profile_data):
        try:
            req_status = "error"
            msg = "Error in saving User Profile data."
            data = {}
            serializer = ProfileSerializer(profile_instance, data=profile_data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                msg = "User Profile data saved successfully."
                req_status = "sucess"
        except Exception as e:
            print(e)

        return {"req_status": req_status, "data": data, "msg": msg}
