from django.shortcuts import render

from main.models import Experience


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