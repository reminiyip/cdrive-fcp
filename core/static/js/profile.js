function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#preview-avatar').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#avatar-input input").change(function(){
    readURL(this);
});