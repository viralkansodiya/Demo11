import frappe
data = {
    "user":"vignesh@kingstech.com.sg",
    "location":"Warehouse 1",
    "rfif_list":[
            "RFID-4321UV-65EF",
            "RFID-8765WX-43GH",
            "RFID-7890EF-09MN",
            "RFID-1234XY-78AB",
            "RFID-2109IJ-76QR",
            "RFID-0987KL-54ST"
    ]   
}

@frappe.whitelist(allow_guest=True)
def get_total_asset():
    data = frappe.request.json
    user = data.get("user")
    warehouse = data.get("location")

    if not user:
        frappe.response["message"]={
            "succes_key":0,
            "error_msg":"User ID Missing"
        }
        return

    if not warehouse:
        frappe.response["message"]={
            "succes_key":0,
            "error_msg":"arg warehouse missing"
        }
        return

    serial_no = frappe.db.sql(f"""
            Select sn.custom_rfid_asset_tag as asset_tag_no, sn.custom_custodian as custodian, sn.name as serial_no, sn.item_code, w.warehouse_name
            From `tabSerial No` as sn
            Left Join `tabWarehouse` as w ON w.name = sn.warehouse
            Where custom_custodian = '{user}' and w.warehouse_name = '{warehouse}'
    """,as_dict=1)

    total_asset = len(serial_no)
    final_data = {}
    rfid =[]
    
    for row in serial_no:
        rfid.append(row.asset_tag_no)

    final_data.update({"total" : total_asset})
    final_data.update({"rfids" : rfid })

    frappe.response["message"]={
        "succes_key":1,
        "data":final_data
    }

    return


@frappe.whitelist(allow_guest=True)
def get_asset_details():
    data = frappe.request.json
    user = data.get("user")
    warehouse = data.get("location")
    rfid_list = data.get("rfif_list")

    if not user:
        frappe.response["message"]={
            "succes_key":0,
            "error_msg":"User ID Missing"
        }
        return

    if not warehouse:
        frappe.response["message"]={
            "succes_key":0,
            "error_msg":"arg warehouse missing"
        }
        return

    serial_no = frappe.db.sql(f"""
            Select sn.custom_rfid_asset_tag as asset_tag_no, sn.custom_custodian as custodian, sn.name as serial_no, sn.item_code, w.warehouse_name
            From `tabSerial No` as sn
            Left Join `tabWarehouse` as w ON w.name = sn.warehouse
            Where custom_custodian = '{user}' and w.warehouse_name = '{warehouse}'
    """,as_dict=1) 

    total_asset = len(serial_no)
    final_data = {}
    final_data.update({"total" : total_asset})
    
    found_map = {}
    all_rfid = []
    not_found = []
    for row in serial_no:
        found_map[row.asset_tag_no] = row
        all_rfid.append(row.asset_tag_no)
        if row.asset_tag_no not in rfid_list:
            not_found.append(row.asset_tag_no)
    
    found = []
    extra = []
    for row in rfid_list:
        if found_map.get(row):
            found.append(row)
        else:
            extra.append(row)
        
    final_data.update({"total_found" : len(found)})
    final_data.update({"rfid_found" : found})
    final_data.update({"total_not_found":len(not_found)})
    final_data.update({"rfid_not_found" : not_found})
    final_data.update({"total_extra":len(extra)})
    final_data.update({"extra_rfid" : extra})
    


    frappe.response["message"]={
        "succes_key":1,
        "data":final_data
    }

    return

import random
import string


@frappe.whitelist(allow_guest=True)
def get_warehouse_list():
    frappe.session.user = "Administrator"
    warehouse_list =  frappe.db.get_list("Warehouse", {"company":"Nexora Trading Sdn Bhd", "disabled":0}, "warehouse_name", pluck="warehouse_name")
    frappe.response["message"]={
        "succes_key":1,
        "data":warehouse_list
    }


def generate_unique_code(length=10):
    # Generates a random alphanumeric code
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_multiple_unique_codes(count=20, length=10):
    # Generates a set of unique codes to ensure no duplicates
    codes = set()
    while len(codes) < count:
        code = generate_unique_code(length)
        codes.add(code)
    return list(codes)

# Generate 20 unique 10-character codes
def get_unic_number():
    doc_list = frappe.db.get_list("Serial No", pluck="name")
    unique_codes = generate_multiple_unique_codes()
    for idx, code in enumerate(unique_codes):
        frappe.db.set_value("Serial No", doc_list[idx], "custom_rfid_asset_tag", code)
