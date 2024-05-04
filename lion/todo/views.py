from django.shortcuts import render
from .models import Todo
from .serializers import TodoSerializer, TodoListSerializer, PutTodoSerializer
#from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


#todo 전체 조회 및 생성
class TodoList(APIView):
    #전체 조회
    def get(self, request):
        #complete=False인 queryset 추출
        todos = Todo.objects.exclude(complete="True")
        serializer = TodoListSerializer(todos, many=True)
        return Response(serializer.data)

    #post 시 작성 항목을 제한하는 방법은 뭘까...
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#todo 상세 조회, 수정, 삭제
class TodoDetail(APIView):
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        todos = self.get_object(pk)
        serializer = TodoSerializer(todos)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        todos = self.get_object(pk)
        #complete 값을 적어도 수정되지 않게 PutTodoSerializer 이용(complete가 filed에서 제외)
        serializer = PutTodoSerializer(todos, data=request.data)

        if serializer.is_valid():
            serializer.save()
            #complete 출력을 위해 TodoSerializer 이용. 
            serializer = TodoSerializer(todos)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todos = self.get_object(pk)
        todos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#완료된 리스트 보여주기
class TodoDoneList(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete="True")
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

#complete 상태를 True로 변경
class Todo_True(APIView):
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        todos = self.get_object(pk)
        todos.complete='True'
        todos.save()
        serializer = TodoSerializer(todos)
        return Response(serializer.data)
