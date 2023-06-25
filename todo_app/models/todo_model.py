# -*- coding: utf-8 -*-

from openerp import models, fields

class ToDoTask(models.Model):
    _name = "todo.task"
    
    name = fields.Char('Description', required=True)
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)
    
