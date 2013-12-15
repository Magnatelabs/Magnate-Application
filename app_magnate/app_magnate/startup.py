import copy

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


def autoload(submodules):
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        for submodule in submodules:
            try:
                import_module("{}.{}".format(app, submodule))
            except:
                if module_has_submodule(mod, submodule):
                    raise


def startup_validation():
    from brabeion import badges
    from status_awards.base import MetaBadge
    # check if static resources exist
    from django.contrib.staticfiles import finders
    from django.conf import settings

    slug_set = set()
    for badge_slug in badges._registry:
        assert badge_slug not in slug_set
        slug_set.add(badge_slug)

        badge = badges._registry[badge_slug]
        assert badge.slug == badge.slug
        assert hasattr(badge, 'levels')
        assert hasattr(badge, 'events')
        assert isinstance(badge.levels, list)
        assert isinstance(badge.events, list)
        assert len(badge.levels) > 0
        for e in badge.events:
            assert isinstance(e, str)
            assert e in badges._event_registry
        if isinstance(badge, MetaBadge):
            assert hasattr(badge, 'requirements')
            assert len(badge.requirements) == len(badge.levels)
        if not settings.TESTING:
            for level in range(len(badge.levels)):
                # Make sure that the picture for the badge exists
                pic_url = 'status_awards/badge_%s_%d.png' % (badge_slug, level)
                assert finders.find(pic_url) is not None, "Cannot find necessary static file %s" % pic_url


def run():
    autoload(["receivers"])
    startup_validation()
