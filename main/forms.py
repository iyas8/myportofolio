from django.forms import ModelForm, TextInput, Textarea
from main.models import Education

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["school", "degree", "start_year", "end_year"]
        labels = {
            "school": "Nama Sekolah / Universitas",
            "degree": "Gelar / Jurusan",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
        }
        widgets = {
            "school": TextInput(attrs={"placeholder": "Contoh: Universitas Indonesia"}),
            "degree": TextInput(attrs={"placeholder": "Contoh: S1 Ilmu Komputer"}),
            "start_year": TextInput(attrs={"placeholder": "Contoh: 2025"}),
            "end_year": TextInput(attrs={"placeholder": "Contoh: Sekarang"}),
        }