from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Staff)
admin.site.register(Shift)
admin.site.register(Concert)
admin.site.register(Ticket)
admin.site.register(Category)