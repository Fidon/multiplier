$(function () {
    $("#fleet_menu_btn").click();

    // Tabs
    $("#container .info_truck ul li a").click(function (e) {
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .info_truck .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    $("#addnew_truck_form").submit(function (e) { 
        e.preventDefault();

        var formData = new FormData();
        var describe = $.trim($("#trk_describe").val());

        formData.append("regnumber", $.trim($("#trk_regnumber").val()));
        formData.append("truckType", $.trim($("#trk_type").val()));
        formData.append("horseType", $.trim($("#trk_horse").val()));
        formData.append("truckModel", $.trim($("#trk_model").val()));
        formData.append("trailer", $("#trk_trailer").val());
        formData.append("driver", $("#trk_driver").val());

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
                $("#trk_cancel_btn").hide();
                $("#trk_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#trk_cancel_btn").show();
                $("#trk_submit_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#new_truck_canvas').animate({ scrollTop: 0 }, 'slow');
                $("#addnew_truck_form .formsms").html(fdback);

                if(response.success) {
                    $("#addnew_truck_form")[0].reset();
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});