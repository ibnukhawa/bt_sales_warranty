
from odoo import api, fields, models, _
from datetime import datetime,timedelta,time

class Service(models.Model):
    
    _name = "service.details"
    _description = "Service Record"
    _inherit = ['mail.thread']
    _rec_name = 'warranty_id'
     
    warranty_id = fields.Many2one('warranty.details',string='Warranty')
    product_id = fields.Many2one('product.product',string='Product', related='warranty_id.product_id')
    sno = fields.Char(string='Serial No' , related='warranty_id.sno')
    warranty_end_date = fields.Date(string='Warranty End Date', related='warranty_id.warranty_end_date')
    date_received = fields.Date(string='Received Date',track_visibility='onchange',default=datetime.now())
    complaint_note = fields.Text(string='Description',track_visibility='onchange')
    service_note = fields.Text(string='Service Note')
    return_date = fields.Date(string='Date of Return',track_visibility='onchange')
    warranty_expired = fields.Boolean(string = "Warranty Expired", track_visibility='onchange')
    responsible_id = fields.Many2one(comodel_name="res.users", 
        string="Responsible", required=True)
    state = fields.Selection([('registered','Registered'),('approved','Approved'),
                              ('inservice','In Service'),
                              ('done','Service Done'),
                              ('delivered','Delivered'),
                              ('cancel', 'Cancelled'),], default='registered',string = "Status",track_visibility='onchange')
    
    @api.multi
    def action_state_process(self,vals):
        for service in self:
            service.state = 'inservice'

    @api.multi
    def action_state_approve(self,vals):
        for service in self:
            service.state = 'approved'
        
    @api.multi
    def action_state_done(self,vals):
        for service in self:
            service.state = 'done'
        
    @api.multi
    def action_state_deliver(self,vals):
        for service in self:
            service.state = 'delivered'
    
    @api.multi
    def action_state_cancel(self,vals):
        for service in self:
            service.warranty_expired = True
            service.state = 'registered'
            
        
    # vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:    
                   