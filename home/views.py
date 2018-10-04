from .models import *
from university.models import *
from partners.models import CampusPartnerUser, CommunityPartnerUser, CampusPartner, CommunityPartner
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner
from .forms import UserForm, CommunityPartnerForm, CommunityContactForm, CampusPartnerUserForm, \
    CommunityPartnerUserForm, UploadProjectForm, UploadCommunityForm , CampusPartnerForm, UploadCampusForm, \
    UploadProjectCommunityForm, UploadProjectCampusForm
from django.shortcuts import render
from django.urls import reverse
import csv
from collections import OrderedDict
from django.contrib import messages


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})


def cpipage(request):
    return render(request, 'home/CpiHome.html',
                  {'cpipage': cpipage})


def signup(request):
    return render(request, 'home/registration/signuporganization.html', {'signup': signup})


def signupuser(request):
    return render(request, 'home/registration/signupuser.html', {'signupuser': signupuser})


def registerCampusPartnerUser(request):
    campus_partner_user_form = CampusPartnerUserForm()

    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        campus_partner_user_form = CampusPartnerUserForm(request.POST)
        # community_partner_form = CommunityPartnerForm(request.POST)
        if user_form.is_valid() and campus_partner_user_form.is_valid():
            # and community_partner_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # cpu = CampusPartnerUser(campuspartner=CampusPartner.objects.filter(
            #         campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'])[0], user=new_user)
            cpu = CampusPartnerUser(campuspartner=campus_partner_user_form.cleaned_data['name'], user=new_user)
            cpu.save()

            return render(request, 'home/register_done.html', )
    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form})


def registerCommunityPartnerUser(request):
    community_partner_user_form = CommunityPartnerUserForm()
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        # campus_partner_form = CampusPartnerForm(request.POST)
        community_partner_user_form = CommunityPartnerUserForm(request.POST)
        if user_form.is_valid() and community_partner_user_form.is_valid():
            # and campus_partner_form.is_valid()
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # cpu = CommunityPartnerUser(communitypartner=CommunityPartner.objects.filter(
            #        name=community_partner_form.cleaned_data['name'])[0], user=new_user)
            cpu = CommunityPartnerUser(communitypartner=community_partner_user_form.cleaned_data['name'], user=new_user)
            cpu.save()
            return render(request, 'home/register_done.html', )
    return render(request,
                  'home/registration/community_partner_user_register.html',
                  {'user_form': user_form, 'community_partner_user_form': community_partner_user_form})



def registerCampusPartner(request):
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)

        if campus_partner_form.is_valid():
            campus_partner_form.save()

            return render(request, 'home/community_partner_register_done.html', )
    else:
        campus_partner_form = CampusPartnerForm()

    return render(request,
                  'home/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form})




def registerCommunityPartner(request):
    if request.method == 'POST':
        community_partner_form = CommunityPartnerForm(request.POST)
        community_partner_contact_form = CommunityContactForm(request.POST)

        if community_partner_form.is_valid() and community_partner_contact_form.is_valid():
            community_partner_form.save()
            community_partner_contact_form.save()

            return render(request, 'home/community_partner_register_done.html', )
    else:
        community_partner_form = CommunityPartnerForm()
        community_partner_contact_form = CommunityContactForm()

    return render(request,
                  'home/community_partner_register.html',
                  {'community_partner_form': community_partner_form,
                   'community_partner_contact_form': community_partner_contact_form}, )


def upload_project(request):
    if request.method == 'GET':
        download_projects_url = '/media/projects_sample.csv'
        return render(request, 'import/uploadProject.html',
                      {'download_projects_url': download_projects_url})
    if request.method == 'POST':
        print(request)
        csv_file = request.FILES["csv_file"]
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            data_dict = dict(OrderedDict(row))
            project_new = data_dict['project_name']
            project_name_existing = Project.objects.filter(project_name=data_dict['project_name'])
            try:
                project_old = str(project_name_existing[0])
                if project_old == project_new:
                    form_campus = UploadProjectCampusForm(data_dict)
                    form_community = UploadProjectCommunityForm(data_dict)
                    if form_campus.is_valid() and form_community.is_valid():
                        form_campus.save()
                        form_community.save()

            except:
                form = UploadProjectForm(data_dict)
                if form.is_valid():
                    form.save()
                    form_campus = UploadProjectCampusForm(data_dict)
                    form_community = UploadProjectCommunityForm(data_dict)
                    if form_campus.is_valid and form_community.is_valid():
                        form_campus.save()
                        form_community.save()
    return render(request, 'import/uploadProject.html',
                  {'upload_project': upload_project})


def upload_community(request):
    if request.method == 'GET':
        download_community_url = '/media/community_sample.csv'
        return render(request, 'import/uploadCommunity.html',
                      {'download_community_url': download_community_url})
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        form = UploadCommunityForm(data_dict)
        print(form)
        if form.is_valid():
            form.save()
    return render(request, 'import/uploadCommunity.html',
                  {'upload_community': upload_community})


def upload_campus(request):
    if request.method == 'GET':
        download_campus_url = '/media/campus_sample.csv'
        return render(request, 'import/uploadCampus.html',
                      {'download_campus_url': download_campus_url})
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        form = UploadCampusForm(data_dict)
        if form.is_valid():
            form.save()
    return render(request, 'import/uploadCampus.html',
                  {'upload_campus': upload_campus})

