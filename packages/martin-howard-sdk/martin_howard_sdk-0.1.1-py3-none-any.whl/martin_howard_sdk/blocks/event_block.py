from django.db import models
from wagtail import blocks
from ..models import HeadingBlock

# Create your models here.
class EventBlock(blocks.StructBlock):
    heading = HeadingBlock()
    description = blocks.TextBlock()
    # ...

    class Meta:
        template = 'blocks/event.html'