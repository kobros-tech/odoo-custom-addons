# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class AccountMove(models.Model):
    _inherit = "account.move"

    def force_date(self, date):
        for rec in self:
            if isinstance(date, str):
                date = datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)
            sequence_prefix = rec.journal_id.code + "/" + str(date.year) + "/" + str('{:02d}'.format(date.month)) + "/"
            sql = "SELECT MAX(sequence_number) as sequence_number from account_move " \
                  "WHERE sequence_prefix = '%s'" % (sequence_prefix)
            self.env.cr.execute(sql)
            res = self.env.cr.dictfetchone()
            if res['sequence_number']:
                sequence_number = res['sequence_number'] + 1
            else:
                sequence_number = 1
            name = sequence_prefix + "{:04d}".format(sequence_number)
            update_sql = """
            UPDATE account_move 
            SET sequence_prefix = %s,sequence_number = %s,name=%s,date=%s
            WHERE id = %s
            """
            self.env.cr.execute(update_sql, (sequence_prefix, sequence_number, name, date, rec.id))
