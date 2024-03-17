$(function () {
    $("#admin_menu_btn").click();

    // Tabs
    $("#container .user_info ul li a").click(function (e) { 
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .user_info .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    $("#new_user_form").submit(function (e) {
        e.preventDefault();
        
        var formData = new FormData();
        var phone = $.trim($("#user_contact").val());
        var comment = $.trim($("#user_comment").val());
        
        formData.append("department", $("#user_dept").val());
        formData.append("fullname", $.trim($("#user_fullname").val()));
        formData.append("username", $.trim($("#user_username").val()));
        formData.append("gender", $("#user_gender").val());
        
        if (phone.length > 0) { formData.append("phone", phone); }
        if (comment.length > 0) { formData.append("comment", comment); }
        
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
                $("#user_cancel_btn").slideDown('fast');
                $("#user_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#user_submit_btn").text("Save").attr('type', 'submit');
                $("#user_cancel_btn").slideUp('fast');
                
                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#new_user_form').animate({ scrollTop: 0 }, 'slow');
                $("#new_user_form .formsms").html(fdback);
                
                if (response.success) {
                    $("#new_user_form")[0].reset();
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });    
});