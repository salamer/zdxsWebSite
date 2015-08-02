from django.contrib import admin
from data.models import Data,DataComment,Category

# Register your models here.

admin.site.register(Data)
admin.site.register(DataComment)
admin.site.register(Category)
