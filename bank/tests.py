from django.test import TestCase
from .models import Post


class PostModelTest(TestCase):
    def setUpTestData(cls):
        Post.objects.create(REGN="50", NAME_B="Sberbank")

    def test_REGN_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('REGN').verbose_name
        self.assertEquals(field_label, 'REGN')

    def test_DT_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('DT').verbose_name
        self.assertEquals(field_label, 'DT')

    def test_NAME_B_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('NAME_B').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_NAME_B_comma_REGN(self):
        post = Post.objects.get(id=1)
        expected_object_name = '%s, %s' % (post.NAME_B, post.REGN)
        self.assertEquals(expected_object_name, str(post))
