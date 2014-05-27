"""
This set of factories stores generic things like lists of names and
factories for auth users.
"""
import factory
from django.contrib.auth import get_user_model

BOYS_NAMES = ['Jack', 'Lewis', 'Riley', 'James', 'Logan', 'Daniel',
              'Ethan', 'Harry', 'Alexander', 'Oliver', 'Max', 'Tyler',
              'Aaron', 'Charlie', 'Adam', 'Finlay', 'Alfie', 'Mason',
              'Ryan', 'Liam', 'Lucas']

GIRLS_NAMES = ['Sophie', 'Emily', 'Olivia', 'Ava', 'Lucy', 'Isla',
               'Lily', 'Jessica', 'Amelia', 'Mia', 'Millie', 'Eva',
               'Ellie', 'Chloe', 'Freya', 'Sophia', 'Grace', 'Emma',
               'Hannah', 'Holly']

# Interleave boys and girls names
FIRST_NAMES = [x for y in zip(BOYS_NAMES, GIRLS_NAMES) for x in y]

LAST_NAMES = ['Smith', 'Marshall', 'Brown', 'Stevenson', 'Wilson',
              'Wood', 'Thomson', 'Sutherland', 'Robertson', 'Craig',
              'Campbell', 'Wright', 'Stewart', 'Mckenzie', 'Anderson',
              'Kennedy', 'Macdonald', 'Jones', 'Scott', 'Burns',
              'Reid', 'White', 'Murray', 'Muir', 'Taylor', 'Murphy',
              'Clark', 'Johnstone', 'Mitchell', 'Hughes', 'Ross',
              'Watt', 'Walker', 'Mcmillan', 'Paterson', 'Mcintosh',
              'Young', 'Milne', 'Watson']


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    first_name = factory.Iterator(FIRST_NAMES)
    last_name = factory.Iterator(LAST_NAMES)
    username = factory.LazyAttribute(lambda obj: ('%s %s' % (obj.first_name.lower(), obj.last_name.lower())).replace(" ", "-"))
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.PostGenerationMethodCall('set_password', 'secret')