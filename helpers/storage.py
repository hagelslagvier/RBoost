#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from time import gmtime, strftime
from json import loads, dumps


class Storage(OrderedDict):
    def __init__(self, path=None, *args, **kwargs):
        OrderedDict.__init__(self, *args, **kwargs)
        self.path = path
        self.is_dirty = False

    def __setitem__(self, key, value, *args, **kwargs):
       if isinstance(value, str):
           today = strftime("%Y-%m-%d", gmtime())
           result = {"success": 0, "failure": 0, "hint": 0}
           value = [value, {today: result}]

       OrderedDict.__setitem__(self, key, value, *args, **kwargs)
       self.is_dirty = True

    def __delitem__(self, key):
        OrderedDict.__delitem__(self, key)
        self.is_dirty = True

    def __str__(self):
        return dumps(self, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

    def __increase(self, key, action):
        today = strftime("%Y-%m-%d", gmtime())
        value, log = self.__getitem__(key)

        if today not in log:
           result = {"success": 0, "failure": 0, "hint": 0}
           log.update({today: result})

        log[today][action] += 1

    def success(self, key):
        self.__increase(key=key, action="success")

    def failure(self, key):
        self.__increase(key=key, action="failure")

    def hint(self, key):
        self.__increase(key=key, action="hint")

    def load(self, path=None):
        if path:
            self.path = path

        with open(self.path, "r") as file:
           text = file.read()
           self.update(loads(text, object_pairs_hook=OrderedDict))

        self.is_dirty = False

    def dump(self, path=None):
        if self.path is None:
            if path:
                self.path = path
            else:
                today = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
                self.path = "Untitled_" + today
        else:
            if path:
                self.path = path

        with open(self.path, "w") as file:
           text = dumps(self, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
           file.write(text)

        self.is_dirty = False