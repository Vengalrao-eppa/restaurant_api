Write A backend API for an exclusive restaraunt, that does the following:

- Allows restaraunt owners to make their menu in Django Admin (data modelling does not need to be too elaborate, see example models below)
- Allows customers to place an order over the rest API
- Does not allow more than 1 order per table, per day

Please additionally adhere to the following constraints:

 ## Packages/Technologies that MUST be used
  - pytest
  - Django
  - Django Rest Framework

## Make sure that
  - You include a README.md explaining how to run the project
  - You Include your dependencies (e.g requirements.txt Pipfile)
  - You have at least 1 test
  - Your code passes the flake8 static code checker

## Stretch goals
  - Ensure the app runs in a docker container with & docker-compose
  - Use postgres as the DB backend 
  - Explain (on the call how & where you might deploy such an application)
  - Use a custom Django user model (extending AbstractUser)
  - Add in authentication for the REST API
  - Ensure a user can edit their order, but only if they created it to begin with

### Sample data models
Here are some example Data Models to get you started, its just sample code, so not confirmed to be correct, feel to change as 
necessary, move into different apps etc.

```python

from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=50)

class Menu(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    menu = models.ManyToManyField(Menu)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

```
