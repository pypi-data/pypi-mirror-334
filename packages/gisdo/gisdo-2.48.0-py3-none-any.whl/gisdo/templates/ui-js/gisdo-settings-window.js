
var zipXML = Ext.getCmp('{{ component.zip_xml.client_id }}'),
    asyncSend = Ext.getCmp('{{ component.async_send.client_id }}');

zipXML.on('check',
    function(self, checked){
        if (checked) {
            asyncSend.show();
        } else {
            asyncSend.hide();
            asyncSend.checked = false;
        }
    }
);

// Если рендеринге окна разрешена архивация, то сразу же нужно отобразить
// checkBox с асинхронной отправкой. События с рендерингом не срабатывают.
(function(){
    if (zipXML.checked) {
        asyncSend.show();
    }
})()