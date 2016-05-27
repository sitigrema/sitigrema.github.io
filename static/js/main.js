requirejs.config({
    appDir: ".",
    baseUrl: "js",
    paths: {
        'jquery': ['/static/js/jquery.min'],
        'bootstrap': ['/static/js/bootstrap.min']
    },
    shim: {
        /* Set bootstrap dependencies (just jQuery) */
        'bootstrap' : ['jquery']
    }
});

require(['jquery', 'bootstrap'], function($) {
    console.log("Loaded :)");
    return {};
});
