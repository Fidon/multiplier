$(function () {
    $("#fleet_menu_btn").click();

    
    $("#container .info_driver ul li a").click(function (e) { 
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .info_driver .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    $("#adnew_driver_form").submit(function (e) { 
        e.preventDefault();

        var formData = new FormData();
        var describe = $.trim($("#drv_describe").val());

        formData.append("fullname", $.trim($("#drv_fullname").val()));
        formData.append("licenseNum", $.trim($("#drv_license").val()));
        formData.append("phone", $.trim($("#drv_phone").val()));

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
                $("#drv_cancel_btn").hide();
                $("#drv_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#drv_cancel_btn").show();
                $("#drv_submit_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#new_driver_canvas').animate({ scrollTop: 0 }, 'slow');
                $("#adnew_driver_form .formsms").html(fdback);

                if(response.success) {
                    $("#adnew_driver_form")[0].reset();
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});