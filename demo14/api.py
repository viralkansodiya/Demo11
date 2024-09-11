import frappe

@frappe.whitelist()
def open_stock_entry_(type_):
    doc = frappe.new_doc('Stock Entry')
    doc.stock_entry_type = "Material Transfer"
    doc.custom_entry_type = type_
    return doc

import frappe

@frappe.whitelist()
def check_search_bar_per(user):
    roles = frappe.get_roles(user)
    from frappe.core.doctype.role.role import desk_properties
    for row in roles:
        role_doc = frappe.db.get_value("Role", row, "search_bar")
        if role_doc:
            return True
    return False