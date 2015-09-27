from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from contacts.models import Contact 
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from .forms import ContactForm, ContactAddressFormSet
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

class LoggedInMixin(object):

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class ContactOwnerMixin(object):

	def get_object(self, queryset=None):
		""" Returns the object the view is displaying.
		"""
		if queryset is None:
			queryset = self.get_queryset()

		pk = self.kwargs.get(self.pk_url_kwarg, None)
		queryset = queryset.filter(pk=pk, owner=self.request.user,)

		try:
			obj = queryset.get()
		except ObjectDoesNotExist:
			raise PermissionDenied

		return obj

class ListContactView(LoggedInMixin, ListView):
	model = Contact
	template_name = 'contact_list.html'

	def get_queryset(self):
		return Contact.objects.filter(owner=self.request.user)

class CreateContactView(LoggedInMixin, ContactOwnerMixin, CreateView):

    model = Contact
    template_name = 'edit_contact.html'
    #fields = ["first_name", "last_name", "email"]
    form_class = ContactForm
    

    
    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
    	context = super(CreateContactView, self).get_context_data(**kwargs)
    	context['action'] = reverse('contacts-new')
    	context['owner'] = self.request.user
    	return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateContactView, self).form_valid(form)

class UpdateContactView(LoggedInMixin, ContactOwnerMixin, UpdateView):

	model = Contact
	template_name = 'edit_contact.html'
	#fields = ["first_name", "last_name", "email"]
	form_class = ContactForm
	

	def get_success_url(self):
		return reverse('contacts-list')

	def get_context_data(self, **kwargs):
		context = super(UpdateContactView, self).get_context_data(**kwargs)
		context['action'] = reverse('contacts-edit', kwargs={'pk':self.get_object().id})
		return context

class DeleteContactView(LoggedInMixin, ContactOwnerMixin, DeleteView):
	model = Contact
	template_name = 'delete_contact.html'

	def get_success_url(self):
		return reverse('contacts-list')

class ContactView(LoggedInMixin, ContactOwnerMixin, DetailView):
	model = Contact
	template_name = 'contact.html'

class EditContactAddressView(LoggedInMixin, ContactOwnerMixin, UpdateView):

    model = Contact
    template_name = 'edit_addresses.html'
    form_class = ContactAddressFormSet

    def get_success_url(self):

        # redirect to the Contact view.
        return self.get_object().get_absolute_url()

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })