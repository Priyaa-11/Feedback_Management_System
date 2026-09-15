from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Student

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.department})"

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} -> {self.teacher.name} ({self.rating} Stars)"