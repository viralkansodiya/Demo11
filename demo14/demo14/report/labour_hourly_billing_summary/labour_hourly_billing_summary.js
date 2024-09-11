// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labour Hourly Billing Summary"] = {
	"filters": [
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": __("Employee"),
			"options": "Employee",
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
	]
};
