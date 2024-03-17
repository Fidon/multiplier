$(function () {
    $("#fleet_menu_btn").click();

    // Tabs
    $("#container .info_trailer ul li a").click(function (e) { 
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .info_trailer .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    $("#new_trailer_form").submit(function (e) { 
        e.preventDefault();

        var formData = new FormData();
        var describe = $.trim($("#trl_describe").val());

        formData.append("regnumber", $.trim($("#trl_regnumber").val()));
        formData.append("trailerType", $("#trl_type").val());
        if(describe.length > 0) { formData.append("describe", describe) }

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            dataType: 'json',
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            beforeSend: function() {
                $("#trl_cancel_btn").hide();
                $("#trl_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#trl_cancel_btn").show();
                $("#trl_submit_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#new_trailer_canvas').animate({ scrollTop: 0 }, 'slow');
                $("#new_trailer_form .formsms").html(fdback);
                
                if(response.success) {
                    $("#new_trailer_form")[0].reset();
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});