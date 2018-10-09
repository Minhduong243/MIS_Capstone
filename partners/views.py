from django.forms import formset_factory
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CampusPartnerForm, CampusPartnerContactForm, CampusPartnerFormProfile
from django.shortcuts import render
from .models import CampusPartner as CampusPartnerModel
from home.models import Contact as ContactModel, Contact
from home.forms import UserForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, modelformset_factory
from django.template import context
from partners.models import CampusPartner, CampusPartnerUser
from .forms import CampusPartnerForm, CampusPartnerContactForm


def registerCampusPartner(request):
    ContactFormset = modelformset_factory(Contact, extra=1, form=CampusPartnerContactForm)
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)

        formset = ContactFormset(request.POST or None)

        if campus_partner_form.is_valid() and formset.is_valid():
                campus_partner = campus_partner_form.save()
                contacts = formset.save(commit=False)
                for contact in contacts:
                 contact.campus_partner = campus_partner
                 contact.save()
                return render(request, 'home/community_partner_register_done.html')

    else:
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
    return render(request,
                  'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'formset': formset})


# Campus Partner User Profile

# @login_required
# def campusPartnerUserProfile(request):

#   # campus_partner_form = CampusPartnerFormProfile(request.POST or None)

#   # We should get the partner by some unique ID directly based on the login information
#   # current_campus_partner = CampusPartnerModel.objects.get(name="unique name")
#   # Use try catch for using .get

#   # current_campus_partner = CampusPartnerModel.objects.all()[0]
#   # campus_partner_name = current_campus_partner.name
#   # college = current_campus_partner.college
#   # department = current_campus_partner.department

#   # # Contact details from Contact Model
#   # # We should use objects.get(campus_partner=current_campus_partner)
#   # # as it gets the unqiue object mapping result in try catch. 
  
#   # campus_user = CampusPartnerUser.objects.get(
#   #     user= request.user.id)

#   campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

#   if not campus_user:
#     return HttpResponseNotFound('<h1>Page not found</h1>')

#   campus_partner_contact = ContactModel.objects.get(
#     campus_partner=campus_user.campus_partner
#     )

#   return render(request, 'partners/campus_partner_user_profile.html', {"data": campus_partner_contact})


# @login_required
# def campusPartnerUserProfileUpdate(request):
#   campus_partner_contact_form = CampusPartnerContactForm()
  
#   return render(request,
#                 'partners/campus_partner_user_update.html',
#                 {'campus_partner_contact_form': campus_partner_contact_form}
#               )

@login_required
def campusPartnerUserProfile(request):

  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

  if not campus_user:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})


@login_required
def campusPartnerUserProfileUpdate(request):
  user_form = UserForm()

  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

  if not campus_user:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    print ("mohan")
    user_form = UserForm(request.POST)
    # print (user_form.cleaned_data['username'])
    user_form.save()
    return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})

    # if user_form.is_valid():
    #   print ("mohan1")
    #   new_user = user_form.save(commit=False)
    #   # new_user.set_password(user_form.cleaned_data['password'])
    #   new_user.save()
    #   return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})
  else:
    print ("krishna")
  
  return render(request,
                'partners/campus_partner_user_update.html',
                {'user_form': user_form, "campus_partner_name": str(campus_user.campus_partner)}
              )