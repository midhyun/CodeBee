from django.shortcuts import render,redirect
from .forms import StudyForm, AcceptedForm
from .models import Study, Accepted

# Create your views here.

def home(request):
    return render(request, 'home.html')

def index(request):
    studies = Study.objects.order_by('-pk')
    context = {
        'studies': studies
    }
    return render(request, 'reviews/index.html', context)

def create(request):
    if request.method =='POST':
        study_form = StudyForm(request.POST, request.FILES)
        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.host = request.user
            study.save()
            Aform = Accepted(joined=True,study=study,users=study.host)
            Aform.save()
            return redirect('reviews:index')
    else:
        study_form = StudyForm()
    context = {'study_form' : study_form}
    return render(request, 'reviews/form.html', context)

def detail(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    context = {
        'study':study
    }
    return render(request, 'reviews/detail.html', context)

def update(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    if request.user == study.host:
        if request.method == 'POST':
            study_form = StudyForm(request.POST, request.FILES, instance=study)
            if study_form.is_valid():
                study_form.save()
                return redirect('reviews:detail', study_pk)
        else:
            study_form = StudyForm(instance=study)
        context = {'study_form': study_form}
        return render(request, 'reviews/form.html', context)
    else:
        return redirect('reviews:detail', study_pk)

def delete(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    study.delete()
    return redirect('reviews:index')

# def join(requset, study_pk, user_pk):
#     study = Study.objects.get(pk=study_pk)
#     accepted = Accepted.objects.filter(study_id=study_pk)
#     if study.limits > len(accepted):

#     return redirect('reviews:index')