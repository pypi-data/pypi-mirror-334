var indexesField = Ext.getCmp('{{component.indexes.client_id}}');

win.on('beforeshow', function(){
    indexesField.validate();
});
