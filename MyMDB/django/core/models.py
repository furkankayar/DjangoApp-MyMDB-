from django.db import models

# Create your models here.

class Movie(models.Model):
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


    class Meta:
        ordering = ('-year', 'title')
        # NOTE: It is like ORDER BY year DESC, title ASC
        

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)
