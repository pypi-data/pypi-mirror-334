{% include 'ext-script/ext-dictionary-window-globals.js' %}
/**
 */
var grid = Ext.getCmp('{{ component.grid.client_id }}'),
    sm = grid.getSelectionModel(),
    mask = new Ext.LoadMask(win.body);

function sendReportTask(){
    mask.show();
    Ext.Ajax.request({
        params: {},
        url: '{{ component.build_window_url }}',
        success: function(res, opt){
            smart_eval(res.responseText);
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
        },
        method: 'POST'
    });
}

function gridDblClickHandler(e){
    if (sm.hasSelection()){
        var selectedId = grid.getSelectionModel().getSelected().id;
        mask.show();
        Ext.Ajax.request({
            url: '{{ component.view_window_url }}',
            params: {id: selectedId},
            success: function(res, opt){
                smart_eval(res.responseText);
            },
            callback: function(opt, success, res){
                mask.hide();
            }
        })
    }
}

function settingsWindow(){
    mask.show();
    Ext.Ajax.request({
        params: {},
        url: '{{ component.settings_window_url }}',
        success: function(res, opt){
            smart_eval(res.responseText);
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
        },
        method: 'POST'
    });
}

//Вызов окна параметров отчета "Выгрузка детей по показателю/тегу"
function unloadChildrenByIndex() {
   Ext.Ajax.request({
       params: {},
       url: '{{ component.unload_by_index_window_url }}',
       success: function (res, opt) {
           smart_eval(res.responseText);
       },
       failure: function (res, opt) {
           uiAjaxFailMessage();
       },
       callback: function (opt, success, res) {
           mask.hide();
       },
       method: 'POST'
   });
}
