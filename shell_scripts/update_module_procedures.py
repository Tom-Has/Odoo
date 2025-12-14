# check which Enterprise modules are installed
modules_ee = env['ir.module.module'].search([('license','=','OEEL-1')])
for m in modules_ee:
    print(f"Name Modul: {m.name} / Installationsstatus: {m.state}")

# uninstall a specific module
env['ir.module.module'].search([('name','=','module_name')]).button_uninstall()
