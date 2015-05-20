var fucus = {
    name: "CQ",
    debug: true,
    greet: function () {
        console.log("Hello from the " + fucus.name + " library.");
    },
    getXmlHttp: function () {
        var xmlhttp;
        if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp = new XMLHttpRequest();
        }
        else {// code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        return xmlhttp;
    },


    /**
     * post a request
     * @param {String} url
     * @param {String} data, after serizlized, look like "name1=value1&name2=value2"
     * @param {Function} callback, callback function after receive the result data
     * @param {Boolean} async or not
     * @return {Void}
     */
    post: function (url, data, callback, async) {
        if (async == null) async = true;
        xmlhttp = this.getXmlHttp();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                callback.call(xmlhttp.responseText);
            }
        }
        xmlhttp.open("POST", url, async);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send(data);
    },
    getInflatData: function (url, jsonId, jsonName, tagName
        ,customizeAttribute, attributeJsonName) {
        var _insertProvinceOption = "";
        var xmlhttp;
        if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp = new XMLHttpRequest();
        }
        else {// code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function () {

            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var jsonData = JSON.parse(xmlhttp.responseText);

                for (var i = 0; i < jsonData.length; i++) {
                    var counter = jsonData[i];

                    console.log(attributeJsonName); 
                    var customizeAttributeString = "";
                    var customizeAttributeValue = "";
                    switch (typeof (counter[attributeJsonName])) {
                        case "string":
                            customizeAttributeValue =  counter[attributeJsonName];
                            console.log("the type is string");
                            break;
                        case "object":
                            customizeAttributeValue = "";
                            for (var j = 0; j < counter[attributeJsonName].length; j++)
                            {
                                customizeAttributeValue += counter[attributeJsonName][j].PATH+" ";
                            }                            
                            console.log("the type is object");
                            break;

                    }
                    customizeAttributeString = customizeAttribute + "='" + customizeAttributeValue + "' ";
                    console.log("the customize attr is " + customizeAttributeString);

                    _insertProvinceOption
                        += "<"+ tagName
                        + " " + customizeAttributeString + "  value='"
                        + counter[jsonId] + "'>"
                        + counter[jsonName] + "</" + tagName + ">"
                    
                }

            }
        }
        xmlhttp.open("POST", url, false);
        xmlhttp.send();
        return _insertProvinceOption;
    },
    inflatTag: function (selectionId, url, jsonId, jsonName, tagName, replace, customizeAttribute, attributeJsonName) {
        data = fucus.getInflatData(url, jsonId, jsonName, tagName, customizeAttribute, attributeJsonName);
        fucus.inflatData(selectionId, data, replace);
    },
    inflatData: function (selectionId, data, replace) {
        if (replace == null) replace = false;
        _provinceSelection = document.getElementById(selectionId);
        if (replace == true) {
            _provinceSelection.innerHTML = "";
        }
        if (fucus.debug) {
            if (_provinceSelection == null) {
                console.log("selection not found");
            }
        }
        _provinceSelection.innerHTML += data;
    },
    inflatSelection: function (selectionId, url, jsonId, jsonName, customizeAttribute, attributeJsonName) {
        fucus.inflatTag(selectionId, url, jsonId, jsonName, "option", customizeAttribute, attributeJsonName);
    },
    inflatList: function (selectionId, url, jsonId, jsonName, replace, customizeAttribute, attributeJsonName) {
        fucus.inflatTag(selectionId, url, jsonId, jsonName, "li", replace, customizeAttribute, attributeJsonName);
    },

    serialize: function (form) {
        if (!form || form.nodeName !== "FORM") {
            return;
        }
        var i, j, q = [];
        for (i = form.elements.length - 1; i >= 0; i = i - 1) {
            if (form.elements[i].name === "") {
                continue;
            }
            switch (form.elements[i].nodeName) {
                case 'INPUT':
                    switch (form.elements[i].type) {
                        case 'text':
                        case 'hidden':
                        case 'password':
                        case 'button':
                        case 'reset':
                        case 'submit':
                            q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                            break;
                        case 'checkbox':
                        case 'radio':
                            if (form.elements[i].checked) {
                                q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                            }
                            break;
                        case 'file':
                            break;
                    }
                    break;
                case 'TEXTAREA':
                    q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                    break;
                case 'SELECT':
                    switch (form.elements[i].type) {
                        case 'select-one':
                            q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                            break;
                        case 'select-multiple':
                            for (j = form.elements[i].options.length - 1; j >= 0; j = j - 1) {
                                if (form.elements[i].options[j].selected) {
                                    q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].options[j].value));
                                }
                            }
                            break;
                    }
                    break;
                case 'BUTTON':
                    switch (form.elements[i].type) {
                        case 'reset':
                        case 'submit':
                        case 'button':
                            q.push(form.elements[i].name + "=" + encodeURIComponent(form.elements[i].value));
                            break;
                    }
                    break;
            }
        }
        return q.join("&");
    },
    setNumber: function (selectId, num) {
        if (num == undefined) {
            n = 1;
        } else {
            n = num;
        }
        selectElement = document.getElementById(selectId);
        selectElement.innerHTML = parseInt(n);
    },
    increaseNumber: function (selectId, num) {
        if (num == undefined) {
            n = 1;
        } else {
            n = num;
        }
        selectElement = document.getElementById(selectId);
        fucus.setNumber(selectId, parseInt(selectElement.innerHTML) + parseInt(n));
    },
    decreaseNumber: function (selectId, num) {
        if (num == undefined) {
            n = 1;
        } else {
            n = num;
        }
        fucus.increaseNumber(selectId, -n);
    }
}