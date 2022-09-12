from rest_framework.response import Response
from .models import User,Address,Experience,Qualifications,Projects
from .serializers import UserSerializer
from rest_framework.views import APIView
from django.db import IntegrityError
from http import HTTPStatus
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
        

class UserView(APIView): 
    serializer_class = UserSerializer
       
    def post(self, request):        # Create an employee.
        try:
            empData = request.data
            print(f"empDate ==> {empData}")
            newAddress = Address.objects.create(houseNumber=empData['addressDetails']['houseNumber'],street = empData['addressDetails']['street'],
                                                    city = empData['addressDetails']['city'],state = empData['addressDetails']['state'])
            newAddress.save()
            print(f"Address ==> {newAddress}\n")
            # newExpAdd = Address.objects.create(houseNumber=empData['workExperience']['address']['houseNumber'],
                                            # street = empData['workExperience']['address']['street'],
                                                    # city = empData['workExperience']['address']['city'],
                                                    # state = empData['workExperience']['address']['state'] )
            # newExpAdd.save()
            # print(f"ExpAddress ==> {newExpAdd}\n")
            newExp = Experience.objects.create(companyName=empData['workExperience']['companyName'],
                                                    fromDate = ("-".join(empData['workExperience']['fromDate'].split("-")[::-1])),
                                                    toDate = ("-".join(empData['workExperience']['toDate'].split("-")[::-1])),
                                                    address=empData['workExperience']['address'] )
            newExp.save()
            print(f"exp ==> {newExp}\n")
            newQualifications = Qualifications.objects.create(qualificationName=empData["qualifications"]["qualificationName"],
                                                            fromDate = ("-".join(empData["qualifications"]['fromDate'].split("-")[::-1]) ),
                                                            toDate = ("-".join(empData["qualifications"]['toDate'].split("-")[::-1])),
                                                            percentage=empData["qualifications"]["percentage"])
            newQualifications.save()
            print(f"Qual ==> {newQualifications}\n")
            newProject = Projects.objects.create(title=empData['projects']['title'],
                                                description=empData['projects']['description'])
            newProject.save()
            print(f"Project ==> {newProject}\n")
            newEmpl = User.objects.create(name=empData['name'],email=empData['email'],age=empData['age'],
                                        gender=empData['gender'],phoneNumber=empData['phoneNumber'],photo =empData['photo'],
                                            addressDetails=newAddress, workExperience = newExp,
                                            qualificiations = newQualifications,projects = newProject)
            newEmpl.save()
            print(f"EMpl ==> {newEmpl}\n")
            serializer = UserSerializer(newEmpl)
            return Response({'status':200 , "message":"employee created successfully","regid": serializer.data['regid'],"success":True}) 
        except IntegrityError as e:
            return Response({'status':200 , "message":"employe already exist","success":False})
        except Exception as e:
            if e.status_code==400:
                return JsonResponse({'status':400 , "message":"invalid body request","success":False},status=HTTPStatus.BAD_REQUEST)
            elif e.status_code==500:
                return JsonResponse({'status':500 , "message":"employe deletion failed","success":False},status=HTTPStatus.INTERNAL_SERVER_ERROR)
            else:
                return JsonResponse({'status':200 , "message":"employe deletion failed","success":False},status=HTTPStatus.OK)
    
    def get(self, request):     # Get employee details.
        try:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({'status':200 , "message":"employee details not found","success":False},status=HTTPStatus.OK)
        
    def put(self,request, *args, **kwargs):
        try:
            data=request.data
            record = User.objects.get(regid=data['regid'])
            record.name = data['name']
            record.email = data['email']
            record.age = data['age']
            record.gender = data['gender']
            record.phoneNumber = data['phoneNumber'] 
            if record.addressDetails != None :
                record.addressDetails.houseNumber = data['addressDetails']['houseNumber']
                record.addressDetails.street = data['addressDetails']['street']
                record.addressDetails.city = data['addressDetails']['city']
                record.addressDetails.state = data['addressDetails']['state']
            if record.workExperience != None :
                record.workExperience.companyName = data['workExperience']['companyName']
                record.workExperience.fromDate = data['workExperience']['fromDate']
                record.workExperience.toDate = data['workExperience']['toDate']
                record.workExperience.address = data['workExperience']['address']
            if record.qualifications != None:
                record.qualifications.qualificationName = data['qualifications']['qualificationName']
                record.qualifications.fromDate = data['qualifications']['fromDate']
                record.qualifications.toDate = data['qualifications']['toDate']
                record.qualifications.percentage = data['qualifications']['percentage']
            if record.projects != None:
                record.projects.title = data['projects']['title']
                record.projects.description = data['projects']['description']
            record.photo = data['photo']
            record.save(update_fields=['name','email','age','gender','phoneNumber','addressDetails','workExperience','qualifications','projects','photo'])
            return JsonResponse({'status':200 , "message":"employee details updated successfully","success":False},status=HTTPStatus.OK)  
        except Exception as e:
            if e.status_code==400:
                return JsonResponse({'status':400 , "message":"invalid body request","success":False},status=HTTPStatus.BAD_REQUEST)
            elif e.status_code==500:
                return JsonResponse({'status':500 , "message":"employee updation failed","success":False},status=HTTPStatus.INTERNAL_SERVER_ERROR)
            else:
                return JsonResponse({'status':200 , "message":"employe details updation failed","success":False},status=HTTPStatus.OK)
 
    def delete(self,request):       # Delete a record of employee.
        try:
            data=request.data['regid']
            obj1=User.objects.get(pk=data)
            obj1.delete()
            return Response({'status':200 , 'message':"Deleted successfully"})
        except ObjectDoesNotExist as e:
            return Response({'status':200 , "message":"no employee found with this regid","success":False})
        except Exception as e:
            if e.status_code==400:
                return JsonResponse({'status':400 , "message":"invalid body request","success":False},status=HTTPStatus.BAD_REQUEST)
            elif e.status_code==500:
                return JsonResponse({'status':500 , "message":"employee deletion failed","success":False},status=HTTPStatus.INTERNAL_SERVER_ERROR)