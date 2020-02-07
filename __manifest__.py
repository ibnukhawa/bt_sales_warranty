{
    'name': 'After Sales Innograph',
    'version': '0.1',
    'author' : 'BroadTech IT Solutions Pvt Ltd and Edited by Yabes Dwi Nugroho',
    'category': 'Sales',
    'license':'AGPL-3',
    'summary' : 'Sales Warranty ',
    'description': """
The module helps to manage the warranty details and service information of products sold to customers and thus smoothen the after sales activities.
    """,
    'website': 'http://www.broadtech-innovations.com',
    'depends': ['sale','product'],
    'data': [
        'data/warranty_name_sequence.xml',
        'data/warranty_expire_scheduler.xml',
        'wizard/warranty_extention.xml',
        'views/warranty_record_view.xml',
        'views/service_record_view.xml',
        'views/campaign_record_view.xml',
        'views/sale_quotation.xml',
        # 'views/sale_task_analysis.xml',
        # 'views/sale_task_view.xml',
        'report/warranty_report.xml',
        'report/warranty_detail_report.xml',
        #'security/ir.model.access.csv',
        #'views/security_group.xml'
    ],
    'images': ['static/description/bt_sales_warranty_banner.jpg'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
