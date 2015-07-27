# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TransactionTestCase
from django.utils.translation import ugettext_lazy as _

from test_project.models import Complex, Simple, Unconventional


class TestTranslatableAutoSlugifyMixin(TransactionTestCase):

    def test_simple_slug(self):
        simple = Simple()
        simple.set_current_language('en')
        simple.name = 'Simple'
        simple.save()
        self.assertEquals(simple.slug, 'simple')

    def test_unconventional_slug(self):
        unconventional = Unconventional()
        unconventional.set_current_language('en')
        unconventional.title = 'Unconventional'
        unconventional.save()
        self.assertEquals('unconventional', unconventional.unique_slug)

    def test_complex_slug(self):
        complex1 = Complex()
        complex1.set_current_language('en')
        complex1.name = 'one'
        complex1.object_type = 'complex'
        complex1.save()
        self.assertEquals('complex-one', complex1.slug)

    def test_existing_object(self):
        simple = Simple()
        simple.set_current_language('en')
        simple.save()
        # slug is now the default
        simple.name = 'A new name'
        simple.slug = None
        simple.save()
        self.assertEquals('a-new-name', simple.slug)

    def test_limited_length(self):
        Simple.slug_max_length = 6
        try:
            for r in range(0, 101):
                simple = Simple()
                simple.set_current_language('en')
                simple.name = 'Simple'
                simple.save()
        except:
            self.fail()
        Simple.slug_max_length = None

    def test_slug_unique_global(self):
        Simple.slug_globally_unique = True

        simple_en = Simple()
        simple_en.set_current_language('en')
        simple_en.name = 'SimpleOne'
        simple_en.save()

        simple_fr = Simple()
        simple_fr.set_current_language('fr')
        simple_fr.name = 'SimpleOne'
        simple_fr.save()

        self.assertNotEquals(simple_en.slug, simple_fr.slug)

        Simple.slug_globally_unique = None  # default is False

        simple_en = Simple()
        simple_en.set_current_language('en')
        simple_en.name = 'SimpleTwo'
        simple_en.save()

        simple_fr = Simple()
        simple_fr.set_current_language('fr')
        simple_fr.name = 'SimpleTwo'
        simple_fr.save()

        self.assertEquals(simple_en.slug, simple_fr.slug)

    def test_simple_slug_default(self):
        # First test that the default works
        simple = Simple()
        simple.set_current_language('en')
        simple.save()
        self.assertEquals(
            'simple-without-name', simple.get_slug_default())
        # Also test without explicit language
        self.assertEquals(
            'simple-without-name', simple.get_slug_default())

        # Now test that a default would be used if available
        Simple.slug_default = _('unnamed-simple-object')
        simple = Simple()
        simple.set_current_language('en')
        simple.save()
        self.assertEquals(
            'unnamed-simple-object', simple.get_slug_default())
        # Also test without explicit language
        self.assertEquals(
            'unnamed-simple-object', simple.get_slug_default())

    def test_unconventional_slug_default(self):
        unconventional = Unconventional()
        unconventional.set_current_language('en')
        unconventional.save()
        self.assertEquals(
            'unconventional-model-without-short-title',
            unconventional.get_slug_default()
        )

    def test_complex_slug_default(self):
        complex1 = Complex()
        complex1.set_current_language('en')
        complex1.save()
        self.assertEquals('complex-without-name', complex1.slug)
