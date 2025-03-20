Ext.Ajax.timeout = 1000*60*2*6000

var win = Ext.getCmp('{{ component.client_id }}'),
    unitsTree = Ext.getCmp('{{ component.units_tree.client_id }}'),
    reportDataURL = '{{ component.report_form_row_data_url }}',
    reportFormId = win.actionContextJson.id,
    winGrids;
/**
 * Рекурсивное получение контролов
 * @param items
 */
var getGrids = function(items){
    var grids = [];
    for (var i = 0; i < items.getCount(); i++){
        var control = items.get(i);
        if (control instanceof Ext.m3.GridPanel){
            grids.push(control);
        } else if (control instanceof Ext.Container && control.items != undefined) {
            grids = grids.concat(getGrids(control.items));
        }
    }
    return grids;
};
winGrids = getGrids(win.items);
/**
 * Обработка клика на дереве учреждений
 */
unitsTree.on('click', function(node, e){
    getReportData(node);
});
/**
 * Получение данных по учреждению
 * @param node Учреждение в дереве
 */
function getReportData(node){
    var mask = new Ext.LoadMask(win.body,
        {msg: 'Загрузка данных для учреждения ' + node.attributes.display });
    mask.show();
    Ext.Ajax.request({
        url: reportDataURL,
        params: {
            report_form_id: reportFormId,
            unit_id: node.id
        },
        success: function(res, opt){
            var data = Ext.decode(res.responseText);
            if (data.message){
                smart_eval(res.responseText);
            }
            else {applyDataToForm(data);}
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
        }
    });
}
/**
 * Загрузка данных в окно
 * @param data
 */
function applyDataToForm(data){
    for(var k = 0, gLength = winGrids.length; k < gLength; k++){
        winGrids[k].store.loadData(data[winGrids[k].name]);
    }
}
/**
 * Закрытие окна
 */
function closeWindow(btn, e){
    win.close();
}
/**
 * Формирование отчета в Excel
 */
function saveInExcel(btn, e){

    var node = unitsTree.getSelectionModel().getSelectedNode();
    if (!node) {return;}
    var mask = new Ext.LoadMask(win.body);
    mask.show();
    Ext.Ajax.request({
        url: '{{ component.excel_url }}',
        params: {
            unit_id: node.id,
            report_id: reportFormId
        },
        success: function(res, opt){
            smart_eval(res.responseText);
        },
        callback: function(opt, success, res){
            mask.hide();
       }
    });
}
/**
 * Отправка отчета в Вэб-сервис
 */
function sendReport(btn, e){
    var mask = new Ext.LoadMask(win.body);
    mask.show();
    Ext.Ajax.request({
        url: '{{ component.send_url }}',
        params: {
            report_id: reportFormId
        },
        success: function(res, opt){
            smart_eval(res.responseText);
        },
        callback: function(opt, success, res){
            mask.hide();
        }
    });
}
