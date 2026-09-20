from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Experience, Education
from main.forms import EducationForm

def show_main(request):
    context = {
        "name": "Muhammad Ilhami Yasya",
        "npm": "2506593891",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student at the University of Indonesia with a strong enthusiasm for technology. I am a committed learner with a growth mindset, currently focused on building a strong foundation in programming."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Muhammad Ilhami Yasya",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    json_response = get_education_json(request)
    educations = serializers.deserialize("json", json_response.content.decode("utf-8"))
    educations = [edu.object for edu in educations]
    
    school_query = request.GET.get("school", "").strip()

    context = {
        "name": "Muhammad Ilhami Yasya",
        "education_list": educations,
        "school_query": school_query,
    }
    return render(request, "education.html", context)

def create_education(request):
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
    educations = Education.objects.all()

    if school_query:
        educations = educations.filter(school__icontains=school_query)

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

def delete_education(request, id):
    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")

def edit_education(request, id):
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