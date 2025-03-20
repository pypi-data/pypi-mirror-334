Ext.Ajax.timeout = 1000*60*2*6000;
/**
 * Created by fattakhov on 14.10.13.
 */
// todo: отрефакторить
{% include 'ext-script/ext-dictionary-window-globals.js' %}
var unitsTree = Ext.getCmp('{{ component.units_tree.client_id }}'),
    sendBtn = Ext.getCmp('{{ component.send_btn.client_id }}'),
    saveBtn = Ext.getCmp('{{ component.save_btn.client_id }}'),
    reportDataURL = '{{ component.report_form_row_data_url }}',
    sendFormURL = '{{ component.send_form_url }}',
    saveFormRowURL = '{{ component.save_form_row_url }}',
    saveTreeFormRowURL = '{{ component.save_tree_form_row_url }}',
    confirmButtons = {
        general_confirmed:          Ext.getCmp('{{ component.general_approve_btn.client_id }}'),
        applications_confirmed:     Ext.getCmp('{{ component.applications_approve_btn.client_id }}'),
        ch_queue_confirmed:         Ext.getCmp('{{ component.ch_queue_approve_btn.client_id }}'),
        ch_enrolled_confirmed:      Ext.getCmp('{{ component.ch_enrolled_approve_btn.client_id }}'),
        ch_overall_confirmed:       Ext.getCmp('{{ component.ch_overall_approve_btn.client_id }}'),
        vacant_places_confirmed:    Ext.getCmp('{{ component.vacant_places_approve_btn.client_id }}'),
        doo_info_confirmed:         Ext.getCmp('{{ component.doo_info_approve_btn.client_id }}')
    },
    windowTabs = {
        general:        Ext.getCmp('{{ component.tab_general.client_id }}'),
        applications:   Ext.getCmp('{{ component.tab_applications.client_id }}'),
        ch_queue:        Ext.getCmp('{{ component.tab_ch_queue.client_id }}'),
        ch_enrolled:     Ext.getCmp('{{ component.tab_ch_enrolled.client_id }}'),
        ch_overall:      Ext.getCmp('{{ component.tab_ch_overall.client_id }}'),
        vacant_places:   Ext.getCmp('{{ component.tab_vacant_places.client_id }}'),
        doo_info:        Ext.getCmp('{{ component.tab_doo_info.client_id }}')
    },
    reportFormId = win.actionContextJson.id,
    tabsControls = {};

function enableConfirmBtns(){
    for (var btn in confirmButtons){
        confirmButtons[btn].enable();
    }
}
/**
 * Рекурсивное получение контролов
 * @param items
 */
var getControls = function(items){
    var controls = [],
        grids = [];

    for (var i = 0; i < items.getCount(); i++){
        var control = items.get(i);
        if (control instanceof Ext.m3.GridPanel){
            grids.push(control);
        } else  if (control.name && !(control instanceof Ext.Button)){
            controls.push(control);
        } else if (control instanceof Ext.Container && control.items != undefined) {
            var cc = getControls(control.items);
            controls = controls.concat(cc.controls);
            grids = grids.concat(cc.grids);
        }
    }
    return {
        controls: controls,
        grids: grids
    };
};
var winControls = getControls(win.items);

for (var tabName in windowTabs){
    tabsControls[tabName] = getControls(windowTabs[tabName].items);
}
/**
 * Обработка клика на дереве учреждений
 */
unitsTree.on('click', function(node, e){
    getReportData(node);
    confirmFlags.clearFlags();
    enableConfirmBtns();
});
/**
 * Получение данных по учреждению
 * @param node Учреждение в дереве
 */
function getReportData(node){
    var mask = new Ext.LoadMask(win.body,
        {msg: 'Загрузка данных для учреждения ' + node.attributes.display });
    mask.show();
    sendBtn.disable();
    saveBtn.disable();
    Ext.Ajax.request({
        url: reportDataURL,
        params: {
            report_form_id: reportFormId,
            unit_id: node.id
        },
        success: function(res, opt){
            applyDataToForm(Ext.decode(res.responseText));
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
            sendBtn.enable();
            saveBtn.enable();
        }
    });
}
/**
 * Загрузка данных в окно
 * @param data
 */
function applyDataToForm(data){
//    var fields = data.fields;
    for(var j = 0, controls = winControls.controls, cLength = controls.length; j < cLength; j++){
        controls[j].setValue(data[controls[j].name]);
    }

    for(var k = 0, grids = winControls.grids, gLength = grids.length; k < gLength; k++){
        applyDataToGrid(grids[k], data.grids[grids[k].name]);
    }

    for (var btn in confirmButtons){
        confirmButtons[btn].setDisabled(data.buttons[btn]);
    }
}
/**
 * Загрузка данных в грид
 * @param grid
 * @param data
 */
function applyDataToGrid(grid, data){
    var store = grid.store;
    store.removeAt(0);
    store.add(new store.recordType(data));
}
/**
 * Вызов окна-подтверждения при нажатии на кнопку Подтверждения проверки
 * @param msg
 * @param btn
 * @param flagName
 */
