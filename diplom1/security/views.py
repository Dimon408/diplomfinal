from django.http import HttpResponse
from datetime import date
from datetime import date 
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .forms import Fio, Search_client, WorkerForm, Enter_error, UserRegistrationForm
from .models import Client_Time, Worker, Error
from django.contrib.auth.models import User
import timedelta
import datetime
from datetime import datetime,timedelta, date, time
from PIL import Image
import face_recognition
import sys
from django.views.generic import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


import matplotlib.pyplot as plt

url_host='http://127.0.0.1:8000'

def index(request):
    return HttpResponse("Привет мир!!!!!!")


def main(request):
    if not request.user.is_authenticated:
        return redirect(url_host+'/accounts/login/')
    user = get_object_or_404(User, username = request.user.username)
    #print('aaa'+str(user.is_staff))
    if user.is_staff==True:
        return render(request, "security/main.html")
    #elif user.is_staff==False:
    #    return render(request, "registration/login.html")
    else:
        worker = get_object_or_404(Worker, user=user)
        if worker.security==True:
            return render(request, "security/main_w.html")
        else:
            return render(request, "security/main_c.html")
        


    
    

   
    

def client_enter(request):
        if not request.user.is_authenticated:
            return redirect(url_host+'/accounts/login/')
        print('start')
        if request.method=="POST":
            print('post1')
            Client_Time1=Client_Time()
            print('post2')
            form = Fio(request.POST)
            print('post3')
            if form.is_valid():
                print('post4')
                print('Форма правильная')
                print(form.cleaned_data['fio_client'])
                Client_Time1.fio_client=form.cleaned_data['fio_client']

                print(form.cleaned_data['gender'])
                if(form.cleaned_data['gender']=='Женский'):
                    Client_Time1.gender=1
                else:
                    Client_Time1.gender=0
                

                print(form.cleaned_data['passport_number_client'])
                Client_Time1.passport_number_client=form.cleaned_data['passport_number_client']

                print(form.cleaned_data['date_of_birthday_client'])
                Client_Time1.date_of_birthday_client=form.cleaned_data['date_of_birthday_client']

                print(form.cleaned_data['phone_number_client'])
                Client_Time1.phone_number_client=form.cleaned_data['phone_number_client']

                print(form.cleaned_data['client_type'])
                if form.cleaned_data['client_type']=='Постоянный':
                    Client_Time1.client_type=0
                elif form.cleaned_data['client_type']=='Временный':
                    Client_Time1.client_type=1
                elif form.cleaned_data['client_type']=='Одноразовый':
                    Client_Time1.client_type=2
                Client_Time1.link_photo1_client = request.FILES.get('myfile1')#request.getFILES['myfile1'] 
                print(Client_Time1.link_photo1_client)
                all_clients=Client_Time.objects.all()   
                Client_Time1.id_client=len(all_clients)+1
                Client_Time1.save()

                print(Client_Time1)

                user = get_object_or_404(User, username = request.user.username)
                if user.is_staff!=True:
                    worker = get_object_or_404(Worker, user=user)
                else:
                    return render(request, "security/client_enter.html", {'form':form})
                if worker.security!=True:
                    return render(request, "security/main_c.html")
                else:
                    return render(request, "security/client_enter_w.html", {'form':form})
        else:
            print('get')
            form=Fio()
            user = get_object_or_404(User, username = request.user.username)
            if user.is_staff!=True:
                worker = get_object_or_404(Worker, user=user)
            else:
                return render(request, "security/client_enter.html", {'form':form})
            if worker.security!=True:
                return render(request, "security/main_c.html")
            else:
                return render(request, "security/client_enter_w.html", {'form':form})
    
    
