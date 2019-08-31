from django.shortcuts import render

# Create your views here.

"""
# NOTE: Django's views can be either functions, often referred to as
Function-Based Views(FBVs), or classes, often called Class-Based Views(CBVs).
The advantage of CBVs is that Django comes with a rich suite of generic views
that you can subclass to easily (almost declaratively) write views to
accomplish common tasks.
"""

from django.views.generic import ListView, DetailView
from core.models import Movie

class MovieList(ListView):

    """
    # NOTE: ListView requires at least a model attribute. It will query for all rows
    of that model, pass it to the template, and return the rendered template in a response.
    It also offers a number of hooks that we may use to replace default behavior, which
    are fully documented.
    """

    model = Movie

class MovieDetail(DetailView):

    """
    # NOTE: A DetailView requires that a path() object include either a pk or slug in
    the path string so that DetailView can pass that value to the QuerySet to query for
    a specific model instance. A slug is a short URL-friendly label that is often used
    in content-heavy sites, as it is SEO friendly.
    """
    model = Movie
