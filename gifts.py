from ic_marathon_app.models import Profile
from django.core.exceptions import MultipleObjectsReturned
from ic_marathon_app.views import check_badges

""" cecs_who_joined = [
"apradoca"
] """

cecs_who_joined = ['adlira', 'acalvill', 'adronqui', 'adserran', 'adrsoto', 'alamedra', 'alberthe', 'alsalvad', 'alegarc2', 'adias', 'avercor', 'anpliego', 'aniembro', 'aoscos', 'argamez', 'amezaara', 'artmoral', 'baraiza', 'balvirde', 'bguerram', 'karingon', 'bremarqu', 'ccarapai', 'cesaavil', 'claudipe', 'danrami2', 'dmeixuei', 'daviher2', 'drincond', 'edgarma', 'elopezlo', 'erichgon', 'eradillo', 'glalvara', 'fermunoz', 'flugo', 'gpenaloz', 'florodri', 'gubell', 'hemherna', 'ilgonzal', 'iguerram', 'jacramos', 'jesusiba', 'jorgavil', 'jfuente2', 'josgonz5', 'jlunapal', 'josencha', 'jdavilad', 'jmauleon', 'jaraizal', 'juliocro', 'kagodine', 'kasherna', 'kevsalaz', 'lauraher', 'lchaconz', 'anaarand', 'lucervan', 'lgomezro', 'manuejim', 'malamill', 'mariae', 'maribgue', 'maguila2', 'marsand3', 'jesusgo2', 'maareval', 'mcerqued', 'marizmen', 'gtomich', 'rrojaslo', 'nbecerri', 'ogandari', 'fmejiapa', 'rsanties', 'rebherna', 'rgalveza', 'rogestra', 'rovazque', 'romcleme', 'ronarosa', 'samanmar', 'sromeroz', 'sanespin', 'sebarive', 'vbustama', 'victorhs', 'vlara', 'yperezro', 'armangar', 'ysalaric', 'zespinos']


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