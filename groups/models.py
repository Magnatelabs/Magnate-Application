from django.db import models
from zinnia.models import Category
from django.utils.translation import ugettext_lazy as _

UPLOAD_LOBBY_COMPANY_LOGO_TO = 'uploads/lobby'

class PortfolioCompany (models.Model):
    
    category = models.ForeignKey(Category)

    name = models.CharField(
        _('company name'), max_length=200)

    description = models.TextField(
        _('company description'), default="")

    tags = models.CharField(
        _('tags'), max_length=400, default="")

    image = models.ImageField(
        _('company logo'), blank=True, upload_to=UPLOAD_LOBBY_COMPANY_LOGO_TO)

    def __unicode__(self):
        return 'Investment. Company: %s, Fund: %s' % (self.name, self.category.title)


# Create your models here.
