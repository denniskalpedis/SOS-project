# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_and_registration.models import Users

from django.db import models

# Create your models here.
class BuyGroupManager(models.Manager):
    def validate(self, data):
        errors = []
        if self.filter(name=data['name']).count() > 0:
            errors.append("Group name already taken!")
        return errors

class InventoryManager(models.Manager):
    def validate(self, data):
        errors= []
        if  not len(data['min']) or not len(data['max']) or not len(data['count']) or not len(data['measurment']) or not len(data['item']):
            errors.append('All fields must be filled out.')
        return errors


class BuyGroup(models.Model):
    name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    admin=models.ForeignKey(Users, related_name="group")
    tas=models.ManyToManyField(Users, related_name="ta_groups_joined", blank=True)
    users=models.ManyToManyField(Users, related_name="user_groups_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BuyGroupManager()
    def __str__(self):
        return self.name

class Items(models.Model):
    item_name= models.CharField(max_length=255)
    voters = models.ManyToManyField(Users, related_name="votes")
    picture = models.CharField(max_length=255) # to be changed and figured out
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    buy_group = models.ForeignKey(BuyGroup, related_name='items')
    def __str__(self):
        return self.item_name

class Inventory(models.Model):
    count = models.IntegerField()
    item = models.ForeignKey(Items, related_name="stock")
    unit = models.CharField(max_length=255)
    max_inventory = models.IntegerField(blank=True)
    min_inventory = models.IntegerField(blank=True)
    buy_group = models.ForeignKey(BuyGroup, related_name='inventory')
    objects = InventoryManager()
    def __str__(self):
        return self.count

