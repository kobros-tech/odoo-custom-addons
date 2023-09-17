# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    force_date = fields.Datetime(string="Force Date", required=True)

    def button_validate(self):
        for rec in self:
            if rec.force_date and rec.force_date != rec.scheduled_date:
                rec.write({'scheduled_date': rec.force_date,
                           'date_done': rec.force_date})
        res = super(StockPicking, self).button_validate()
        for rec in self:
            if rec.force_date and rec.force_date != rec.date_done:
                rec.write({'date_done': rec.force_date})
        return res
