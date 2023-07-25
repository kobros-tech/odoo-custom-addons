# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64


class PrintoutWizard(models.TransientModel):
    _name = 'printout.wizard'
    _description = 'Printout Wizard'

    printout_type = fields.Selection([
        ('boiler', 'Boiler Printout'),
        ('compressor', 'Compressor Printout'),
        ('panel', 'Panel Printout'),
        ('daily_running_1','Daily Running Report Printout 1'),
        ('daily_running_2','Daily Running Report Printout 2'),
        ('repaire_request','طلب إصلاج'),
        ('equipment_life_cycle','سجل حياة معدة'),
        
        ],
        string='Printout Type', required=True)
    def get_engineer_managers(self):
        mangers = self.env['res.users'].search([('is_engineering_manager','=',True)])
        return mangers.ids
    engineering_managers = fields.Many2many('res.users', default=get_engineer_managers)
    def action_proceed(self):

        pdf_name = ''
        if self.printout_type == 'boiler':
            report_pdf = self.env['ir.actions.report']._render_qweb_pdf("maintenance_printouts.account_maintenance_report_x", self.id)
            pdf_name = 'OPERATION BOILER REPORT.pdf'
        elif self.printout_type == 'daily_running_1':
            report_pdf = self.env['ir.actions.report']._render_qweb_pdf("maintenance_printouts.account_maintenance_running_report_1", self.id)
            pdf_name = 'التقرير الوردية الاولي لتشغيل محطة التبريد.pdf'
        elif self.printout_type == 'daily_running_2':
            report_pdf = self.env['ir.actions.report']._render_qweb_pdf("maintenance_printouts.account_maintenance_running_report_2", self.id)
            pdf_name = 'التقرير الوردية الثانية لتشغيل محطة التبريد.pdf'
       

       
        attachment_id = self.env['wizard.print.report'].create({
            'pdf_report': pdf_name or (dict(self._fields['printout_type'].selection).get(self.printout_type) + '.pdf'),
            'report_file': base64.b64encode(report_pdf[0]),
        })

        return {
            'name': _('Notification'),
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.print.report',
            'res_id': attachment_id.id,
            'data': None,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }        


class WizardPrintReport(models.TransientModel):
    _name = 'wizard.print.report'
    _description = 'wizard Print PDF report'
  
    pdf_report = fields.Char('File Name', size=64)
    report_file = fields.Binary('Prepared File', readonly=True)