def search_client(request):
    if not request.user.is_authenticated:
        return redirect(url_host+'/accounts/login/')
    print('1')
    if request.method=="POST":
        print('post')
        form=Search_client(request.POST)
        print('2')
        all_clients=set(Client_Time.objects.all())

        if request.POST.get("fio_client")!='':
            fio_filter=request.POST.get("fio_client")
            fio_filtered_clients=set(Client_Time.objects.filter(fio_client = fio_filter))
            all_clients.intersection_update(fio_filtered_clients)
          
        if request.POST.get('gender')!='':
            gender_filter=request.POST.get('gender')
            if ( gender_filter=="Мужской"):
                gender_filter=0
            else:
                gender_filter=1
            gender_filtered_clients=set(Client_Time.objects.filter(gender = gender_filter))
            print(gender_filtered_clients)
            print(all_clients)
            all_clients.intersection_update(gender_filtered_clients)

        if request.POST.get('passport_number_client')!='':
            passport_number_filter=request.POST.get('passport_number_client')
            passport_number_filtered_clients=set(Client_Time.objects.filter(passport_number_client = passport_number_filter))
            all_clients.intersection_update(passport_number_filtered_clients)

        if request.POST.get('age')!='':
            age_filter=request.POST.get('age')
            age_min=age_filter.split('-')[0]
            age_max=age_filter.split('-')[1]
            age_min_date=datetime.now() - timedelta(days=int(age_min)*365)
            age_max_date=datetime.now() - timedelta(days=int(age_max)*365)
            age_min_filtered_clients=set(Client_Time.objects.filter(date_of_birthday_client__lte = age_min_date))
            age_max_filtered_clients=set(Client_Time.objects.filter(date_of_birthday_client__gte = age_max_date))
            all_clients.intersection_update(age_min_filtered_clients)
            all_clients.intersection_update(age_max_filtered_clients)
                
        if request.POST.get('phone_number_client')!='':
            phone_filter=request.POST.get('phone_number_client')
            phone_filtered_clients=list(Client_Time.objects.filter(phone_number_client = phone_filter))
            all_clients.intersection_update(phone_filtered_clients)
        output=[]

        if all_clients=={}:
            output={}
        else:
            if request.FILES.get('myfile1')!=None:
                app_client=Client_Time()
                print(request.FILES.get('myfile1'))
                print(request.FILES.get('myfile1'))
                app_client.link_photo1_client = request.FILES.get('myfile1')
                known_image = face_recognition.load_image_file(app_client.link_photo1_client)
                print(known_image)
                for client in all_clients:
                    unknown_image = face_recognition.load_image_file(client.link_photo1_client)
                    print(unknown_image)
                    baixiaona_encoding = face_recognition.face_encodings(known_image)[0]
                    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                    results = face_recognition.compare_faces([baixiaona_encoding], unknown_encoding)
             
                    if results[0] == True:
                        output.append(client)
            else:
                output=all_clients

            
        context={
                'result_rearch' : output
                }
        
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, 'security/search_client.html', context=context)
        if worker.security!=True:
            return render(request, "security/search_client_c.html", context=context)
        else:
            return render(request, 'security/search_client_w.html', context=context)
    else:
        print('get')
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, 'security/search_client.html')
        if worker.security!=True:
            return render(request, "security/search_client_c.html")
        else:
            return render(request, 'security/search_client_w.html')
    

    
