# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64
from num2words import num2words


class AccountPayment(models.Model):
    _inherit = 'account.payment'


    total_in_words = fields.Char(string='Total in words',
                                 compute='_get_number_string')



    @api.depends('amount_total')
    def _get_number_string(self):
        for rec in self:

            # Enter your amount here to convert
            amount = "{:.2f}".format(round(rec.amount_total, 2))

            split_num = str(amount).split('.')

            pounds = int(split_num[0])
            cents = int(split_num[1])
            lang = rec.partner_id.lang or 'ar_001'  # ar_001 #en_US
            currency = rec.currency_id.name  # EGP #EUR #JPY #USD

            currency_data = {
                'ar_001': ['مبلغ وقدره', 'و', 'صفر', 'فقط لاغير'],
                'en_US': ['Amount of', 'and', 'zero', 'only'],
                'EGPar_001': ['جنيه مصري', 'قرشاً'],
                'EGPen_US': ['egyptian Pound', 'piastre'],
                'USDar_001': ['دولار أمريكي', 'سنت'],
                'USDen_US': ['american dollar', 'cent'],
                'EURar_001': ['يورو اوروبي', 'سنت'],
                'EURen_US': ['european euro', 'cent'],
                'JPYar_001': ['ين ياباني', 'سن'],
                'JPYen_US': ['japanese yen', 'sen'],
                'SARen_US': ['riyal', 'halalas'],
            }

            real_in_words = num2words(float(pounds), lang=lang)
            helala_in_words = num2words(float(cents), lang=lang)


            total_in_words = "%s " % currency_data.get(lang)[0]+real_in_words + " %s" % currency_data.get(currency+lang)[0] +\
                ((" %s " % currency_data.get(lang)[1] + helala_in_words + " %s" % currency_data.get(currency+lang)[1])
                 if helala_in_words != '%s' % currency_data.get(lang)[2] else "") + " %s" % currency_data.get(lang)[3]

            rec.total_in_words = total_in_words   
    
   