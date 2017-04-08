$(document).ready(function() {
    $('#search-form').on('submit', function (e) {
        e.preventDefault();
        tag_name = $('#search-tag').val();

        if (tag_name === "") return;

        // search tag
        url = $('#search-form').attr('action').replace('TAG_NAME', tag_name);
        window.location = url;
    });

    $('#filter-form').on('change', function (e) {
        filters = [];
        $('#filter-form input:checked').each(function () {
            filters.push($(this).val());
        });

        query = '?filters=' + filters.join(',');
        window.location = query;
    });
});