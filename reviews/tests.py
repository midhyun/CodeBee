from django.test import TestCase

# Create your tests here.
n = 숫자입력
for i in range(n):
    study = Study()
    study.limits = 4
    study.host_id = 1
    study.title = 'pagination Test'
    study.content = 'pagination Test'
    study.tag = 'pagination Test'
    study.categorie = 'pagination Test'
    study.study_type = 'pagination Test'
    study.deadline = '2022-11-20T22:10:00'
    study.location_type = False
    study.location = 'pagination Test'
    study.X = 'pagination Test'
    study.Y = 'pagination Test'
    study.save()
    Aform = Accepted(joined=True, study=study, users=study.host)
    Aform.save()

