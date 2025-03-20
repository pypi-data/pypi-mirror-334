/**
 * Created by fattakhov on 01.10.13.
 */

/**
 * Добавление элемента <object>, содержащего плагин
 * в DOM веб страницы.
 */
var initPluginDOMElement = function() {
    var object = document.createElement('object'),
        hiddenStyle = {
            visibility: 'hidden',
            width: '0px',
            height: '0px',
            margin: '0px',
            padding: '0px'
        };
    object.id = 'cadesplugin';
    object.type = "application/x-cades";
    Ext.apply(object.style, hiddenStyle);

    if (document.body.firstChild){
        document.body.insertBefore(object, document.body.firstChild);
    }
    else {
        document.body.appendChild(object);
    }
  };
if (! document.getElementById('cadesplugin')){ initPluginDOMElement(); }
/**
 * @class CryptoPro
 * @extends Object
 * Класс, инкапсулирующий создание плагинов
 */
CryptoPro = Ext.extend(Object, {
    /**
     * @property constants
     * @type Object
     * Объект содержит настройки плагина по-умолчанию.
     */
    constants: {
        /**
         * @const CADESCOM_CADES_BES
         * @type Number
         *
         */
        CADESCOM_CADES_BES: 1,
        /**
         * @const CAPICOM_CURRENT_USER_STORE
         * @type Number
         *
         */
        CAPICOM_CURRENT_USER_STORE: 2,
        /**
         * @const CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
         * @type Number
         *
         */
        CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED: 2,
        /**
         * @const CAPICOM_CERTIFICATE_FIND_SUBJECT_NAME
         * @type Number
         *
         */
        CAPICOM_CERTIFICATE_FIND_SUBJECT_NAME: 1,
        /**
         * @const CADESCOM_XML_SIGNATURE_TYPE_ENVELOPED
         * @type Number
         * Вложенная подпись.
         */
        CADESCOM_XML_SIGNATURE_TYPE_ENVELOPED: 0,
        /**
         * @const CADESCOM_XML_SIGNATURE_TYPE_ENVELOPING
         * @type Number
         * Оборачивающая подпись
         */
        CADESCOM_XML_SIGNATURE_TYPE_ENVELOPING: 1,
        /**
         * @const CADESCOM_XML_SIGNATURE_TYPE_TEMPLATE
         * @type Number
         * Подпись по шаблону
         */
        CADESCOM_XML_SIGNATURE_TYPE_TEMPLATE: 2,
        CAPICOM_CERTIFICATE_INCLUDE_WHOLE_CHAIN: 1
    },
    /**
     * @property activeXFabric
     * @type Object
     * Фабрика-адаптер для ActiveX компонент
     */
    activeXFabric: {
        CreateObject: function(name) { return new ActiveXObject(name);}
    },
    /**
     * @property pluginsEnum
     * @type Object
     * Перечисление названий плагинов
     */
    pluginsEnum: {
        store:      "CAPICOM.Store",
        cpSigner:   "CAdESCOM.CPSigner",
        signedXML:  "CAdESCOM.SignedXML",
        signedData: "CAdESCOM.CadesSignedData"
    },
    /**
     * Создает обект плагина
     * @constructor
     */
    constructor: function() {
        this.plugin = this.initPlugin();
    },
    /**
     * Инициализация плагина CAdESCOM
     * (http://cpdn.cryptopro.ru/content/cades/plugin-activation.html)
     * @returns: {CAdESCOM plugin}
    */
    initPlugin: function() {
        var result = undefined;
        switch (navigator.appName) {
            case 'Microsoft Internet Explorer':
                result = this.activeXFabric;
                break;
            default:
                result = document.getElementById("cadesplugin");
        }
        return result;
    }
});
function decimalToHexString (number) {
    if (number < 0) { number = 0xFFFFFFFF + number + 1; }
    return number.toString(16).toUpperCase();
}
function getErrorMessage (e) {
    var err = e.message;
    if (!err) { err = e; }
    else if (e.number) { err += " (0x" + decimalToHexString(e.number) + ")"; }
    return err;
}
function showErrorMessage (e) {
    Ext.Msg.alert('Внимание', getErrorMessage(e));
}

var win = Ext.getCmp('{{ component.client_id }}'),
    certsSelectField = Ext.getCmp('{{ component.certs_select_field.client_id }}'),
    textToSignField = Ext.getCmp('{{ component.text_to_sign.client_id }}'),
    signedTextField = Ext.getCmp('{{ component.signed_text.client_id }}'),
    signedXMLField = Ext.getCmp('{{ component.signed_xml.client_id }}'),
    certsStore = certsSelectField.getStore(),
    selectedCertIndex = undefined,

    cryptoProAdapter = new CryptoPro(),
    cryptoProPlugin = cryptoProAdapter.plugin,
    cryptoProPEnum = cryptoProAdapter.pluginsEnum,
    cryptoProConsts = cryptoProAdapter.constants;

var oStore,
    oSigner;

try {
    oStore = cryptoProPlugin.CreateObject(cryptoProPEnum.store);
    oSigner = cryptoProPlugin.CreateObject(cryptoProPEnum.cpSigner);
}
catch (e) {
    showErrorMessage(e);
}
/**
 * Закрыть текущее окно
 */
function cancelForm() {
    win.close();
}
/**
 * Загрузка сертификатов в комбобокс выбора
 */
