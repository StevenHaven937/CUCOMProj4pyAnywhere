import re
import os
import csv

from qrcode.main import QRCode
from email.mime.base import MIMEBase

from django.http.request import QueryDict
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings

from .constants import ONEDRIVE_LINK, WHATSAPP_GROUP_LINK
from .models import Student


def import_csv(file):
    students = csv.DictReader(open(file))
    for student in students:
        Student(
            student_id=student.get("student_id"),
            first_name=student.get("first_name"),
            middle_name=student.get("middle_name"),
            last_name=student.get("last_name"),
            name=student.get("student_name"),
            intake=student.get("intake"),
            joined_term=student.get("joined_term"),
            current_term=student.get("current_term"),
            academic_year=student.get("academic_year") if student.get("academic_year") != "" else None,
            admission_partner=student.get("admission_partner"),
            offer_letter_sent=False if student.get("offer_letter_sent") == "" or student.get("offer_letter_sent") == "0" else True,
            offer_letter_sent_on=student.get("offer_letter_sent_on") if student.get("offer_letter_sent_on") != "" else None,
            offer_letter_signed_on=student.get("offer_letter_signed_on") if student.get("offer_letter_signed_on") != "" else None,
            country=student.get("country"),
            degree=student.get("degree"),
            cucom_email_address=student.get("cucom_email_address"),
            email_address=student.get("email_address"),
            program=student.get("program"),
            date_of_birth=student.get("date_of_birth") if student.get("date_of_birth") != "" else None,
            gender=student.get("gender"),
            offer_letter_signed=False if student.get("offer_letter_signed") == "" else True,
            fees_confirmed=False if student.get("fees_confirmed") == "" or student.get("fees_confirmed") == "0" else True,
            # id_card_image=student.get("id_card_image"),
            id_card_created=False if student.get("id_card_created") == "" or student.get("id_card_created") == "0" else True,
            id_card_created_on=student.get("id_card_created_on") if student.get("id_card_created_on") != "" else None,
            id_card_issued=False if student.get("id_card_issued") == "" or student.get("id_card_issued") == "0" else True,
            id_card_issued_on=student.get("id_card_issued_on") if student.get("id_card_issued_on") != "" else None,
            id_card_validity=student.get("id_card_validity") if student.get("id_card_validity") != "" else None,
            welcome_mail_sent=False if student.get("welcome_mail_sent") == "" or student.get("welcome_mail_sent") == "0" else True,
            orientation_mail_sent=False if student.get("orientation_mail_sent") == "" or student.get("orientation_mail_sent") == "0" else True,
            class_resources_sent=False if student.get("class_resources_sent") == "" or student.get("class_resources_sent") == "0" else True,
            lms_invitation_sent=False if student.get("lms_invitation_sent") == "" or student.get("lms_invitation_sent") == "0" else True,
            whatsapp_invitation_sent=False if student.get("whatsapp_invitation_sent") == "" or student.get("whatsapp_invitation_sent") == "0" else True,
            whatsapp_group_joined=False if student.get("whatsapp_group_joined") == "" or student.get("whatsapp_group_joined") == "0" else True,
            notes=student.get("notes"),
        ).save()


def generate_full_name(fname, mname, lname):
    # Create full name
    if mname.strip() == "":
        student_name = " ".join([fname.strip(), lname.strip()])
    else:
        student_name = " ".join([fname.strip(), mname.strip(), lname.strip()])
        
    return student_name


def generate_student_id(request:QueryDict, pk:int):
    def get_last_sid_generated(p):
        highest = 0
        last_student = Student.objects.filter(program=p)
        for student in last_student:
            s_id = student.student_id
            if s_id and "A-MD" in s_id.upper():
                cv = int(s_id[-4:])
                if cv > highest:
                    highest = cv
        return f"{highest + 1:04d}"
    
    student = Student.objects.get(pk=pk)
    if student.student_id:
        raise ValueError(f"User already have 'student_id': {student.student_id}")
    else:
        program, academic_yr, fname, lname = [
            request.get("program"),
            request.get("academic_year"),
            request.get("first_name"),
            request.get("last_name"),
        ]
        prefix1 = str()
        prefix2 = academic_yr[-2:]
        prefix3 = fname[0] + lname[0]
        suffix = get_last_sid_generated(program)
    
        if program.lower() == "fast track md":
            prefix1 = "A-MD"
        elif program.lower() == "pre med":
            prefix1 = "PM-"
    
        return prefix1 + prefix2 + prefix3 + suffix


