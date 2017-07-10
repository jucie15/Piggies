from django.contrib import admin
from accounts.models import Profile
from cast.models import Favorite

# class FavoriteInline(admin.StackedInline):
#     model = Favorite

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile

