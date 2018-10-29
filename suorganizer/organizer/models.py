from datetime import date

from django.db import models
from django.core.urlresolvers import reverse



class TagManager(models.Manager):

    def get_by_natural_key(self,slug):
        return self.get(slug=slug)


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True,
                            help_text='A label for URL config.')

    objects = TagManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizer_tag_detail',
                       args=(self.slug,))

    def get_update_url(self):
        return reverse('organizer_tag_update',
                        kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('organizer_tag_delete',
                        kwargs={'slug':self.slug})

    def published_posts(self):
        return self.blog_posts.filter(pub_date__lt=date.today())

    def natural_key(self):
        return (self.slug,)


class StartupManager(models.Manager):

    def get_by_natural_key(self,slug):
        return self.get(slug=slug)


class Startup(models.Model):
    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True,
                            help_text='A label for URL config.')
    description = models.TextField()
    founded_date = models.DateField('date founded')
    contact = models.EmailField()
    website = models.URLField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = StartupManager()

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizer_startup_detail',
                      kwargs={'slug':self.slug})

    def get_newslink_create_url(self):
        return reverse(
            'organizer_newslink_create',
            kwargs={'startup_slug':self.slug})

    def get_update_url(self):
        return reverse('organizer_startup_update',
                        kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer_startup_delete',
                        kwargs={'slug': self.slug})

    def natural_key(self):
        return (self.slug,)


class NewsLinkManager(models.Manager):

    def get_by_natural_key(self, startup_slug, slug):
        return self.get(startup__slug=startup_slug, slug=slug)


class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    pub_date = models.DateField('date published')
    link = models.URLField(max_length=255)
    startup = models.ForeignKey(Startup)
    slug = models.SlugField(max_length=63)

    objects = NewsLinkManager()

    class Meta:
        verbose_name='news article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug','startup')

    def __str__(self):
        return "{}:{}".format(self.startup, self.title)

    def get_absolute_url(self):
        return self.startup.get_absolute_url()

    def get_update_url(self):
        return reverse('organizer_newslink_update',
                       kwargs={
                            'startup_slug':self.startup.slug,
                            'newslink_slug':self.slug})

    def get_delete_url(self):
        return reverse(
            'organizer_newslink_delete',
            kwargs={'startup_slug': self.startup.slug,
                    'newslink_slug': self.slug})

    def natural_key(self):
        return (self.startup.natural_key(),self.slug)
    natural_key.dependencies = ['organizer.startup']























    
