from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_history_ids = fields.One2many('sale.task.history','order_id',string='Tasks')

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        products = []
        for product in vals.get('order_line'):
            products.append(product[2]['product_id'])
        task_history_obj = self.env['sale.task.history']
        tasks = []
        unique_task = []
        product_ids = self.env['product.product'].search([('id', 'in', products)])
        for curr_product in product_ids:
            for task in curr_product.task_ids:
                tasks.append(task.id)
        if tasks:
            unique_task = set(tasks)
        for curr_task in unique_task:
            vals = {'order_id':res.id , 'sale_task_id':curr_task}
            task_history_obj.sudo().create(vals)
        return res


    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        products = []
        if vals.get('order_line'):
            for product in vals.get('order_line'):
                if product[2]:
                    products.append(product[2]['product_id'])
        task_history_obj = self.env['sale.task.history']
        tasks = []
        unique_task = []
        old_tasks = [] 
        sale_task_history = self.env['sale.task.history'].search([('order_id', '=', self.id)])
        for task_history in sale_task_history:
            old_tasks.append(task_history.sale_task_id)
        product_ids = self.env['product.product'].search([('id', 'in', products)])
        for curr_product in product_ids:
            for task in curr_product.task_ids:
                if task not in old_tasks:
                    tasks.append(task.id)
        if tasks:
            unique_task = set(tasks)
        for curr_task in unique_task:
            vals = {'order_id':self.id , 'sale_task_id':curr_task}
            task_history_obj.sudo().create(vals)
        return res


    def action_confirm(self):
        tasks = []
        for task in self:
            for record in task.task_history_ids:
                if record:
                    if not record.done:
                        raise ValidationError(_('Please mark all tasks done to confirm this order!'))            
        res = super(SaleOrder, self).action_confirm() 
        return res







 