def worker_enter(request):
    if not request.user.is_authenticated:
        return redirect(url_host+'/accounts/login/')
    print('start')
    if request.method=="POST":
        print('post1')
        New_worker=Worker()
        print('post2')
        form = WorkerForm(request.POST)
        print('post3')
        print(form)
        user_form = UserRegistrationForm(request.POST)
        print()
        print()
        print()
        print(user_form)
        
        if form.is_valid():
            print('post4')
            print('Форма правильная')

            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            New_worker.user=new_user
            print(form.cleaned_data['fio_worker'])
            New_worker.fio_worker=form.cleaned_data['fio_worker']
        
            print(form.cleaned_data['passport_number_worker'])
            New_worker.passport_number_worker=form.cleaned_data['passport_number_worker']

            print(form.cleaned_data['date_of_birthday_worker'])
            New_worker.date_of_birthday_worker=form.cleaned_data['date_of_birthday_worker']
            
            print(user_form.cleaned_data['username'])
            New_worker.snils=user_form.cleaned_data['username']

            print(form.cleaned_data['adrress_worker'])
            New_worker.adrress_worker=form.cleaned_data['adrress_worker']

            print(form.cleaned_data['phone_number'])
            New_worker.phone_number=form.cleaned_data['phone_number']

            print(form.cleaned_data['job_tittle'])
            New_worker.job_tittle=form.cleaned_data['job_tittle']

            print(form.cleaned_data['security'])
            New_worker.security=form.cleaned_data['security']

            New_worker.link_photo1_worker = request.FILES.get('myfile1')#request.getFILES['myfile1'] 
            print(New_worker.link_photo1_worker)

            
            all_worker=list(Worker.objects.all()) 
            if all_worker:   
                New_worker.id_worker=len(all_worker)+1
            else:
                New_worker.id_worker=1
 
            New_worker.date_of_registration=date.today()
            New_worker.save()

            user = get_object_or_404(User, username = request.user.username)
            if user.is_staff!=True:
                worker = get_object_or_404(Worker, user=user)
            else:
                return render(request, "security/worker_enter.html", {'form':form})
            # if worker.security!=True:
            #     return render(request, "security/main_c.html")
            # else:
            #     return render(request, "security/worker_enter_w.html", {'form':form})

    else:
        print('get')
        form=Fio()
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, "security/worker_enter.html", {'form':form})
        # if worker.security!=True:
        #     return render(request, "security/main_c.html")
        # else:
        #     return render(request, "security/worker_enter_w.html", {'form':form})


    
    
