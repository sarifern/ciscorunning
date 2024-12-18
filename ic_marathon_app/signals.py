# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver
# from .models import Workout
# from django.core.files.storage import default_storage
# import q


# @receiver(post_delete, sender=Workout)
# def delete_workout(sender, instance, **kwargs):
#     # update personal distance
#     profile = instance.belongs_to
#     profile.distance -= instance.distance

#     if profile.distance < profile.user_goal_km:
#         profile.user_goal = False
#     profile.save()

#     # delete image from S3
#     try:
#         default_storage.delete(instance.photo_evidence.name)
#     except Exception:
#         q("Can't delete the file {} in S3".format(instance.photo_evidence.name))


# @receiver(post_save, sender=Workout)
# def save_workout(sender, instance, **kwargs):
#     # update personal distance
#     profile = instance.belongs_to
#     profile.distance += instance.distance
#     if profile.distance >= 84.0 and profile.category == "beginnerrunner":
#         profile.category = "runner"
#     if profile.distance >= profile.user_goal_km:
#         profile.user_goal = True
#     profile.save()
