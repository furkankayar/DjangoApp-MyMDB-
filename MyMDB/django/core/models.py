from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum

# Create your models here.

class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')
        return qs

    def all_with_related_persons_and_score(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum('vote__value'))
        """
        # NOTE: annotate turns our regular SQL query into an aggregate query,
        adding the supplied aggregate operation's result to e new attribute
        called score. Django abstracts most common SQL aggregate functions
        into class representations, including Sum, Count and Average (and more). 
        """
        return qs

class Movie(models.Model):
    objects = MovieManager()

    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
                (NOT_RATED, 'NR - Not Rated'),
                (RATED_G, 'G - General Audiences'),
                (RATED_PG, 'PG - Parental Guidance Suggested'),
                (RATED_R, 'R - Restricted'),
            )
    """
    # NOTE: Django will add and istance method to our model called
    get_rating_display(), which will return the matching second element for the
    value stored in our model. Anything that doesn't match one of the values in
    choices will be a ValidationError on save.
    """
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank = True)
    director = models.ForeignKey(
        to='Person',
        on_delete=models.SET_NULL,
        related_name='directed',
        null=True,
        blank=True)
    # NOTE: related_name offers person.directed.add(movie) usage.
    writers = models.ManyToManyField(
        to='Person',
        related_name='writing_credits',
        blank=True)
    # NOTE: person.writing_credits.add(movie) same as movie.writers.add(person)
    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True)
    # NOTE: ManyToManyField with a through class.

    class Meta:
        ordering = ('-year', 'title')
        # NOTE: It is like ORDER BY year DESC, title ASC


    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

"""
# NOTE: PersonDetail view will list all the movies in which a Person is acting,
writing or directing credits. In our template, we will print out the name of each
film in each credit(and Role.name for the acting credits).To avoid sending a
flood of queries to the database, we will create new managers for our models that
will return smarter QuerySet's.
"""

class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie')

class Person(models.Model):

    objects = PersonManager()

    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.died:
            return '{}, {} ({}-{})'.format(
                self.last_name,
                self.first_name,
                self.born.year,
                self.died.year)

        return '{}, {} ({})'.format(
            self.last_name,
            self.first_name,
            self.born.year)


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return "{} {} {}".format(self.movie_id, self.person_id, self.name)

    class Meta:
        ordering = ('movie', 'person', 'name')


class VoteManager(models.Manager):

    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(movie=movie, user=user)
        except Vote.DoesNotExist:
            return Vote(movie=movie, user=user)


class Vote(models.Model):

    objects = VoteManager()

    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "+1"),
        (DOWN, "-1"),
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
    """
    # NOTE: unique_together attribute of Meta creates a unique constraint on the
    table. A unique constraint will prevent two rows having the same value for
    both user and movie, enforcing our rule of one vote per user per movie.
    """
