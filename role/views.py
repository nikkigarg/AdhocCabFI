from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from role.serializers import RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = RoleSerializer

    def list(self, request, *args, **kwargs):
        try:
            req_status = "success"
            code = status.HTTP_200_OK
            msg = "Roles data fetched successfully."
            role = Group.objects.all()
            serializer = RoleSerializer(role, many=True)
            data = serializer.data
        except Exception as e:
            print(e)
            req_status = "error"
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            msg = "Unable to fetch Roles data."
            data = {}
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def create(self, request):
        try:
            req_status = "error"
            msg = "Unable to create Role."
            data = {}
            code = status.HTTP_500_INTERNAL_SERVER_ERROR

            req_data = request.data
            permissions = req_data.get('permissions', {})

            permission_res = self.get_added_permissions_ids(permissions)
            permission_ids = permission_res['data']
            if permission_res['req_status'] == "success" and len(permission_ids) > 0:
                serializer = RoleSerializer(data=req_data)
                if serializer.is_valid():
                    role_obj = serializer.save()
                    role_obj.permissions.add(*permission_ids)
                    req_status = "success"
                    code = status.HTTP_200_OK
                    msg = "Role created successfully."
                    data = {'role_id': role_obj.id, 'name': role_obj.name}
                else:
                    code = status.HTTP_400_BAD_REQUEST
                    msg = "Bad Request." + str(serializer.errors)
            else:
                code = status.HTTP_400_BAD_REQUEST
                msg = "Bad Request." + "Add atleast one permission to create group."
        except Exception as e:
            # msg = str(e)
            print(str(e))
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def destroy(self, request, pk=None):
        try:
            req_status = "success"
            code = status.HTTP_204_NO_CONTENT
            msg = "Role deleted successfully."
            role = Group.objects.get(id=pk)
            role.delete()
        except Exception as e:
            print(e, "<<<<<<<<")
            req_status = "error"
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            msg = "Error in deleting Role." + str(e)
        return Response({"code": code, "req_status": req_status, "data": {}, "msg": msg})

    def retrieve(self, request, pk=None):
        try:
            req_status = "success"
            code = status.HTTP_302_FOUND
            msg = "Role data fetched successfully."

            role = get_object_or_404(Group, pk=pk)
            serializer = RoleSerializer(role)
            data = serializer.data
            # if want to send permission ids in get response of group
            data.update({"permission_ids":role.permissions.values_list('id', flat=True)})
        except Exception as e:
            print(e)
            req_status = "error"
            code = status.HTTP_404_NOT_FOUND
            msg = "Unable to fetch Role data." + str(e)
            data = {}
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    def update(self, request, pk=None):
        try:
            req_status = "error"
            msg = "Unable to update Role data."
            data = {}
            code = status.HTTP_500_INTERNAL_SERVER_ERROR

            req_data = request.data
            permissions = req_data.get('permissions', {})
            role = Group.objects.get(id=pk)
            permission_res = self.update_permissions(role, permissions)
            serializer = RoleSerializer(role, data=req_data)
            if permission_res['req_status'] == 'success':
                if serializer.is_valid():
                    role_obj = serializer.save()

                    req_status = "success"
                    code = status.HTTP_201_CREATED
                    msg = "Role data updated successfully." + permission_res['msg']
                    data = {'role_id': role_obj.id, 'name': role_obj.name}
                else:
                    code = status.HTTP_400_BAD_REQUEST
                    msg = "Bad Request." + str(serializer.errors)
            else:
                code = status.HTTP_400_BAD_REQUEST
                msg = "Bad Request." + permission_res['msg']
        except Exception as e:
            # msg = str(e)
            print(str(e))
        return Response({"code": code, "req_status": req_status, "data": data, "msg": msg})

    @action(detail=False, url_path="all-permission")
    def get_all_permissions(self, request):
        try:
            req_status = "success"
            code = status.HTTP_200_OK
            msg = "All permission fetched successfully."
            permissions_dict = {}
            code_names = Permission.objects.values_list('codename', flat=True)
            for codename in code_names:
                permission = codename.split("_")
                if permission[1] not in permissions_dict:
                    permissions_dict[permission[1]] = {}
                permissions_dict[permission[1]][permission[0]] = False
        except Exception as e:
            print(e)
            req_status = "error"
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            msg = "Error in fetching permissions."
        return Response({"code": code, "req_status": req_status, "data": permissions_dict, "msg": msg})

    def get_added_permissions_ids(self, permissions):
        try:
            req_status = "success"
            code_names = []
            added_permission_ids = []
            for app_label, permission in permissions.items():
                for key, value in permission.items():
                    if value:
                        code_names.append(key + '_' + app_label)
            if len(code_names) > 0:
                added_permission_ids = Permission.objects.filter(codename__in=code_names).values_list('id', flat=True)
        except Exception as e:
            print(e)
            req_status = "error"
        return {"req_status": req_status, "data": added_permission_ids}

    def update_permissions(self, role_obj, permissions):
        try:
            req_status = "error"
            msg = "Error in updating Permission."
            permission_res = self.get_added_permissions_ids(permissions)
            new_ids = permission_res['data']
            if permission_res['req_status'] == "success" and len(new_ids) > 0:
                old_ids = role_obj.permissions.values_list('id', flat=True)
                all_ids = set(old_ids.union(new_ids))
                added_ids = all_ids - all_ids.intersection(old_ids)
                removed_ids = all_ids - all_ids.intersection(new_ids)
                # add and remove permission ids fro group
                role_obj.permissions.remove(*removed_ids)
                role_obj.permissions.add(*added_ids)
                req_status = "success"
                msg = "Updated Permissions successfully."
            else:
                msg = "Please select atleast one permission."
        except Exception as e:
            print(e)
            msg = str(e)
        return {"req_status": req_status, "msg": msg}
