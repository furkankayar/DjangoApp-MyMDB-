from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
# Create your views here.

"""
# NOTE: Django's views can be either functions, often referred to as
Function-Based Views(FBVs), or classes, often called Class-Based Views(CBVs).
The advantage of CBVs is that Django comes with a rich suite of generic views
that you can subclass to easily (almost declaratively) write views to
accomplish common tasks.
"""


from core.models import Movie, Person, Vote
from core.forms import VoteForm

class MovieList(ListView):

    """
    # NOTE: ListView requires at least a model attribute. It will query for all rows
    of that model, pass it to the template, and return the rendered template in a response.
    It also offers a number of hooks that we may use to replace default behavior, which
    are fully documented.
    """

    """
    # NOTE: ListView has built-in support for pagination. Pagination is controlled
    by the GET parameter page that controls which page to show.
    """
    model = Movie
    paginate_by = 10


class MovieDetail(DetailView):

    """
    # NOTE: A DetailView requires that a path() object include either a pk or slug in
    the path string so that DetailView can pass that value to the QuerySet to query for
    a specific model instance. A slug is a short URL-friendly label that is often used
    in content-heavy sites, as it is SEO friendly.
    """
    model = Movie
    queryset = Movie.objects.all_with_related_persons_and_score()

    def get_context_data(self, **kwargs):
        
        ctx = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user
            )
            if vote.id:
                vote_form_url = reverse(
                    'core:UpdateVote',
                    kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id
                    }
                )
            else:
                vote_form_url = (
                    reverse(
                        'core:CreateVote',
                        kwargs={
                            'movie_id': self.object.id
                        }
                    )
                )
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, CreateView):
    """
    # NOTE: LoginRequeiredMixin is a mixin that can be added to any View and
    will check whether the request is being made by an authenticated user. If
    the user is not logged in, the will be redirected to the login page.
    LOGIN_REDIRECT_URL = // in settings file.
    Or /accounts/profile/ as default.
    """
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail',
                        kwargs={
                            'pk':movie_id
                        })

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail',
                                    kwargs={
                                        'pk':movie_id
                                    })
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):

    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another users vote')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)
