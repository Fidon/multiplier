$(function () {
    $("#trips_menu_btn").click();

    // Tabson truck's page
    $("#container .info_trip ul li a").click(function (e) { 
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .info_trip .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });
});