from django.db import models
from wagtail import blocks

# Create your models here.
class HeadingBlock(blocks.CharBlock):
    class Meta:
        template = 'blocks/heading.html'