from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.

"""
# NOTE: If CreateView reveives a GET request, it will render the template for
the form. One of the anchestors of CreateView is FormMixin which overrides
get_context_data() to call get_form() an add the form instance to out template's
context. The renderred template is returned as the body of the response by
render_to_response.
If CreateView receives a POST request, it will also use get_form() to get form
instance. The form will be bound to the POST data in the request. A bound form can
validate the data it is bound to. CreateView will then call form.is_valid() and
either form_valid() or form_invalid() as appropriate. form_valid() will call
form.save() (saving the data to the database) then return a 302 response that will
redirect the browser to success_url. The form_invalid() method will re-render the
template with the form (which will now contain error messages for the user to fix
and resubmit)
"""
class RegisterView(CreateView):
    template_name='user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('core:MovieList')
