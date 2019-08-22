import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView


from todo.models import ToDo


class UpdateToDo(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        if not request.body:
            todo_list = ToDo.objects.filter(user=user)
            results = [ob.as_json() for ob in todo_list]
            return HttpResponse(json.dumps(results), content_type="application/json")

        data = json.loads(request.body)

        for todo in data:
            new_status = 'ok'
            if todo['status'] == 'archived':
                new_status = todo['status']

            if todo['status'] == "created":
                ToDo.objects.get_or_create(user=user, task=todo['task'], description=todo['description'],
                                           deadline=todo['deadline'], is_done=todo['is_done'], status=new_status)
            elif todo['status'] == "updated":
                if todo.objects.filter(id=todo['global_id']).exists():
                    todo.objects.filter(id=todo['global_id']).update(task=todo['task'], description=todo['description'],
                                                                     deadline=todo['deadline'], is_done=todo['is_done'],
                                                                     status=new_status)
                else:
                    ToDo.objects.get_or_create(user=user, task=todo['task'], description=todo['description'],
                                               deadline=todo['deadline'], is_done=todo['is_done'], status=new_status)
            elif todo['status'] == "deleted":
                if ToDo.objects.filter(id=todo['global_id']).exists():
                    ToDo.objects.get(id=todo['global_id']).delete()

        todo_list_to_send = ToDo.objects.filter(user=user)
        results = [ob.as_json() for ob in todo_list_to_send]
        return HttpResponse(json.dumps(results), content_type="application/json")
