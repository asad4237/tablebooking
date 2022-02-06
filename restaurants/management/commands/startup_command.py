from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group , Permission
from django.contrib.auth import get_user_model
import logging
import os
import traceback
from restaurants.models import Restaurant
from restaurants.tests.factories import RestaurantFactory

User = get_user_model()

GROUPS = {
    "Admin": {
        #general permissions
        "log entry" : ["add","delete","change","view"],
        "group" : ["add","delete","change","view"],
        "permission" : ["add","delete","change","view"],
        "user" : ["add","delete","change","view"],
        "content type" : ["add","delete","change","view"],
        "session" : ["add","delete","change","view"],

        #django app model specific permissions
        "table" : ["add","delete","change","view"],
        "booking" : ["view",'add', 'change'],
    },

    "Employee": {
        #django app model specific permissions
        "booking" : ["view",'add', 'change'],
    },
}


USERS = {

    "1111" : ["Admin","admin@domain.sa","12345678"],
    "2222" : ["Employee","employee@domain.sa","12345678"],
}


class Command(BaseCommand):
    help = 'startup command'

    def handle(self, *args, **kwargs):
        try:
            # put startup code here
            #for p in Permission.objects.all():
            #   print(p.pk,"- content_type - ", p.content_type,"- codename - ", p.codename,"- name - ", p.name)
            superuser_pass = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            superuser_name = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            superuser_email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            new_user, created = User.objects.get_or_create(staffnumber=superuser_name, is_staff=True,
                                                           is_superuser=True, email=superuser_email)
            new_user.set_password(superuser_pass)
            new_user.save()
            print('superuser created with',superuser_name,superuser_pass,superuser_email)

            print('creating default resturant')
            restaurant = RestaurantFactory.create(opening_time=12, closing_time=24)
            restaurant.save()
            for group_name in GROUPS:

                new_group, created = Group.objects.get_or_create(name=group_name)

                # Loop models in group
                for app_model in GROUPS[group_name]:

                    # Loop permissions in group/model
                    for permission_name in GROUPS[group_name][app_model]:

                        # Generate permission name as Django would generate it
                        name = "Can {} {}".format(permission_name, app_model)
                        print("Creating {}".format(name))

                        try:

                            model_add_perm = Permission.objects.get(name=name)
                        except Permission.DoesNotExist:
                            logging.warning("Permission not found with name '{}'.".format(name))
                            continue
                        except Exception as ex:
                            logging.warning("Permission retrieving error '{}'.".format(name))
                            logging.error(ex)
                            continue

                        new_group.permissions.add(model_add_perm)

                for user_name in USERS:

                    new_user = None
                    if user_name == "1111":
                        new_user, created = User.objects.get_or_create(staffnumber=user_name, is_staff=True,
                                                                       email=USERS[user_name][1])
                    else:
                        new_user, created = User.objects.get_or_create(staffnumber=user_name, is_staff=True,
                                                                       email=USERS[user_name][1])

                    new_user.set_password(USERS[user_name][2])
                    new_user.save()

                    if USERS[user_name][0] == str(new_group):
                        new_user.groups.add(new_group)
                        #new_group.user_set.add(new_user)

                        print("Adding {} to {}".format(user_name, new_group))

            #admin_group, admin_created = Group.objects.get_or_create(name='Admin')
            #perm = Permission.objects.get_or_create(name='Can delete table')
            #admin_group.permissions.add(perm)
            #admin_group.user_set.add()

            #employee_group, employee_created = Group.objects.get_or_create(name='Employee')
            logging.info("default permission setup completed")

        except Exception as ex:
            logging.error(ex)
            logging.error(traceback.format_exc())
            raise CommandError('Startup command initalization failed.')