def search_worker(request):
    if not request.user.is_authenticated:
        return redirect(url_host+'/accounts/login/')
    print('1')
    if request.method=="POST":
        print('post')
        form=Search_client(request.POST)
        # if form.is_valid():
        #     print('2')
        #     all_clients=list(Client_Time.objects.all())

        #     if form.cleaned_data['fio_client']!=None:
        #         fio_filter=form.cleaned_data['fio_client']
        #         fio_filtered_clients=list(Client_Time.objects.filter(fio_client = fio_filter))
        #         all_clients.intersection_update(fio_filtered_clients)
            
        #     if form.cleaned_data['gender']!=None:
        #         gender_filter=form.cleaned_data['gender']
        #         gender_filtered_clients=list(Client_Time.objects.filter(gender = gender_filter))
        #         all_clients.intersection_update(gender_filtered_clients)

        #     if form.cleaned_data['passport_number_client']!=None:
        #         passport_number_filter=form.cleaned_data['passport_number_client']
        #         passport_number_filtered_clients=list(Client_Time.objects.filter(passport_number_client = passport_number_filter))
        #         all_clients.intersection_update(passport_number_filtered_clients)

        #     if form.cleaned_data['age']!=None:
        #         gender_filter=form.cleaned_data['age']
        #         age_min=gender_filter.split('-')[0]
        #         age_max=gender_filter.split('-')[1]
        #         age_min_date=datetime.now() - timedelta(years=age_min)
        #         age_max_date=datetime.now() - timedelta(years=age_max)
        #         age_min_filtered_clients=list(Client_Time.objects.filter(date_of_birthday_client__gte = age_min_date))
        #         age_max_filtered_clients=list(Client_Time.objects.filter(date_of_birthday_client__lte = age_min_date))
        #         all_clients.intersection_update(age_min_filtered_clients)
        #         all_clients.intersection_update(age_max_filtered_clients)
            
        #     if form.cleaned_data['phone_number_client']!=None:
        #         phone_filter=form.cleaned_data['phone_number_client']
        #         phone_filtered_clients=list(Client_Time.objects.filter(phone_number_client = phone_filter))
        #         all_clients.intersection_update(phone_filtered_clients)

        print('2')
        all_workers=set(Worker.objects.all())

        if request.POST.get("fio_worker")!='':
            fio_filter=request.POST.get("fio_worker")
            fio_filtered_workers=set(Worker.objects.filter(fio_worker = fio_filter))
            all_workers.intersection_update(fio_filtered_workers)
          
        if request.POST.get('passport_number_worker')!='':
            passport_number_filter=request.POST.get('passport_number_worker')
            passport_number_filtered_workers=set(Worker.objects.filter(passport_number_worker = passport_number_filter))
            all_workers.intersection_update(passport_number_filtered_workers)

        if request.POST.get('age')!='':
            age_filter=request.POST.get('age')
            age_min=age_filter.split('-')[0]
            age_max=age_filter.split('-')[1]
            age_min_date=datetime.now() - timedelta(days=int(age_min)*365)
            age_max_date=datetime.now() - timedelta(days=int(age_max)*365)
            age_min_filtered_workers=set(Worker.objects.filter(date_of_birthday_worker__lte = age_min_date))
            age_max_filtered_workers=set(Worker.objects.filter(date_of_birthday_worker__gte = age_max_date))
            all_workers.intersection_update(age_min_filtered_workers)
            all_workers.intersection_update(age_max_filtered_workers)
            
        if request.POST.get('phone_number')!='':
            phone_filter=request.POST.get('phone_number')
            phone_filtered_workers=list(Worker.objects.filter(phone_number = phone_filter))
            all_workers.intersection_update(phone_filtered_workers)

        output=[]

        if all_workers=={}:
            output={}
        else:
            if request.FILES.get('myfile1')!=None:
                app_worker=Worker()
                print(request.FILES.get('myfile1'))
                print(request.FILES.get('myfile1'))
                app_worker.link_photo1_worker = request.FILES.get('myfile1')
                known_image = face_recognition.load_image_file(app_worker.link_photo1_worker)
                print(known_image)
                for worker in all_workers:
                    unknown_image = face_recognition.load_image_file(worker.link_photo1_worker)
                    print(unknown_image)
                    baixiaona_encoding = face_recognition.face_encodings(known_image)[0]
                    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                    results = face_recognition.compare_faces([baixiaona_encoding], unknown_encoding)
            
                    if results[0] == True:
                        output.append(worker)
            else:
                output=all_workers

        
        context={
                'result_search' : output
                }
        
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, "security/search_worker.html", context=context)
        if worker.security!=True:
            return render(request, "security/main_c.html")
        else:
            return render(request, "security/search_worker_w.html", context=context)
      
    else:
        print('get')
        
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, "security/search_worker.html")
        if worker.security!=True:
            return render(request, "security/main_c.html")
        else:
            return render(request, "security/search_worker_w.html")


def error(request):
    if not request.user.is_authenticated:
        return redirect(url_host+'/accounts/login/')
    print('start')
    if request.method=="POST":
        print('post1')
        New_error=Error()
        print('post2')
        form = Enter_error(request.POST)
        print('post3')
        print(form.is_valid())
        if form.is_valid():
            all_errors=list(Error.objects.all()) 
            if all_errors:   
                New_error.id_error=len(all_errors)+1
            else:
                New_error.id_error=1
            print('id')
                
            type_error=form.cleaned_data['type_error']
            match type_error:
                case "Ошибка распознования фото":
                    New_error.type_error=0
                case "Ошибка програмного обеспечения":
                    New_error.type_error=1                    
                case "ЧП":
                    New_error.type_error=2
            print(New_error.type_error)
                
            New_error.about_error=form.cleaned_data['about_error']
            print(New_error.about_error)

            New_error.date_error=form.cleaned_data['date_error']
            print(New_error.date_error)

            if request.POST.get("fio_worker")!='':
                fio_filter=request.POST.get("fio_worker")
                fio_filtered_workers=list(set(Worker.objects.filter(fio_worker = fio_filter)))
                if fio_filtered_workers:
                    New_error.id_worker=fio_filtered_workers[0] 
                else:
                    New_error.id_worker=None
                print(New_error.id_worker)
            else:
                New_error.id_worker=None
                
                

            if request.POST.get("fio_client")!='':
                fio_filter=request.POST.get("fio_client")
                fio_filtered_clients=list(set(Client_Time.objects.filter(fio_client = fio_filter)))
                if fio_filtered_clients:
                    New_error.id_clietn=fio_filtered_clients[0] 
                else:
                    New_error.id_clietn=None   
                print(New_error.id_clietn)
            else:
                New_error.id_clietn=None
                
                
            screen=request.FILES.get('myfile1')
            if screen:
                New_error.screen_error = request.FILES.get('myfile1')
            New_error.save()

            print(New_error.screen_error)

            user = get_object_or_404(User, username = request.user.username)
            if user.is_staff!=True:
                worker = get_object_or_404(Worker, user=user)
            else:
                return render(request, "security/error.html", {'form':form})
            if worker.security!=True:
                return render(request, "security/error_c.html")
            else:
                return render(request, "security/error_w.html", {'form':form})
            
    else:
        print('get')
        form=Enter_error()
            
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, "security/error.html", {'form':form})
        if worker.security!=True:
            return render(request, "security/error_c.html")
        else:
            return render(request, "security/error_w.html", {'form':form})




