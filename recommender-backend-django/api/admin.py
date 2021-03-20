from django.contrib import admin
from .models import ApiMovie, ApiRating, AuthUser, ApiLink


admin.site.register(ApiMovie)
admin.site.register(ApiRating)
admin.site.register(ApiLink)
admin.site.register(AuthUser)
