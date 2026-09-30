import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Experience, Education
from main.forms import EducationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Muhammad Ilhami Yasya",
        "npm": "2506593891",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student at the University of Indonesia with a strong enthusiasm for technology. I am a committed learner with a growth mindset, currently focused on building a strong foundation in programming."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Muhammad Ilhami Yasya",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    school_query = request.GET.get("school", "").strip()
    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Muhammad Ilhami Yasya",
        "school_query": school_query,
        "is_editor": is_editor,
        "form": EducationForm(),
    }
    return render(request, "education.html", context)

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Muhammad Ilhami Yasya",
        "form": form,
    }
    return render(request, "education_form.html", context)

def get_education_json(request):
    school_query = request.GET.get("school", "").strip()
    educations = Education.objects.prefetch_related('starred_by').all()

    if school_query:
        educations = educations.filter(school__icontains=school_query)

    data = []
    for edu in educations:
        starred_users = edu.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(edu.id),
            "fields": {
                "school": edu.school,
                "degree": edu.degree,
                "start_year": edu.start_year,
                "end_year": edu.end_year,
                "description": edu.description,
                "is_active": edu.is_active,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_education(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")

@login_required(login_url="/login/")
def edit_education(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=id)

    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui")
        return redirect("main:show_education")

    context = {
        "name": "Muhammad Ilhami Yasya",
        "form": form,
    }
    return render(request, "edit_education.html", context)


@login_required(login_url="/login/")
def toggle_star(request, id):
    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)
    return redirect("main:show_education")


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    context = {
        "name": "Muhammad Ilhami Yasya",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    context = {
        "name": "Muhammad Ilhami Yasya",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan riwayat pendidikan."},
            status=403,
        )

    form = EducationForm(request.POST)
    if form.is_valid():
        education = form.save()
        return JsonResponse(
            {"message": "Riwayat pendidikan berhasil ditambahkan.", "pk": str(education.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)