class Error1():
    
    def __init__(self, error):
        self.id_error=error.id_error
        match error.type_error:
            case 0:
                self.type_error="Ошибка распознования фото"
            case 1:
                self.type_error="Ошибка програмного обеспечения"                    
            case 2:
                self.type_error="ЧП"
        self.about_error = error.about_error 
        self.date_error = error.date_error

        if error.id_worker:
            self.id_worker = error.id_worker
        else:
            self.id_worker = ''
        if error.id_clietn:
            self.id_client = error.id_clietn
        else:
            self.id_client = ''
         
        self.screen_error = error.screen_error



def search_error(request):
    if not request.user.is_authenticated:
        return redirect(url_host+'/accounts/login/')
    if request.method=="POST":
        print('post')
        all_errors=set(Error.objects.all())

        if request.POST.get("type_error")!='':
            type_error=request.POST.get("type_error")
            match type_error:
                case "Ошибка распознования фото":
                    type_error_filtered=set(Error.objects.filter(type_error = 0))
                case "Ошибка програмного обеспечения":
                    type_error_filtered=set(Error.objects.filter(type_error = 1))                    
                case "ЧП":
                    type_error_filtered=set(Error.objects.filter(type_error = 2))
            all_errors.intersection_update(type_error_filtered)
          
        if request.POST.get('date_error')!='':
            date_filter=request.POST.get('date_error')
            date_filtered_error=set(Error.objects.filter(date_error = date_filter))
            all_errors.intersection_update(date_filtered_error)

        if request.POST.get('fio_worker')!='':
            fio_worker=request.POST.get('fio_worker')
            worker=list(set(Worker.objects.filter(fio_worker = fio_worker)))
            if worker:
                worker_filtered_errors=set(Error.objects.filter(id_worker = worker[0]))
                all_errors.intersection_update(worker_filtered_errors)
            else:
                all_errors={}
            
        if request.POST.get('fio_client')!='':
            fio_client=request.POST.get('fio_client')
            client=list(set(Client_Time.objects.filter(fio_client = fio_client)))
            if client:
                client_filtered_errors=set(Error.objects.filter(id_clietn = client[0]))
                all_errors.intersection_update(client_filtered_errors)
            else:
                all_errors={}
        output=[]
        if all_errors:
            for error in all_errors:
                new_error=Error1(error)
                output.append(new_error)

        print(output)
        context={
                'result_rearch' : output
                }

        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, "security/search_error.html", context=context)
        if worker.security!=True:
            return render(request, "security/main_c.html")
        else:
            return render(request, "security/search_error_w.html", context=context)
        
    else:
        print('get')
        user = get_object_or_404(User, username = request.user.username)
        if user.is_staff!=True:
            worker = get_object_or_404(Worker, user=user)
        else:
            return render(request, "security/search_error.html")
        if worker.security!=True:
            return render(request, "security/main_c.html")
        else:
            return render(request, "security/search_error_w.html")
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/accounts/login/")
    
def registration(request):
    return

    
