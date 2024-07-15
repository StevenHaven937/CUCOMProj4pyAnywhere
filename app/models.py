"""
Definition of models.
"""

from django.db import models
from django.urls import reverse

class Student(models.Model):
    student_id = models.CharField(max_length=12, default="", blank=True)
    first_name = models.CharField(max_length=50, default="")
    middle_name = models.CharField(max_length=50, default="", blank=True)
    last_name = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=80, default="", blank=True)
    intake = models.CharField(max_length=10, default="")
    joined_term = models.CharField(max_length=35, default="")
    current_term = models.CharField(max_length=35, default="")
    academic_year = models.IntegerField(null=True, blank=True, default="")
    admission_partner = models.CharField(max_length=50, blank=True, default="")
    offer_letter_sent = models.BooleanField(default=False)
    offer_letter_sent_on = models.DateField(null=True, blank=True, default=None)
    offer_letter_signed_on = models.DateField(null=True, blank=True, default=None)
    country = models.CharField(max_length=50, blank=True, default="")
    degree = models.CharField(max_length=25, null=True, blank=True, default="")
    cucom_email_address = models.EmailField(default="", blank=True)
    email_address = models.EmailField(default="", blank=True)
    program = models.CharField(max_length=25, null=True, blank=True, default="")
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    gender = models.CharField(max_length=10, null=True, blank=True, default="")
    offer_letter_signed = models.BooleanField(default=False)
    fees_confirmed = models.BooleanField(default=False)
    
    id_card_link = models.URLField(null=True, blank=True, default="")
    id_card_image = models.ImageField(default="app/assets/default.jpg", upload_to="app/students_photos/")
    id_card_created = models.BooleanField(default=False)
    id_card_created_on = models.DateField(null=True, blank=True, default=None)
    id_card_issued = models.BooleanField(default=False)
    id_card_issued_on = models.DateField(null=True, blank=True, default=None)
    id_card_validity = models.CharField(max_length=10, null=True, blank=True, default="")
    
    welcome_mail_sent = models.BooleanField(default=False)
    orientation_mail_sent = models.BooleanField(default=False)
    class_resources_sent = models.BooleanField(default=False)
    lms_invitation_sent = models.BooleanField(default=False)
    whatsapp_invitation_sent = models.BooleanField(default=False)
    whatsapp_group_joined = models.BooleanField(default=False)

    status = models.BooleanField(default=True)
    
    notes = models.TextField(max_length=255, default="", blank=True)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

