/* Initializer.
 * Copyright (C) 2010,2012 shinGETsu Project.
 */

var shingetsu = (function () {
    var _initializer = [];

    var shingetsu = {
        debugMode: false,
        plugins: {},
        uiLang: 'en'
    };

    shingetsu.log = function (arg) {
        if (typeof console == 'object') {
            console.log(arg);
        } else if (shingetsu.debugMode) {
            alert(arg);
        }
    };

    shingetsu.initialize = function (func) {
        _initializer[_initializer.length] = func;
    };
    shingetsu.addInitializer = shingetsu.initialize;

    var _initialize = function () {
        for (var i=0; i < _initializer.length; i++) {
            if (shingetsu.debugMode) {
               _initializer[i]();
               continue;
            }
            try {
               _initializer[i]();
            } catch (e) {
                shingetsu.log(e);
            }
        }
    };

    $(_initialize);

    return shingetsu;
})();
