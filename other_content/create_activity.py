record.activity_schedule('mail.mail_activity_data_todo', activity_deadline, employee.name + ' - Bitte lesen', **{
          'user_id': employee.user_id.id
        })

record.sale_order_id.activity_schedule('mail.mail_activity_data_todo', record.planned_date_begin, record.sale_order_id.user_id.name + ' Bitte Projekt abwickeln!', **{'user_id': record.sale_order_id.user_id.id})

task.sale_order_id.activity_schedule('mail.mail_activity_data_todo', task.planned_date_begin, task.sale_order_id.user_id.name + ' Bitte Projekt abwickeln!', **{'user_id': task.sale_order_id.user_id.id})

record.sale_order_id.activity_schedule('mail.mail_activity_data_todo', record.planned_date_begin, record.sale_order_id.user_id.name + ' Bitte Projekt abwickeln!', **{'user_id': env.ref('base.partner_root').id})

# Plane die Aktivität
record.sale_order_id.activity_schedule(
    'mail.mail_activity_data_todo', 
    record.planned_date_begin, 
    'Bitte Projekt abwickeln!', 
    **{'user_id': record.sale_order_id.user_id.id}
)

# Erstelle eine Nachricht im Chatter mit Odoobot { env.ref('base.partner_root').id } als Absender
env['mail.message'].create({
    'model': 'sale.order',
    'res_id': record.sale_order_id.id,
    'body': 'Es gibt eine neue Aktivität für ' + record.sale_order_id.user_id.name + '.',
    'message_type': 'notification',
    'subtype_id': env.ref('mail.mt_note').id,
    'author_id': env.ref('base.partner_root').id,
})
