from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea
from django.utils.html import strip_tags
from main.models import Education

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["school", "degree", "start_year", "end_year", "description", "is_active"]
        labels = {
            "school": "Nama Sekolah / Universitas",
            "degree": "Gelar / Jurusan",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
            "description": "Deskripsi Singkat (Opsional)",
            "is_active": "Masih Menempuh Pendidikan?",
        }
        widgets = {
            "school": TextInput(attrs={"placeholder": "Contoh: Universitas Indonesia"}),
            "degree": TextInput(attrs={"placeholder": "Contoh: S1 Ilmu Komputer"}),
            "start_year": TextInput(attrs={"placeholder": "Contoh: 2025"}),
            "end_year": TextInput(attrs={"placeholder": "Contoh: 2029"}),
            "description": Textarea(attrs={"placeholder": "Ceritakan sedikit...", "rows": 3}),
        }

    def clean_school(self):
        school = strip_tags(self.cleaned_data["school"]).strip()
        if not school:
            raise ValidationError("Nama institusi tidak boleh hanya berisi tag HTML.")
        return school

    def clean_degree(self):
        degree = strip_tags(self.cleaned_data["degree"]).strip()
        if not degree:
            raise ValidationError("Gelar atau jurusan tidak boleh hanya berisi tag HTML.")
        return degree

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()