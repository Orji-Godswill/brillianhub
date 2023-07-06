import random
import string
import os
from django.utils.text import slugify

def get_filename(path):
    return os.path.basename(path)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                slug=slug,
                randstr=random_string_generator(size=4)
            )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_key_generator(instance):
    size = random.randint(30, 35)
    key = random_string_generator(size=size)

    klass = instance.__class__
    qs_exists = klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key 