from django.contrib import admin

from channel.models import Channel, Series, Season, Video

# Register your models here.

admin.site.register(Channel)
admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Video)
