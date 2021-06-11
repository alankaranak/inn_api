from django.contrib import admin
from company.models import Person, User, Company


class PersonAdmin(admin.ModelAdmin):
    list_display = ('fio', 'uid', 'display_inn')


    def display_inn(self, obj):
        if not obj.inn:
            return "Н\Д"
        return obj.inn.inn
    display_inn.short_description = 'ИНН компании'


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('inn', 'name', 'address', 'nol')


admin.site.register(Company, CompanyAdmin)
admin.site.register(User)
admin.site.register(Person, PersonAdmin)
