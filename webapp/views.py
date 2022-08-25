from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employees
from .serializers import EmployeesSerializer
from django.http import HttpResponse
from django.db.models import Q

def home(request):
    return HttpResponse("<h1>This is Django Restful api</h1><br><p>add '/employees to the url to see data</p>")

class EmployeesListAPIView(APIView):    

    def get(self, request):
        allEmployees = Employees.objects.all()
        query = None
        params = [(key, value) for key, value in request.query_params.items()]
        or_ind = []
        for ind, pair in enumerate(params):
            key, value = pair
            if "|" in value:
                a = value.split("|")
                value = a[0]
                for Ind, i in enumerate(a[1:]):
                    or_ind.append(ind+Ind+1)
                    b = i.split("=")
                    params.insert(ind+1, (b[0], b[1]))


            if (key == "orderby"):
                if not query:
                    allEmployees = allEmployees.order_by(value)
                else: 
                    allEmployees = allEmployees.filter(query).order_by(value)
                continue

            
            notequal = False
            if "!" in key:
                key = key[:-1]
                notequal = True
            
            if (("%" in value) or ("^" in value)):
                if ("^" in value):
                    if value[0] == "^":
                        value = value[1:]
                        key += "__startswith"
                    else:
                        value = value[:-1]
                        key += "__endswith"
                else:
                    value = value[1:]
                    key += "__contains"

            elif (("<" in key) or (">" in key)):
                if ("<" in key):
                    ind = key.index("<")
                    if value == "":
                        value = key[ind+1:]
                        key = key[:ind] + "__lt"
                    else:
                        key = key[:ind] + "__lte"
                else:
                    ind = key.index(">")
                    if value == "":
                        value = key[ind+1:]
                        key = key[:ind] + "__gt"
                    else:
                        key = key[:ind] + "__gte"

            if (value == "null"):
                key += "__isnull"
                value = True

            q = Q(**{key:value})

            if notequal:
                q = ~q
            
            if not query:
                query = q
            else:
                if ind in or_ind:
                    query = query | q
                else:
                    query = query & q
            
        if query:
            allEmployees = allEmployees.filter(query)
        print(or_ind)
        serializer = EmployeesSerializer(allEmployees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "firstname": request.data.get("firstname"),
            "lastname": request.data.get("lastname"),
            "emp_id": request.data.get("emp_id"),
        }
        serializer = EmployeesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Employees.objects.get(pk=id)
        except:
            return None

    def dataDoesNotExist(self):
        return Response(
                {"res": "employee does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id, *args, **kwargs):
        employee = self.get_object(id=id)
        if not employee:
            return self.dataDoesNotExist()
        serializer = EmployeesSerializer(instance=employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        employee = self.get_object(id=id)
        if not employee:
            return self.dataDoesNotExist()
        serializer = EmployeesSerializer(instance=employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        employee = self.get_object(id=id)
        if not employee:
            return self.dataDoesNotExist()
        employee.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

