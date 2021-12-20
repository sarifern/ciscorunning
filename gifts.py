from ic_marathon_app.models import Profile
from django.core.exceptions import MultipleObjectsReturned
from ic_marathon_app.views import check_badges

cecs_who_joined = [
"ksookdeo",
"alegarc2",
"baraiza",
"vbustama",
"lramosba",
"igalanva",
"bzendeja",
"sarifern",
"dfeito",
"carlvarg",
"kagodine",
"tlopezgo",
"josegon5",
"arrosale",
"flugo"
]

for cec in cecs_who_joined:
    try:
        #get profile
        profile = Profile.objects.get(cec=cec)
        profile.distance += 5
        profile.save()
        print(f"user {cec} has been granted the gift")
        check_badges(profile.user)
    except MultipleObjectsReturned:
        #check profile manually
        print(f"duplicated user {cec}, check manually")
    except Profile.DoesNotExist:
        pass