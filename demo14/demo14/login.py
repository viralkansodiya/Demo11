import frappe
from frappe.auth import LoginManager
import json

@frappe.whitelist(allow_guest =True)
def login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(user  = usr, pwd = pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response['message'] = {
            "succes_key" : 0,
            "message" : "Authentication Error!"
        }
        return

    api_generate = generate_api_key(frappe.session.user)
    user = frappe.get_doc("User", frappe.session.user)

    frappe.response["message"] = {
        "succes_key" : 1,
        "message" : "Authentication Successful",
        "sid" : frappe.session.sid,
        "api_key" : user.api_key,
        "api_secret" : api_generate,
        "username" : user.username,
        "email": user.email
    }

def generate_api_key(user):
    user_detail = frappe.get_doc("User", user)
    api_secret = frappe.generate_hash(length =15)

    if not user_detail.api_key:
        api_key = frappe.generate_hash(length=15)
        user_detail.api_key = api_key
    
    user_detail.api_secret = api_secret
    user_detail.save()

    return api_secret 