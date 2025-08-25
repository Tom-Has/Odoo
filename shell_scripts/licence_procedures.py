# check which Enterprise modules are installed
ee_modules = env['ir.module.module'].search([('license','=','OEEL-1')])
for m in ee_modules:
    print(f"Name Modul: {m.name} / Installationsstatus: {m.state}")

# uninstall a specific module
env['ir.module.module'].search([('name','=','module_name')]).button_uninstall()
