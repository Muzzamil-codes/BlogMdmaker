from django.utils.text import slugify
import math
import string
import random


def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return res


def generate_slug(text):
    new_slug = slugify(text)
    from .models import BlogModel
    if BlogModel.objects.filter(slug=new_slug).first():
        return generate_slug(text + generate_random_string(5))
    return new_slug

def otp_generator():
    digits = "0123456789"
    OTP = ''

    for i in range(4):
        OTP += digits[math.floor(random.random() * 10 )]

    return OTP