def generate_qrcode(student):
    def create_qrcode(filename, data:str):
        filename = str(filename).title()

        # Creating QR code
        qr = QRCode(version=3, box_size=10, border=2) # type: ignore
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(back_color=(255, 255, 255), fill_color=(0, 0, 0))
        
        # Saving QR code in directory
        qr_filename = f"{filename}.png"
        img.save(f"G:\\My Drive\\Docs\\Digital Marketing\\InDesign Data Merge\\CUCOM - ID Card\\QR Codes\\{qr_filename}")

        return qr_filename
    
    existing_qr_codes = [i.lower() for i in os.listdir(r"G:\My Drive\Docs\Digital Marketing\InDesign Data Merge\CUCOM - ID Card\QR Codes")]
    sid = student.student_id
    student_name = student.name
    nationality = student.country
    program = student.degree
    email = student.email_address
    degree = student.degree
    dob = student.date_of_birth
    gender = student.gender
    validity = student.id_card_validity

    is_validated = (
        sid is not None or sid != "" or sid != " ",
        student_name is not None or student_name != "" or student_name != " ",
        nationality is not None or nationality != "" or nationality != " ",
        program is not None or program != "" or program != " ",
        email is not None or email != "" or email != " ",
        degree is not None or degree != "" or degree != " ",
        dob is not None or dob != "" or dob != " ",
        gender is not None or gender != "" or gender != " ",
        validity is not None or validity != "" or validity != " ",
    )

    # Terms and Conditions
    tnc = """
Terms and Conditions:
- Always carry the ID card during class hours and clinical sites for the identification purposes. The card is valid while you continue to be an active student at CUCOM University.
- Each individual student is responsible for managing his/her ID cards. When using the debit card options on your ID card, it must be protected as you would cash or a credit card. Although the card is the property of Commonwealth University school of Medicine, it is entrusted to you for your convenience while enrolled at the university. ID should be accessed by anyone other than the cardholder or requested parents or guests. Only the person pictured on the ID card will be allowed to use an ID card inside the campus as well as in clinical practice areas. The card will be confiscated if infractions are revealed
- Lost, stolen, or misplaced cards must be reported immediately to the ID Services Office at University. The cardholder is responsible for their card at all times
- A new ID card will need to be obtained when you make a classification change like If you have a name change, first provide the Registrar’s Office (student) information to make the change on your record. There is no ID replacement fee for these changes, if the card turned in is not damaged and is your current valid ID card.
    """

    qr_data = f" \
ID Number: {sid}\n \
Student name: {student_name}\n \
Nationality: {nationality}\n \
Program: {program}\n \
Email: {email}\n \
Degree: {degree}\n \
Date of Birth (YYYY/MM/DD): {dob}\n \
Gender: {gender}\n\n \
" + tnc
    
    if is_validated:
        # Generate QR code
        if f'{student_name}.png'.lower() not in existing_qr_codes:
            qr_file = create_qrcode(student_name, qr_data)
        else:
            qr_file = f'{student_name}.png'

        # Create data merge file
        if f'{student_name}.png'.lower() not in existing_qr_codes:
            new_row = {
                        "ID Number": sid,
                        "Student Name": student_name,
                        "Program": degree,
                        "Valid Date": validity,
                        "@qr code": f".\\QR Codes\\{qr_file}",
                        "@image": f".\\Images\\{student_name}.jpg",
                    }

            fieldnames = ["ID Number", "Student Name", "Program", "Valid Date", "@qr code", "@image"]

            with open("G:\\My Drive\\Docs\\Digital Marketing\\InDesign Data Merge\\CUCOM - ID Card\\Django Generated - Data Merge File.csv", "a", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(new_row)
    else:
        raise ValueError("Some data for QR Code generation is missing.")


class EmailMultiRelated(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send multipart/related
    messages. For example, including text and HTML versions with inline images.
    """
    related_subtype = 'related'
    
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None, alternatives=None):
        # self.related_ids = []
        self.related_attachments = []
        return super(EmailMultiRelated, self).__init__(subject, body, from_email, to, bcc, connection, attachments, headers, alternatives)
    
    def attach_related(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted and the mimetype is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """
        if isinstance(filename, MIMEBase):
            assert content == mimetype == None
            self.related_attachments.append(filename)
        else:
            assert content is not None
            self.related_attachments.append((filename, content, mimetype))
    
    def attach_related_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        self.attach_related(filename, content, mimetype)
    
    def _create_message(self, msg):
        return self._create_attachments(self._create_related_attachments(self._create_alternatives(msg)))
    
    def _create_alternatives(self, msg):       
        for i, (content, mimetype) in enumerate(self.alternatives):
            if mimetype == 'text/html':
                for filename, _, _ in self.related_attachments:
                    content = re.sub(r'(?<!cid:)%s' % re.escape(filename), 'cid:%s' % filename, content)
                self.alternatives[i] = (content, mimetype)
        
        return super(EmailMultiRelated, self)._create_alternatives(msg)
    
    def _create_related_attachments(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for related in self.related_attachments:
                msg.attach(self._create_related_attachment(*related))
        return msg
    
    def _create_related_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object. Adjust headers to use Content-ID where applicable.
        Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super(EmailMultiRelated, self)._create_attachment(filename, content, mimetype)
        if filename:
            mimetype = attachment['Content-Type']
            del(attachment['Content-Type'])
            del(attachment['Content-Disposition'])
            attachment.add_header('Content-Disposition', 'inline', filename=filename)
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % filename)
        return attachment


def send_registration_email(student):
    subject = 'Welcome to Commonwealth University College Of Medicine, Saint Lucia!'
    html_msg = render_to_string("app/email_templates/registration.html", context={"name": student.name})
    message = strip_tags(html_msg)
    to = [student.email_address, ]
    # to = ["balajitheboss101@gmail.com", ]

    email = EmailMultiRelated(
        subject,
        message,
        EMAIL_HOST_USER,
        to,
    )
    email.attach_alternative(html_msg, "text/html")
    email.send()

    return True


def send_resource_email(student):
    def get_full_file_paths(directory_path, target_file=None):
        """
        Get full paths of all files in the specified directory.
        Optionally, filter and return the path of a specific file.

        :param directory_path: The path of the directory to list files from.
        :param target_file: The specific file to find (optional).
        :return: List of full file paths or the full path of the target file.
        """
        # List all files in the directory
        file_list = os.listdir(directory_path)

        # Get the full path of each file
        full_paths = [os.path.join(directory_path, file_name) for file_name in file_list]

        # If a specific file is targeted, filter and return its full path
        if target_file:
            for full_path in full_paths:
                if os.path.basename(full_path) == target_file:
                    return full_path
            return None  # Return None if the target file is not found

        # Return the list of full paths
        return full_paths
    
    student_name = str(student.name)
    current_term = str(student.current_term)

    context = {
        "name": student_name,
        "ondrive_link": ONEDRIVE_LINK.get(current_term),
        "whatsapp_link": WHATSAPP_GROUP_LINK.get(current_term),
    }
    subject = 'Important Links and Information for Your Classes'
    html_msg = render_to_string("app/email_templates/resource.html", context=context)
    message = strip_tags(html_msg)
    to = [student.cucom_email_address, ]
    # to = ["balajitheboss101@gmail.com",]

    email = EmailMultiRelated(
        subject,
        message,
        EMAIL_HOST_USER,
        to=to
    )
    email.attach_alternative(html_msg, "text/html")

    # Get attachement file
    directory_path = r"C:\Users\Dr. Sri Balaji\OneDrive - Cucom University\Attachments\Student ID Cards"
    target_file = f"{student_name.upper()}.pdf"
    attachment_file = get_full_file_paths(directory_path=directory_path, target_file=target_file)

    # Condition for attachement
    if attachment_file:
        email.attach_file(attachment_file)
    else:
        raise ValueError(f"'{student_name}' has no ID Card not found at {directory_path}")
    
    email.send()
    return True

