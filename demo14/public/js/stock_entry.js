frappe.ui.form.on("Stock Entry", {
    refresh:(frm,cdt,cdn) =>{
        if(frm.doc.custom_entry_type == "Check In"){
            let d = locals[cdt][cdn]
            frm.doc.items.forEach(r => {
                console.log("s")
                frappe.model.get_value("Company", frm.doc.company, 'abbr' , (d)=>{
                    frappe.model.set_value(r.doctype, r.name, 't_warehouse', `Goods In Transit - ${d.abbr}`)
                    frappe.model.set_value(r.doctype, r.name, 's_warehouse', `Stores - ${d.abbr}`)
                   
                })
            });
        }
        if(frm.doc.custom_entry_type == "Check Out"){
            let d = locals[cdt][cdn]
            frm.doc.items.forEach(r => {
                frappe.model.get_value("Company", frm.doc.company, 'abbr' , (d)=>{
                    console.log("s")
                    frappe.model.set_value(r.doctype, r.name, 's_warehouse', `Goods In Transit - ${d.abbr}`)
                    frappe.model.set_value(r.doctype, r.name, 't_warehouse', `Stores - ${d.abbr}`)
                   
                })
            });
        }
    }
})

frappe.ui.form.on('Stock Entry Detail', {
	items_add:function(frm,cdt,cdn){
        let d = locals[cdt][cdn]
        if(frm.doc.custom_entry_type == 'Check In'){
            frappe.model.get_value("Company", frm.doc.company, 'abbr' , (r)=>{
                d.s_warehouse = `Stores - ${r.abbr}`
                d.t_warehouse = `Goods In Transit - ${r.abbr}`
            })
        }
        if(frm.doc.custom_entry_type == 'Check Out'){
            frappe.model.get_value("Company", frm.doc.company, 'abbr' , (r)=>{
                d.t_warehouse = `Stores - ${r.abbr}`
                d.s_warehouse = `Goods In Transit - ${r.abbr}`
            })
        }

    },
});