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

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // register new batch
    $("#trp_newbatch_form").submit(function (e) { 
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: new FormData($(this)[0]),
            dataType: 'json',
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            beforeSend: function() {
                $("#trp_btc_cancel_btn").hide();
                $("#trp_newbatch_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#trp_btc_cancel_btn").show();
                $("#trp_newbatch_submit_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#trp_addnewbatch_modal .modal-body').animate({ scrollTop: 0 }, 'slow');
                $("#trp_newbatch_form .formsms").html(fdback);
                
                if(response.success) {
                    $("#trp_newbatch_form")[0].reset();
                    var new_batch = $("<option></option>").attr("value", parseInt(response.id)).text(response.batch+' - '+response.type+': '+response.client);
                    $("#trp_batch").append(new_batch);
                    $("#trp_batch").val(parseInt(response.id));
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    // add multiple trucks
    var last_index = 1;
    $("#trp_addtruck_btn").click(function (e) { 
        var selectedOptionValue = $("#trp_truck"+last_index).find(":selected").val();
        var remainingOptions = $("#trp_truck"+last_index+" option").length - 1;
    
        if (remainingOptions > 1) {
            var clonedDiv = $("#trp_truck_div"+last_index).clone();
            last_index += 1;
            clonedDiv.attr("id", "trp_truck_div"+last_index);
            clonedDiv.find("select").removeAttr("required");
            clonedDiv.find("select").attr("id", "trp_truck"+last_index);
            
            if (selectedOptionValue !== "") {
                clonedDiv.find("select option[value='" + selectedOptionValue + "']").remove();
            }
            
            clonedDiv.find("label").attr("for", "trp_truck"+last_index);
            clonedDiv.insertAfter("#trp_truck_div"+(last_index-1));
        } else {
            var fdback = `<div class="alert alert-danger alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-exclamation-circle'></i> No more available trucks to add. <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
            $("#new_trip_form .formsms").html(fdback);
        }
    });

    // register new trip
    $("#new_trip_form").submit(function (e) { 
        e.preventDefault();

        var loadingDate = new Date($('#trp_loadingdate').val());
        var startDate = new Date($('#trp_startdate').val());

        if (startDate >= loadingDate) {
            var trucks_added = [];
            $(this).find("select[id^='trp_truck']").each(function() {
                if ($(this).val() !== "") {
                    trucks_added.push($(this).val());
                }
            });

            var formdata = new FormData($(this)[0])
            formdata.append('trucks', trucks_added);

            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: formdata,
                dataType: 'json',
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': CSRF_TOKEN
                },
                beforeSend: function() {
                    $("#trp_cancel_btn").hide();
                    $("#trp_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
                },
                success: function(response) {
                    $("#trp_cancel_btn").show();
                    $("#trp_submit_btn").text("Save").attr('type', 'submit');

                    var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                    
                    $('#new_trip_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                    $("#new_trip_form .formsms").html(fdback);
                    
                    if(response.success) {
                        $("#new_trip_form")[0].reset();
                        for(var i=last_index; i>1; i--) {
                            $("#trp_truck_div"+i).remove();
                        }
                        trips_table.draw();
                    }
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            });
        } else {
            var fdback = `<div class="alert alert-danger alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-exclamation-circle'></i> Trip start datetime can't be less that loading date. <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
            $("#new_trip_form .formsms").html(fdback);
        }
    });
    
    function get_dates(dt) {
        const mindate = $('#min_date').val();
        const maxdate = $('#max_date').val();
        let dt_start = "";
        let dt_end = "";
        if (mindate) dt_start = mindate + ' 00:00:00.000000';
        if (maxdate) dt_end = maxdate + ' 23:59:59.999999';
        return (dt === 0) ? dt_start : dt_end;
    }

    $("#trips_table thead tr").clone(true).attr('class','filters').appendTo('#trips_table thead');
    var trips_table = $("#trips_table").DataTable({
        fixedHeader: true,
        processing: true,
        serverSide: true,
        ajax: {
            url: $("#trips_url_input").val(),
            type: "POST",
            data: function (d) {
                d.startdate = get_dates(0);
                d.enddate = get_dates(1);
            },
            dataType: 'json',
            headers: { 'X-CSRFToken': CSRF_TOKEN },
        },
        columns: [
            { data: 'count' },
            { data: 'batch' },
            { data: 'truck' },
            { data: 'driver' },
            { data: 'startdate' },
            { data: 'status' },
            { data: 'currentposition' },
            { data: 'type' },
            { data: 'days' },
            { data: 'complete' },
            { data: 'action' },
        ],
        order: [[4, 'desc']],
        paging: true,
        lengthMenu: [[10, 20, 30, 50, 100, -1], [10, 20, 30, 50, 100, "All"]],
        pageLength: 10,
        lengthChange: true,
        autoWidth: true,
        searching: true,
        bInfo: true,
        bSort: true,
        orderCellsTop: true,
        columnDefs: [{
            "targets": [0, 10],
            "orderable": false,
        },
        {
            targets: [1, 2, 3, 5, 6, 7],
            className: 'text-start ps-1',
        },
        {
            targets: [3, 5, 6],
            className: 'elipsis',
        },
        {
            targets: 1,
            createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
                var cell_content =`<a href="${$("#batches_url_input").val()}${rowData.batch_id}/">${rowData.batch}</a>`;
                $(cell).html(cell_content);
            }
        },
        {
            targets: 2,
            createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
                var cell_content =`<a href="${$("#trucks_url_input").val()}${rowData.truck_id}/">${rowData.truck}</a>`;
                $(cell).html(cell_content);
            }
        },
        {
            targets: 3,
            createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
                var cell_content =`<a href="${$("#drivers_url_input").val()}${rowData.driver_id}/">${rowData.driver}</a>`;
                $(cell).html(cell_content);
            }
        },
        {
            targets: 10,
            createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
                var cell_content =`<a href="${$("#trips_url_input").val()}${rowData.id}/" class="btn btn-bblight btn-sm text-white">View</a>`;
                $(cell).html(cell_content);
            }
        }],
        dom: "lBfrtip",
        buttons: [
            { // Copy button
                extend: "copy",
                text: "<i class='fas fa-clone'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Copy",
                title: "Trips - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                }
            },
            { // PDF button
                extend: "pdf",
                text: "<i class='fas fa-file-pdf'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Export to PDF",
                title: "Trips - Multiplier ltd",
                filename: 'trips-multiplier-ltd',
                orientation: 'landscape',
                pageSize: 'A4',
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    search: 'applied',
                    order: 'applied'
                },
                tableHeader: {
                    alignment: "center"
                },
                customize: function(doc) {
                    doc.styles.tableHeader.alignment = "center";
                    doc.styles.tableBodyOdd.alignment = "center";
                    doc.styles.tableBodyEven.alignment = "center";
                    doc.styles.tableHeader.fontSize = 7;
                    doc.defaultStyle.fontSize = 6;
                    doc.content[1].table.widths = Array(doc.content[1].table.body[1].length + 1).join('*').split('');

                    var body = doc.content[1].table.body;
                    for (i = 1; i < body.length; i++) {
                        doc.content[1].table.body[i][0].margin = [3, 0, 0, 0];
                        doc.content[1].table.body[i][0].alignment = 'center';
                        doc.content[1].table.body[i][1].alignment = 'left';
                        doc.content[1].table.body[i][2].alignment = 'left';
                        doc.content[1].table.body[i][3].alignment = 'left';
                        doc.content[1].table.body[i][4].alignment = 'center';
                        doc.content[1].table.body[i][5].alignment = 'left';
                        doc.content[1].table.body[i][6].alignment = 'left';
                        doc.content[1].table.body[i][7].alignment = 'center';
                        doc.content[1].table.body[i][8].alignment = 'center';
                        doc.content[1].table.body[i][9].alignment = 'center';
                        doc.content[1].table.body[i][9].margin = [0, 0, 3, 0];

                        for (let j = 0; j < body[i].length; j++) {
                            body[i][j].style = "vertical-align: middle;";
                        }
                    }
                }
            },
            { // Export to excel button
                extend: "excel",
                text: "<i class='fas fa-file-excel'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Export to Excel",
                title: "Trips - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                }
            },
            { // Print button
                extend: "print",
                text: "<i class='fas fa-print'></i>",
                className: "btn btn-bblight text-white",
                title: "Trips - Multiplier ltd",
                orientation: 'landscape',
                pageSize: 'A4',
                titleAttr: "Print",
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    search: 'applied',
                    order: 'applied'
                },
                tableHeader: {
                    alignment: "center"
                },
                customize: function (win) {
                    $(win.document.body).css("font-size","11pt");
                    $(win.document.body).find("table").addClass("compact").css("font-size","inherit");
                }
            }
        ],
        initComplete: function() {
            var api = this.api();
            api.columns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).eq(0).each(function (colIdx) {
                var cell = $(".filters th").eq($(api.column(colIdx).header()).index());
                if (colIdx == 0 || colIdx == 10) {
                    cell.html("");
                } else if (colIdx == 4) {
                    var calendar =`<button type="button" class="btn btn-sm btn-bblight text-white" data-bs-toggle="modal" data-bs-target="#date_filter_modal"><i class="fas fa-calendar-alt"></i></button>`;
                    cell.html(calendar);
                    $("#date_clear").on("click", function() {
                        $("#min_date").val("");
                        $("#max_date").val("");
                    });
                    $("#date_filter_btn").on("click", function() {
                        trips_table.draw();
                    });
                } else if (colIdx == 7 || colIdx == 9) {
                    var select = document.createElement("select");
                    select.className = "select-filter text-ttxt float-start";
                    if (colIdx == 7) {
                        select.innerHTML = `<option value="">All</option>` +
                        `<option value="Going">Going</option>` +
                        `<option value="Return">Return</option>`;
                    } else {
                        select.innerHTML = `<option value="">All</option>` +
                        `<option value="Yes">Yes</option>` +
                        `<option value="No">No</option>`;
                    }
                    cell.html(select);
                    
                    // Add change event listener to the select
                    $(select).on("change", function() {
                        api.column(colIdx).search($(this).val()).draw();
                    });
                } else {
                    if (colIdx==1 || colIdx==2 || colIdx==3 || colIdx==5 || colIdx==6 || colIdx==7) {
                        $(cell).html("<input type='text' class='text-ttxt float-start w-auto' placeholder='Filter..'/>");
                    } else {
                        $(cell).html("<input type='text' class='text-ttxt' placeholder='Filter..'/>");
                    }
                    $("input", $(".filters th").eq($(api.column(colIdx).header()).index()))
                    .off("keyup change").on("keyup change", function(e) {
                        e.stopPropagation();
                        $(this).attr('title', $(this).val());
                        var regexr = "{search}";
                        var cursorPosition = this.selectionStart;
                        api.column(colIdx).search(
                            this.value != '' ? regexr.replace('{search}', this.value) : '',
                            this.value != '',
                            this.value == ''
                            ).draw();
                        $(this).focus()[0].setSelectionRange(cursorPosition, cursorPosition);
                    });
                }
            });
        }
    });

    $("#trips_search").keyup(function() {
        trips_table.search($(this).val()).draw();
    });

    $("#trips_filter_clear").click(function (e) { 
        e.preventDefault();
        $("#trips_search").val('');
        trips_table.search('').draw();
    });

    // register new trip update/history
    $("#trip_addhistory_form").submit(function (e) { 
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: new FormData($(this)[0]),
            dataType: 'json',
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            beforeSend: function() {
                $("#cancel_hist_btn").hide();
                $("#submit_hist_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#cancel_hist_btn").show();
                $("#submit_hist_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#trip_addhistory_modal .modal-body').animate({ scrollTop: 0 }, 'slow');
                $("#trip_addhistory_form .formsms").html(fdback);
                
                if(response.success) {
                    $("#trip_history_table").load(location.href + " #trip_history_table");
                    $("#trp_hist_status").val('');
                    $("#trp_hist_position").val('');
                    $("#hist_summary .spn1").html(`<b>Last status:</b> &nbsp; ${response.status}`);
                    $("#hist_summary .spn2").html(`<b>Last position:</b> &nbsp; ${response.pos}`);
                    $("#hist_summary .spn3").html(`<b>Last date:</b> &nbsp; ${response.st_date}`);
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    // mark trip as complete
    $("#comp_submit_btn").click(function (e) { 
        var formdata = new FormData();
        var today_date = new Date().toISOString().split('T')[0];
        formdata.append("complete_id", $("#trip_id_input").val());
        formdata.append("today_date", today_date);

        $.ajax({
            type: 'POST',
            url: $("#update_trip_form").attr('action'),
            data: formdata,
            dataType: 'json',
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            beforeSend: function() {
                $("#comp_cancel_btn").hide();
                $("#comp_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>");
            },
            success: function(response) {
                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $("#mark_complete_modal .formsms").html(fdback);
                
                if(response.success) {
                    $("#tab_container_div").load(location.href + " #tab_container_div");
                    $("#comp_submit_btn").html(`<i class="fas fa-check-circle"></i> Close`).attr("data-bs-dismiss", "modal");
                } else {
                    $("#comp_cancel_btn").show();
                    $("#comp_submit_btn").html(`<i class="fas fa-check-circle"></i> Continue`);
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    // Update trip info
    $("#update_trip_form").submit(function (e) { 
        e.preventDefault();
        var loadingDate = new Date($('#trp_loadingdate').val());
        var startDate = new Date($('#trp_startdate').val());

        if (loadingDate >= startDate) {
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: new FormData($(this)[0]),
                dataType: 'json',
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': CSRF_TOKEN
                },
                beforeSend: function() {
                    $("#trp_cancel_btn").hide();
                    $("#trp_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
                },
                success: function(response) {
                    $("#trp_cancel_btn").show();
                    $("#trp_submit_btn").text("Update").attr('type', 'submit');

                    var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                    
                    $('#trip_updateinfo_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                    $("#update_trip_form .formsms").html(fdback);
                    
                    if(response.success) {
                        $("#trip_basic_info").load(location.href + " #trip_basic_info");
                    }
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            });
        } else {
            var fdback = `<div class="alert alert-danger alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-exclamation-circle'></i> Trip start datetime can't be less that loading date. <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
            $("#update_trip_form .formsms").html(fdback);
            $('#trip_updateinfo_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
        }
    });
});