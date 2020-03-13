from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Instructor, ScheduledCourse
from Adtaa import auto_solutions_generator as coffeeFx
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .utils import render_to_pdf

#this is the views page for the adtaa

def index(request):
    return render(request, 'Adtaa/index.html')

def schedule(request):

    if request.method == 'POST':
        coursesQuerySet = ScheduledCourse.objects.all()
        courses = coursesQuerySet[::1]
        coursesToSave = []
        for course in courses:
            if str(course.scheduleNumber) in request.POST:
                coursesToSave.append(course)
        ScheduledCourse.objects.all().delete()
        for course in coursesToSave:
            course.save()
        return redirect('schedcourselist')


    ScheduledCourse.objects.all().delete()
    autosolutions = coffeeFx.main()

    for i in range(len(autosolutions)):
        for j in range(len(autosolutions[i])):
            tempCourse = ScheduledCourse(courseNumber=autosolutions[i][j][0].courseNumber, courseTitle=autosolutions[i][j][0].courseTitle, \
                                         courseDays=autosolutions[i][j][0].courseDays, courseTime=autosolutions[i][j][0].courseTime, \
                                         instructor=autosolutions[i][j][1], scheduleNumber=i+1)
            tempCourse.save()

    outerList=[]
    for solution in autosolutions:
        middleList=[]
        for course in solution:
            innerList=[course[0].courseNumber, course[0].courseTitle, course[0].courseDays, course[0].returnReadableTime(), course[1].lastName]
            middleList.append(innerList)
        outerList.append(middleList)
    autosolutions=outerList
    context = {'autosolutions': autosolutions}




    return render(request, 'Adtaa/schedule.html', context)



class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'

class CourseAddView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['courseNumber', 'courseTitle', 'courseDays', 'courseTime', 'discipline1', 'discipline2']

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['courseNumber', 'courseTitle', 'courseDays', 'courseTime', 'discipline1', 'discipline2']

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model=Course
    success_url = '/courselist'



class InstructorListView(ListView):
    model = Instructor
    context_object_name = 'instructors'

class InstructorAddView(LoginRequiredMixin, CreateView):
    model = Instructor
    fields = ['firstName', 'lastName', 'maxClassLoad', 'discipline1', 'discipline2']

class InstructorUpdateView(LoginRequiredMixin, UpdateView):
    model = Instructor
    fields = ['firstName', 'lastName', 'maxClassLoad', 'discipline1', 'discipline2']

class InstructorDeleteView(LoginRequiredMixin, DeleteView):
    model=Instructor
    success_url = '/instructorlist'


class SchedCourseListView(ListView):
    model = ScheduledCourse
    context_object_name = 'courses'

class SchedCourseUpdateView(LoginRequiredMixin, UpdateView):
    model = ScheduledCourse
    fields = ['courseNumber', 'courseTitle', 'courseDays', 'courseTime', 'instructor']

def generatePDF_view(request, *args, **kwargs):
    template=get_template('Adtaa/printed_schedule.html')
    coursesQuerySet = ScheduledCourse.objects.all()
    courses = coursesQuerySet[::1]
    context = {
        'scheduledcourses':courses
    }
    html=template.render(context)
    # pdf = render_to_pdf('Adtaa/printed_schedule.html', context)
    pdf = render_to_pdf('Adtaa/printed_schedule.html', context)
    return HttpResponse(pdf, content_type='application/pdf')