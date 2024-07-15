"""
Definition of views.
"""

from datetime import datetime
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View

from django.contrib import messages

from . import forms
from .models import Student
from .constants import DEGREES, GENDER_OPTIONS, INTAKE_OPTIONS, PROGRAMS, TERM_OPTIONS

from .utils import generate_full_name, generate_student_id, send_registration_email, send_resource_email, generate_qrcode


def test(request):
    return render(
        request,
        "app/email_templates/welcome_mail.html",
        {
            "name": "Dr. Strange",
        }
    )


class Home(TemplateView):
    """Renders the home page."""
    
    template_name = "app/index.html"
    extra_context = {
        "title": "Home",
        "year": datetime.now().year,
    }


class SignupView(TemplateView):
    template_name = "app/register_page.html"
    extra_context = {
        "title": "Register"
    }


class LoginView(LoginView):
    template_name = "app/login.html"
    authentication_form = forms.BootstrapAuthenticationForm
    extra_context = {
        "title": "Sign in",
        "year": datetime.now().year,
    }


class UpcomingView(TemplateView):
    """ Renders the upcoming_page html """

    template_name = "app/upcoming_page.html"
    extra_context = {
            "title": "Coming soon...",
            "message": "We are working on bulding this page",
            "year": datetime.now().year,
        }


class CommonContextMixin:
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add common context data
        context.update({
            "year": datetime.now().year,
            "gender_options": GENDER_OPTIONS,
            "intake_options": INTAKE_OPTIONS,
            "term_options": TERM_OPTIONS,
            "degrees": DEGREES,
            "programs": PROGRAMS,
            "fees_options": {True: "Paid", False: "Unpaid"},
        })
        return context


class StudentsTableView(CommonContextMixin, ListView):
    """ Renders students table list page """
    model = Student
    template_name = "app/students.html"
    paginate_by = 10

    year_counts = list(set(x for x in model.objects.values_list("academic_year", flat=True) if x is not None))
    year_counts.sort()
    
    extra_context = {
        "title": "Students list",
        "academic_year_options": dict(zip(year_counts, year_counts)),
        "term_options": TERM_OPTIONS,
        "program_options": PROGRAMS,
    }
    

    def get_queryset(self):
        queryset = super().get_queryset()
        
        name_kw_query = self.request.GET.get("student_name")
        fees_confirmed_query = self.request.GET.get("fees_confirmed")
        registration_mail_query = self.request.GET.get("welcome_mail")
        intake_query = self.request.GET.get("intake")
        academic_yr_query = self.request.GET.get("academic_yr")
        current_term_query = self.request.GET.get("current_term")
        program_query = self.request.GET.get("program")
        
        filt_condition = lambda param: True if param != "" and param is not None else False
            
        if filt_condition(fees_confirmed_query):
            queryset = queryset.filter(fees_confirmed=fees_confirmed_query, status=True)
        if filt_condition(registration_mail_query):
            queryset = queryset.filter(welcome_mail_sent=registration_mail_query, status=True)
        if filt_condition(intake_query):
            queryset = queryset.filter(intake=intake_query, status=True)
        if name_kw_query:
            queryset = queryset.filter(name__icontains=name_kw_query, status=True)
        if academic_yr_query:
            queryset = queryset.filter(academic_year=academic_yr_query, status=True)
        if current_term_query:
            queryset = queryset.filter(current_term=current_term_query, status=True)
        if program_query:
            queryset = queryset.filter(program=program_query, status=True)
        
        return queryset


class StudentFormProcessingMixin:
    def process_form_data(self, form):
        # Format fields
        fname = self.request.POST.get("first_name").strip()
        mname = self.request.POST.get("middle_name").strip()
        lname = self.request.POST.get("last_name").strip()
        email = self.request.POST.get("email_address").lower().strip()
        cucom_email = self.request.POST.get("cucom_email_address").lower().strip()

        # Generate full name
        student_name = generate_full_name(fname, mname, lname)

        id_card_validity = self.request.POST.get("id_valid_from") + "-" + self.request.POST.get("id_valid_to")

        # Update form instance
        obj = form.save(commit=False)
        obj.first_name = fname
        obj.middle_name = mname
        obj.last_name = lname
        obj.email_address = email
        obj.cucom_email_address = cucom_email
        obj.name = student_name
        obj.id_card_validity = id_card_validity

        return obj, student_name


class ProfileView(CommonContextMixin, StudentFormProcessingMixin, UpdateView):
    template_name = "app/profile.html"
    form_class = forms.StudentEntryForm
    model = Student
    # success_url = "/students/"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        stu_obj = context.get("object")

        try:
            id_from, id_to = stu_obj.id_card_validity.split("-")
        except AttributeError:
            id_from, id_to = "", ""

        context["title"] = stu_obj.name
        context["id_val_from"] = id_from
        context["id_val_to"] = id_to
        return context

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        obj, student_name = self.process_form_data(form)

        # Handle additional logic for ProfileView
        student = self.get_context_data().get("object")
        if self.request.POST.get("fees_confirmed") and not student.student_id:
            obj.student_id = generate_student_id(self.request.POST, student.pk)

        obj.save()

        messages.success(self.request, f"{student_name} updated!")
        return super().form_valid(form)


class StudentEntry(CommonContextMixin, StudentFormProcessingMixin, CreateView):
    template_name = "app/student_entry.html"
    model = Student
    form_class = forms.StudentEntryForm
    extra_context = {"title": "Student Entry"}

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        obj, student_name = self.process_form_data(form)
        student_exists = self.model.objects.filter(name__icontains=student_name)
        if student_exists:
            messages.info(self.request, f"{student_name} already exist!")   # Bug: Message not shown.
            return redirect(f"/profile/{student_exists.first().pk}")
        else:
            obj.save()
            messages.success(self.request, f"{student_name} successfully added!")
            return super().form_valid(form)


def delete_student(_, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect("students")


def success_animation():
    return HttpResponse('<video src="https://cdnl.iconscout.com/lottie/premium/thumb/success-5461130-4561483.mp4" muted="muted" loop="loop" type="video/mp4" width="50%" autoplay></video>')


class SendRegistrationMail(View):
    def get(self, _, pk):
        student = get_object_or_404(Student, pk=pk)
        response = send_registration_email(student)
        if response:
            student.welcome_mail_sent = True
            student.save()
        return success_animation()


class SendResourceMail(View):
    def get(self, _, pk):
        student = get_object_or_404(Student, pk=pk)
        response = send_resource_email(student)
        if response:
            student.class_resources_sent = True
            student.save()
        return success_animation()
    

class GenQR(View):
    def get(self, _, pk):
        student = get_object_or_404(Student, pk=pk)
        generate_qrcode(student)
        return success_animation()

