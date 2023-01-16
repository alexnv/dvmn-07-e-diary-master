import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Chastisement, Commendation, Schoolkid, Subject, Lesson

PRAISES_LIST = ["Хвалю!"]

def get_schoolkid_by_name(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
        return schoolkid
    except ObjectDoesNotExist:
        print(f"Не найдено ученика по имени {name}")
    except MultipleObjectsReturned:
        print(f"Найдено более одного ученика по имени {name}")


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid_by_name(schoolkid_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points = 5)


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid_by_name(schoolkid_name)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name, subject_name):
    schoolkid = get_schoolkid_by_name(schoolkid_name)
    subject = Subject.objects.filter(title=subject_name, year_of_study=schoolkid.year_of_study).first()
    lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study,
                                   subject=subject).order_by('date').first()
    commendation = Commendation.objects.create(teacher=lesson.teacher, subject=lesson.subject, schoolkid=schoolkid,
                                               created=lesson.date, text=random.choice(PRAISES_LIST))
