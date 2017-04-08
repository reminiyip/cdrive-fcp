$(document).ready(function() {
    $('#search-form').on('submit', function (e) {
        e.preventDefault();
        tag_name = $('#search-tag').val();

        if (tag_name === "") return;

        // search tag
        url = $('#search-form').attr('action').replace('TAG_NAME', tag_name);
        window.location = url;
    });
});