function showWarningMsg(msg, btn, flagName){
    btn.disable();
    confirmFlags.confirm(flagName);
    sendTabInfo(windowTabs[flagName], flagName);
}
var confirmFlags = {
    flags: {
        general:        false,
        applications:   false,
        ch_queue:       false,
        ch_enrolled:    false,
        ch_overall:     false,
        vacant_places:  false,
        doo_info:       false
    },
    // количество неподтвержденных табов
    notConfirmed:   7,
    confirm:        function(flagName){
        if (this.flags[flagName] == false){
            this.flags[flagName] = true;
            this.notConfirmed--;
        }
        else {
            console.error(flagName + ' is ' + this.flags[flagName]);
        }
    },
    isConfirmed:    function(){
        return this.notConfirmed == 0
    },
    clearFlags: function(){
        for (var fl in this.flags){
            this.flags[fl] = false;
        }
    }
};
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Общая информация
 * @param btn
 * @param e
 */
function confirmGeneral(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Общей информации?', btn, 'general');
}
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Информация о поданных заявлениях
 * @param btn
 * @param e
 */
function confirmApplications(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Информации о поданных заявлениях?', btn, 'applications');
}
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Информация о детях в очереди
 * @param btn
 * @param e
 */
function confirmChQueue(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Информации о детях в очереди?', btn, 'ch_queue');
}
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Информация о зачисленных детях
 * @param btn
 * @param e
 */
function confirmChEnrolled(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Информации о зачисленных детях?', btn, 'ch_enrolled');
}
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Информация об общем кол-ве детей
 * @param btn
 * @param e
 */
function confirmChOverall(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Информации об общем количестве детей?', btn, 'ch_overall');
}
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Информация о свободных местах
 * @param btn
 * @param e
 */
function confirmVacantPlaces(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Информации о свободных местах?', btn, 'vacant_places');
}
/**
 * Обработчик нажатия кнопки Пометить как проверенное вкладки Информация о ДОО
 * @param btn
 * @param e
 */
function confirmDOOInfo(btn, e){
    showWarningMsg('Вы хотите подтвердить данные Информации о ДОО?', btn, 'doo_info');
}
/**
 * Отправка формы на веб сервис
 * @param btn
 * @param e
 */
function sendForm(btn, e){
    var selectedNode = unitsTree.getSelectionModel().getSelectedNode();
    if (!selectedNode){
        Ext.Msg.show({
            title: 'Внимание',
            msg: 'Пожалуйста, выберите учреждение.',
            icon: Ext.Msg.INFO,
            buttons: Ext.Msg.OK
        });
        return;
    }
    var mask = new Ext.LoadMask(win.body, {msg: 'Отправка данных на сервер'});
    mask.show();
    sendBtn.disable();
    saveBtn.disable();
    Ext.Ajax.request({
        url: sendFormURL,
        params: {
            unit_id: selectedNode.id,
            id: reportFormId
        },
        success: function(res, opt){
            smart_eval(res.responseText);
//            win.close();
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
            sendBtn.enable();
            saveBtn.enable();
        }
    });
}
/**
 * Отправка данных таба по учреждению
 */
function sendTabInfo(tab, tab_name){
    var tabControls = getControls(tab.items),
        mask = new Ext.LoadMask(win.body, {msg: 'Сохранение информации по вкладке'});
    function getDataParams(){
        var data = tabControls.controls.concat(tabControls.grids),
            params = {};
        for (var l = 0, lLength = data.length; l < lLength; l++){
            var cControl = data[l];
            if (cControl.store){
                var cStore = cControl.getStore();
                for (var m = 0; m < cStore.data.items.length; m++){
                    Ext.apply(params, cStore.data.items[m].data);
                }
            }
            else {
                params[cControl.name] = cControl.getValue();
            }
        }
        return params;
    }
    var params = {
        data: getDataParams(),
        tab: tab_name,
        report_form_id: reportFormId,
        unit_id: unitsTree.getSelectionModel().getSelectedNode().id
    };
    mask.show();
    sendBtn.disable();
    saveBtn.disable();
    Ext.Ajax.request({
        url: saveFormRowURL,
        params: {data: Ext.encode(params)},
        success: function(res, opt){
            var response = Ext.decode(res.responseText);
            // fixme: smart_eval не работал с raw строкой, сделал пока так
            if (response.code){
                smart_eval(res.responseText);
            }
            else if (response.report_form_id){
                reportFormId = response.report_form_id;
            }
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
            sendBtn.enable();
            saveBtn.enable();
        }
    });
}
function closeWindow(btn, e){
    win.close();
}
/**
 * Сохранение учреждения и всех дочерних
 * @param btn
 * @param e
 */
function saveTabHandler(btn, e){
    var mask = new Ext.LoadMask(win.body, {msg: 'Запрос на сохранение учреждений...'});
    var params = {
        unit_id: unitsTree.getSelectionModel().getSelectedNode().id,
        report_form_id: reportFormId
    };
    mask.show();
    sendBtn.disable();
    saveBtn.disable();
    Ext.Ajax.request({
        url: saveTreeFormRowURL,
        params: {data: Ext.encode(params)},
        success: function(res, opt){
            var response = Ext.decode(res.responseText);
            // fixme: smart_eval е работал с raw строкой, сделал пока так
            if (response.code){
                smart_eval(res.responseText);
            }
            else {
                if (response.report_form_id){ reportFormId = response.report_form_id; }
                if (response.message) {
                    Ext.Msg.show({
                        msg: response.message,
                        title: 'Сохранение',
                        buttons: Ext.Msg.OK,
                        icon: Ext.Msg.INFO
                    });}
            }
        },
        failure: function(res, opt){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
            sendBtn.enable();
            saveBtn.enable();
        }
    });
}