from django.contrib import admin
from .models import BlogPost, React, Promote

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(React)
admin.site.register(Promote)
