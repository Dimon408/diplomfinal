from django.db import models
from django.conf import settings



# Create your models here.
class Client_Time(models.Model):

    TYPE_CLIENT = [
        (0,'Постоянный'),
        (1,'Временный'),
        (2,'Одноразовый')
    ]
    GENDER = [
        (0, 'Мужской'),
        (1, 'Женский')
    ]
    id_client = models.PositiveIntegerField(primary_key=True)
    fio_client = models.CharField(max_length=255)
    gender = models.SmallIntegerField(choices=GENDER)
    passport_number_client = models.CharField(max_length=255)
    date_of_birthday_client = models.DateField()
    phone_number_client = models.CharField(max_length=255)
    client_type = models.SmallIntegerField(choices=TYPE_CLIENT)#постоянный временный одноразовый
    link_photo1_client = models.ImageField(upload_to='static//photo', default=None, blank=True)
    link_photo2_client = models.ImageField(upload_to='static//photo', default=None, blank=True)
    link_photo3_client = models.ImageField(upload_to='static//photo', default=None, blank=True)

    def __str__(self):
        return str(self.fio_client)

class Worker(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default=None
    )
    id_worker = models.PositiveIntegerField(primary_key=True)
    fio_worker = models.CharField(max_length=255)
    passport_number_worker = models.SmallIntegerField(default=None)
    date_of_birthday_worker = models.DateField()
    snils = models.CharField(max_length=255)
    adrress_worker = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    link_photo1_worker = models.ImageField(upload_to='static//photo', default=None, blank=True)
    link_photo2_worker = models.ImageField(upload_to='static//photo', default=None, blank=True)
    link_photo3_worker = models.ImageField(upload_to='static//photo', default=None, blank=True)
    job_tittle = models.CharField(max_length=255)
    security = models.BooleanField(default=False)
    date_of_registration = models.DateField()

    def __str__(self):
        return str(self.fio_worker)
        


class Error(models.Model):

    TYPE_ERROR = [
        (0,'Ошибка распознования фото'),
        (1,'Ошибка програмного обеспечения'),
        (2,'ЧП')
    ]

    id_error = models.PositiveIntegerField(primary_key=True)
    type_error = models.SmallIntegerField(choices=TYPE_ERROR) # ошибка распознования фото ошибка програмного обеспечения ЧП
    about_error = models.TextField()  # текстбез ограничения длины 
    date_error = models.DateField()
    id_worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True, null=True, default=None)
    id_clietn = models.ForeignKey(Client_Time, on_delete=models.CASCADE, blank=True, null=True, default=None)
    screen_error = models.ImageField(upload_to='static//photo', default=None, blank=True)


class Prohod_place(models.Model):
    id_prohod = models.PositiveIntegerField(primary_key=True)
    id_worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True)
    id_clietn = models.ForeignKey(Client_Time, on_delete=models.CASCADE, blank=True)
    date_start = models.DateField()
    date_end = models.DateField()


class Protect_points(models.Model):
    id_point = models.PositiveIntegerField(primary_key=True)
    name_point = models.CharField(max_length=255)
    adress_point = models.CharField(max_length=255)
    id_superviser = models.ForeignKey(Worker, on_delete=models.CASCADE)


class Dostups(models.Model):
    id_dostup = models.PositiveIntegerField(primary_key=True)
    id_point = models.ForeignKey(Protect_points, on_delete=models.CASCADE, blank=True)
    id_worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=True)
    dostup_start = models.DateField()
    dostup_end = models.DateField()



