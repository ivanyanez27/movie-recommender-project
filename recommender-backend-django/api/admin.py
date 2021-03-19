from django.contrib import admin
from .models import ApiMovie, ApiRating, AuthUser


admin.site.register(ApiMovie)
admin.site.register(ApiRating)
admin.site.register(AuthUser)
