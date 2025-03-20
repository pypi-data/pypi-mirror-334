var notOnFederalReport = Ext.getCmp('{{ component.not_on_federal_report.client_id }}'),
    relatedToMoEnable = "{{ component.related_to_mo_enable }}" === "True",
    relatedMoPortal = "{{ component.related_mo_portal }}" === "True",
    isNotShowOnPortal = Ext.getCmp('{{ component.is_not_show_on_portal_field.client_id }}'),
    relatedToMo = Ext.getCmp('{{ component.field__related_to_mo_id.client_id }}');

kind_fld.on('change', federalFieldVisibleManage);
relatedToMo.on('change', function (component, newValue, oldValue) {
    if (newValue && relatedMoPortal){
        isNotShowOnPortal.setValue(true);
    }
});
win.on('beforeshow', function(){
    federalFieldVisibleManage();
});

function federalFieldVisibleManage(){
    if (kind_fld.getValue()==douType){
        notOnFederalReport.show();
        if (relatedToMoEnable) {
            relatedToMo.show();
        }else{
            relatedToMo.hide();
        }
    } else {
        notOnFederalReport.hide();
        relatedToMo.hide();
    }
}