from django.shortcuts import render

# Create your views here.

"""
# NOTE: Django's views can be either functions, often referred to as
Function-Based Views(FBVs), or classes, often called Class-Based Views(CBVs).
The advantage of CBVs is that Django comes with a rich suite of generic views
that you can subclass to easily (almost declaratively) write views to
accomplish common tasks.
"""

from django.views.generic import ListView
from core.models import Movie

class MovieList(ListView):

    """
    # NOTE: ListView requires at least a model attribute. It will query for all rows
    of that model, pass it to the template, and return the rendered template in a responseç
    It also offers a number of hooks that we may use to replace default behavior, which
    are fully documented.
    """

    model = Movie
