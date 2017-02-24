#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

from django import template

register = template.Library()

@register.filter
def mongo_id(value):
    return value.get('_id', '')


@register.assignment_tag
def define(val=None):
  return val

@register.simple_tag
def get_value(dic,key):
    try:
        return dic[key]
    except:
        return " "

# register.filter(mongo_id)
