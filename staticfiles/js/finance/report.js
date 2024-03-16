$(function () {
    $("#finance_menu_btn").click();

    $("#container .revenue_info ul li a").click(function (e) { 
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .revenue_info .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });
});