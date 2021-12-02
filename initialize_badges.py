from django.contrib.staticfiles.storage import staticfiles_storage
from badgify.models import Award, Badge
Badge.objects.get_or_create(slug="ownK", name="My milestone", description="Congratulations! You achieved your goal",
                            image=staticfiles_storage.open('img/own.jpg'))
Badge.objects.get_or_create(slug="168K", name="168K Milestone Achieved", description="Impossible is nothing! You set a four marathon record",
                            image=staticfiles_storage.open('img/168k.jpg'))
Badge.objects.get_or_create(slug="126K", name="126K Milestone Achieved", description="Insane! You set a three marathon record",
                            image=staticfiles_storage.open('img/126k.jpg'))
Badge.objects.get_or_create(slug="84K", name="84K Milestone Achieved", description="You’re on Fire!  You set a two marathon record",
                            image=staticfiles_storage.open('img/84k.jpg'))
Badge.objects.get_or_create(slug="42K", name="42K Milestone Achieved", description="You reached your goal! Give an extra mile!",
                            image=staticfiles_storage.open('img/42k.jpg'))
Badge.objects.get_or_create(slug="21K", name="21K Award Unlocked", description="Wow! You set a new half marathon personal record",
                            image=staticfiles_storage.open('img/21k.jpg'))
Badge.objects.get_or_create(slug="10K", name="10K Record Smashed", description="Congrats! You set a new 10k personal record",
                            image=staticfiles_storage.open('img/10k.jpg'))
