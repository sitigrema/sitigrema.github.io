requirejs.config({
    appDir: ".",
    baseUrl: "js",
    paths: {
        'jquery': ['/static/js/jquery.min'],
        'bootstrap': ['/static/js/bootstrap.min'],
        'social': ['/static/js/social']
    },
    shim: {
        'bootstrap' : ['jquery']
    }
});

require(['jquery', 'bootstrap', 'social'], function($) {
    console.log("Loaded :)");
    return {};
});