function loadCerts() {
    oStore.Open();
    var certCount = oStore.Certificates.Count,
        records = [];
    for (var i = 1, j = 0; i <= certCount; i++, j++){
        records[j] = [j, oStore.Certificates.Item(i).SubjectName]
    }
    oStore.Close();
    certsStore.loadData(records);
}
/**
 * Подпись текста
 */
function signText(btn, e) {
    var textToSign = textToSignField.getValue(),
        oSignedData,
        sSignedData;

    if (selectedCertIndex == undefined) {
        Ext.Msg.alert('Внимание', 'Выберите сертификат.');
        return;
    }
    if (! textToSign) {
        Ext.Msg.alert('Внимание', 'Введите текст для подписи.');
        return;
    }
    /**
     * * Подписывание текста.
     */
    oStore.Open();
    oSigner.Certificate = oStore.Certificates.Item(selectedCertIndex + 1);

    oSignedData = cryptoProPlugin.CreateObject(cryptoProPEnum.signedData);
    oSigner.Options = cryptoProConsts.CAPICOM_CERTIFICATE_INCLUDE_WHOLE_CHAIN;
    oSignedData.Content = textToSign;

    try {
        sSignedData = oSignedData.SignCades(oSigner, cryptoProConsts.CADESCOM_CADES_BES);
    }
    catch (e) { showErrorMessage(e); }

    if (sSignedData) {
        signedTextField.setValue(sSignedData)
    }

    oStore.Close();

}
/**
 * Подпись XML
 */
function signXMLText(btn, e) {
    var textToSign = textToSignField.getValue(),
        oSignedXML,
        sSignedXML;

    if (selectedCertIndex == undefined) {
        Ext.Msg.alert('Внимание', 'Выберите сертификат.');
        return;
    }
    if (! textToSign) {
        Ext.Msg.alert('Внимание', 'Введите текст для подписи.');
        return;
    }

    oStore.Open();
    oSigner.Certificate = oStore.Certificates.Item(selectedCertIndex + 1);

    oSignedXML = cryptoProPlugin.CreateObject(cryptoProPEnum.signedXML);
    oSignedXML.Content = textToSign;
    oSignedXML.DigestMethod = "http://www.w3.org/2001/04/xmldsig-more#gostr3411";
    oSignedXML.SignatureMethod = "http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411";
//    oSignedXML.SignatureType = cryptoProConsts.CADESCOM_XML_SIGNATURE_TYPE_ENVELOPING;
//    oSignedXML.SignatureType = cryptoProConsts.CADESCOM_XML_SIGNATURE_TYPE_ENVELOPED;

    try {
        sSignedXML = oSignedXML.Sign(oSigner)
    }
    catch (e) { showErrorMessage(e); }

    if (sSignedXML) {
        signedXMLField.setValue(sSignedXML);
    }
    oStore.Close();
}
/**
 * Запрос на сервер для генерации SOAP
 * запроса
 */
function generateXML(btn, e) {
    var mask = new Ext.LoadMask(win.body);
    mask.show();
    Ext.Ajax.request({
        url: '{{ component.render_soap_request_url }}',
        params: win.actionContextJson || {},
        success: function(res){
            textToSignField.setValue(res.responseText);
        },
        failure: function(res, opts){
            uiAjaxFailMessage();
        },
        callback: function(opt, success, res){
            mask.hide();
        },
        method: 'POST'
    });
}
/**
 * Верификация подписи текста
 */
function verifyText() {}
/**
 * Верификация подписи XML текста
 */
function verifyXMLText() {
    var signedText = signedXMLField.getValue(),
        oSignedXML,
        signResult;

    if (! signedText) {
        Ext.Msg.alert('Внимание', 'Отсутствует текст XML.');
        return;
    }

    oSignedXML = cryptoProPlugin.CreateObject(cryptoProPEnum.signedXML);
    oSignedXML.DigestMethod = "http://www.w3.org/2001/04/xmldsig-more#gostr3411";
    oSignedXML.SignatureMethod = "http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411";
    oSignedXML.SignatureType = cryptoProConsts.CADESCOM_XML_SIGNATURE_TYPE_ENVELOPING;

    try {
        signResult = oSignedXML.Verify(signedText)
    }
    catch (e) { showErrorMessage(e); }

    if (signResult) {
        Ext.Msg.alert('Результат проверки подписи.', signResult);
    } else {
        Ext.Msg.alert('Ошибка.', 'Ошибка при верификации');
    }

}
/**
 * Обработчик выбора сертификата
 */
function selectCert(el, rec, index){
    if (index != undefined) {
        selectedCertIndex = index;
    }
}
/**
 * Хэндлер навешан на окно при показе,
 * так как MessageBox в уведомлением отрабатывает раньше,
 * чем открывается само окно.
 */
win.on('show', function(){
    if (oStore && oSigner){ loadCerts(); }
    else {
        Ext.Msg.show({
            title: 'Внимание',
            msg: ('Не найден \'КриптоПро ЭЦП Browser plug-in.\'<br>Скачайте и установите <a href="http://www.cryptopro.ru/products/cades/plugin/get">этот</a> плагин.<br>Если плагин выключен, включите его в настройках браузера.'),
            buttons: Ext.Msg.OK,
            icon: Ext.Msg.WARNING,
            scope: win,
            closable: false,
            fn: function(btn, text, opt) { cancelForm(); }
        });
    }
});