from django import forms
from django.contrib.auth.models import User

class Fio(forms.Form):
    fio_client = forms.CharField()
    gender = forms.CharField()
    passport_number_client=forms.CharField()
    date_of_birthday_client=forms.DateField()
    phone_number_client=forms.CharField()
    client_type=forms.CharField()
    #link_photo1_client = forms.ImageField()

    def getfio(self):
        values=self.data['fio_client']
        return values

    def getgender(self):
        values=self.data['gender']
        return values

    def getpassport(self):
        values=self.data['passport_number_client']
        return values

    def getdate(self):
        values=self.data['date_of_birthday_client']
        return values
    
    def getphone(self):
        values=self.data['phone_number_client']
        return values

    def gettype(self):
        values=self.data['client_type']
        return values

    # def getphoto(self):
    #     values=self.data['link_photo1_client']
    #     return values

class Search_client(forms.Form):
    fio_client = forms.CharField()
    gender = forms.CharField()
    passport_number_client=forms.CharField()
    age=forms.CharField()
    phone_number_client=forms.CharField()
    
    def getfio(self):
        values=self.data['fio_client']
        return values

    def getgender(self):
        values=self.data['gender']
        return values

    def getpassport(self):
        values=self.data['passport_number_client']
        return values

    def getage(self):
        values=self.data['age']
        return values
    
    def getphone(self):
        values=self.data['phone_number_client']
        return values

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()
    

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
        
class WorkerForm(forms.Form):
    fio_worker = forms.CharField()
    passport_number_worker = forms.IntegerField()
    date_of_birthday_worker = forms.DateField()
    adrress_worker = forms.CharField()
    phone_number = forms.IntegerField()
    job_tittle = forms.CharField()
    security = forms.BooleanField()
    #link_photo1_client = forms.ImageField()


    def getfio(self):
        values=self.data['fio_worker']
        return values

    def getpassort_number(self):
        values=self.data['passport_number_worker']
        return values

    def getdate_of_birthday_worker(self):
        values=self.data['date_of_birthday_worker']
        return values

    def getsnils(self):
        values=self.data['snils']
        return values
    
    def getadrress_worker(self):
        values=self.data['adrress_worker']
        return values

    def getphone_worker(self):
        values=self.data['phone_number']
        return values
    
    def getjob_title(self):
        values=self.data['job_tittle']
        return values
    
    def getsecurity(self):
        values=self.data['security']
        return values
    
class Search_worker(forms.Form):
    fio_worker = forms.CharField()
    passport_number_worker = forms.IntegerField()
    age = forms.CharField()
    snils = forms.CharField()
    phone_number = forms.IntegerField()
    job_tittle = forms.CharField()
    #link_photo1_client = forms.ImageField()

    def getfio(self):
        values=self.data['fio_worker']
        return values

    def getpassort_number(self):
        values=self.data['passport_number_worker']
        return values

    def getage(self):
        values=self.data['age']
        return values

    def getsnils(self):
        values=self.data['snils']
        return values

    def getphone_worker(self):
        values=self.data['phone_number']
        return values
    
    def getjob_title(self):
        values=self.data['job_tittle']
        return values
    
class Enter_error(forms.Form):
    type_error=forms.CharField()
    about_error=forms.CharField()
    date_error=forms.DateField()
    #fio_worker=forms.CharField()
    #fio_client=forms.CharField()

    def gettype_error(self):
        values=self.data['type_error']
        return values
    
    def getabout_error(self):
        values=self.data['about_error']
        return values
    
    def getdate(self):
        values=self.data['date_error']
        return values
    
    # def getfio_worker(self):
    #     values=self.data['fio_worker']
    #     return values
    
    # def getfio_client(self):
    #     values=self.data['fio_client']
    #     return values


    