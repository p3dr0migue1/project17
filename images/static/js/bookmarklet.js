(function() {
    var jquery_version = '2.1.4';
    var site_url = 'http://127.0.0.1:8000/';
    var static_url = site_url + 'static/';
    var min_width = 100;

    function bookmarklet(msg) {
        // load css
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
        });
        jQuery('head').append(css);

        // load HTML
        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
        jQuery('body').append(box_html);

        // close event
        jQuery('#bookmarklet #close').click(function() {
            jQuery('#bookmarklet').remove();
        });

    };

    if (typeof window.jQuery != 'undefined') {
        bookmarklet();
    } else {
        // check for conflicts
        var conflict = typeof window.$ != 'undefined';
        // create the script and point to Google API
        var script = document.createElement('script')
        script.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' + jquery_version)
    }
})