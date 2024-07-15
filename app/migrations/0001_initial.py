# Generated by Django 5.0.6 on 2024-06-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, default='', max_length=12)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('middle_name', models.CharField(blank=True, default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('name', models.CharField(blank=True, default='', max_length=80)),
                ('intake', models.CharField(default='', max_length=10)),
                ('joined_term', models.CharField(default='', max_length=35)),
                ('current_term', models.CharField(default='', max_length=35)),
                ('academic_year', models.IntegerField(blank=True, default='', null=True)),
                ('admission_partner', models.CharField(blank=True, default='', max_length=50)),
                ('offer_letter_sent', models.BooleanField(default=False)),
                ('offer_letter_sent_on', models.DateField(blank=True, default=None, null=True)),
                ('offer_letter_signed_on', models.DateField(blank=True, default=None, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=50)),
                ('degree', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('cucom_email_address', models.EmailField(blank=True, default='', max_length=254)),
                ('email_address', models.EmailField(blank=True, default='', max_length=254)),
                ('program', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('date_of_birth', models.DateField(blank=True, default=None, null=True)),
                ('gender', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('offer_letter_signed', models.BooleanField(default=False)),
                ('fees_confirmed', models.BooleanField(default=False)),
                ('id_card_link', models.URLField(blank=True, default='', null=True)),
                ('id_card_image', models.ImageField(default='app/assets/default.jpg', upload_to='app/students_photos/')),
                ('id_card_created', models.BooleanField(default=False)),
                ('id_card_created_on', models.DateField(blank=True, default=None, null=True)),
                ('id_card_issued', models.BooleanField(default=False)),
                ('id_card_issued_on', models.DateField(blank=True, default=None, null=True)),
                ('id_card_validity', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('welcome_mail_sent', models.BooleanField(default=False)),
                ('orientation_mail_sent', models.BooleanField(default=False)),
                ('class_resources_sent', models.BooleanField(default=False)),
                ('lms_invitation_sent', models.BooleanField(default=False)),
                ('whatsapp_invitation_sent', models.BooleanField(default=False)),
                ('whatsapp_group_joined', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
