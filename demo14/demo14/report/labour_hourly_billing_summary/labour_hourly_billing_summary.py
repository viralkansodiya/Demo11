# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_column(filters)
	return columns, data

def get_data(filters):

	conditions = ''
	if filters.get("from_date"):
		conditions += f" and ec.attendance_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" and ec.attendance_date <= '{filters.get('to_date')}'"
	if filters.get("employee"):
		conditions += f" and emp.employee = '{filters.get('employee')}'"


	data = frappe.db.sql(f""" Select ec.in_time, ec.out_time, ec.working_hours,
							emp.employee_name, emp.name, emp.custom_hourly_rate,
							(ec.working_hours - emp.custom_total_allowancehours) as efective_hours,
							emp.custom_total_allowancehours , ((ec.working_hours - emp.custom_total_allowancehours) * emp.custom_hourly_rate) as per_day

							From `tabAttendance` as ec
							Left join `tabEmployee` as emp ON emp.name = ec.employee

							Where ec.status = "Present" {conditions}
	""",as_dict = 1)

	return data

def get_column(filters):
	return [
		{
			"label": _("Employee"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 180,
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("In Time"),
			"fieldname": "in_time",
			"fieldtype": "Datetime",
			"width": 180,
		},
		{
			"label": _("Out Time"),
			"fieldname": "out_time",
			"fieldtype": "Datetime",
			"width": 180,
		},
		{
			"label": _("Working Hours"),
			"fieldname": "working_hours",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Time Allowance"),
			"fieldname": "custom_total_allowancehours",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Effective Hrs"),
			"fieldname": "efective_hours",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Per Hour rate"),
			"fieldname": "custom_hourly_rate",
			"fieldtype": "Currency",
			"width": 180,
		},
		{
			"label": _("Per day Payment"),
			"fieldname": "per_day",
			"fieldtype": "Currency",
			"width": 180,
		},
	]