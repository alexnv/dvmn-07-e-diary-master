from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Chastisement, Commendation, Schoolkid, Subject, Lesson


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        for mark in marks:
            mark.points = 5
            mark.save()
    except ObjectDoesNotExist:
        print(f"Не найдено ученика по имени {schoolkid_name}")
    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}")

def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
    except ObjectDoesNotExist:
        print(f"Не найдено ученика по имени {schoolkid_name}")
    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}")


def create_commendation(schoolkid_name, subject_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        subject = Subject.objects.filter(title=subject_name, year_of_study=schoolkid.year_of_study)[0]
        lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study, subject=subject).order_by('date').first()
        #for lesson in lessons:
        commendation = Commendation.objects.create(teacher=lesson.teacher, subject=lesson.subject, schoolkid=schoolkid, created=lesson.date, text="Хвалю!")
        commendation.save()
    except ObjectDoesNotExist:
        print(f"Не найдено ученика по имени {schoolkid_name}")
    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {schoolkid_name}")