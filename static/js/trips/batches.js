$(function () {
    $("#trips_menu_btn").click();

    // tabs
    $("#container .batch_info ul li a").click(function (e) { 
        e.preventDefault();
        var tab_id = $(this).attr('href').replace('#','');
        $("#container .batch_info .tab_container .tab_div").each(function () {
            if (($(this).is(':visible')) && ($(this).attr('id') !== tab_id)) {
                $(this).css('display','none');
                $('#'+tab_id).fadeIn('slow');
            }
        });
    });

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // register new batch
    $("#addnew_batch_form").submit(function (e) { 
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
                $("#btc_cancel_btn").hide();
                $("#btc_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#btc_cancel_btn").show();
                $("#btc_submit_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#new_batch_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                $("#addnew_batch_form .formsms").html(fdback);
                
                if(response.success) {
                    $("#addnew_batch_form")[0].reset();
                    batches_table.draw();
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    // update batch information
    $("#update_batch_form").submit(function (e) { 
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
                $("#btc_cancel_btn").hide();
                $("#btc_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#btc_cancel_btn").show();
                $("#btc_submit_btn").text("Update").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#update_batch_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                $("#update_batch_form .formsms").html(fdback);

                if(response.success) {
                    $("#batch_basic_info").load(location.href + " #batch_basic_info");
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
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

    $("#batches_table thead tr").clone(true).attr('class','filters').appendTo('#batches_table thead');
    var batches_table = $("#batches_table").DataTable({
        fixedHeader: true,
        processing: true,
        serverSide: true,
        ajax: {
            url: $("#batches_url").val(),
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
            { data: 'regdate' },
            { data: 'batchnumber' },
            { data: 'type' },
            { data: 'client' },
            { data: 'trucks' },
            { data: 'complete' },
            { data: 'action' },
        ],
        order: [[2, 'desc']],
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
            "targets": [0, 7],
            "orderable": false,
        },
        {
            targets: [2, 3, 4],
            className: 'text-start',
        },
        {
            targets: 7,
            createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
                var cell_content =`<a href="${$("#batches_url").val()}${rowData.id}/" class="btn btn-bblight btn-sm text-white">View</a>`;
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
                title: "Batches - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6]
                }
            },
            { // PDF button
                extend: "pdf",
                text: "<i class='fas fa-file-pdf'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Export to PDF",
                title: "Batches - Multiplier ltd",
                filename: 'batches-multiplier-ltd',
                orientation: 'portrait',
                pageSize: 'A4',
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6],
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
                        doc.content[1].table.body[i][1].alignment = 'center';
                        doc.content[1].table.body[i][2].alignment = 'left';
                        doc.content[1].table.body[i][3].alignment = 'center';
                        doc.content[1].table.body[i][4].alignment = 'left';
                        doc.content[1].table.body[i][5].alignment = 'center';
                        doc.content[1].table.body[i][6].alignment = 'center';
                        doc.content[1].table.body[i][6].margin = [0, 0, 3, 0];

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
                title: "Batches - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6]
                }
            },
            { // Print button
                extend: "print",
                text: "<i class='fas fa-print'></i>",
                className: "btn btn-bblight text-white",
                title: "Batches - Multiplier ltd",
                orientation: 'portrait',
                pageSize: 'A4',
                titleAttr: "Print",
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6],
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
            api.columns([0, 1, 2, 3, 4, 5, 6, 7]).eq(0).each(function (colIdx) {
                var cell = $(".filters th").eq($(api.column(colIdx).header()).index());
                if (colIdx == 1) {
                    var calendar =`<button type="button" class="btn btn-sm btn-bblight text-white" data-bs-toggle="modal" data-bs-target="#date_filter_modal"><i class="fas fa-calendar-alt"></i></button>`;
                    cell.html(calendar);
                    $("#date_clear").on("click", function() {
                        $("#min_date").val("");
                        $("#max_date").val("");
                    });
                    $("#date_filter_btn").on("click", function() {
                        batches_table.draw();
                    });
                } else if (colIdx == 0 || colIdx == 7) {
                    cell.html("");
                } else if (colIdx == 3 || colIdx == 6) {
                    var select = document.createElement("select");
                    select.className = "select-filter text-ttxt float-start";
                    if (colIdx == 3) {
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
                    if (colIdx == 2) {
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

    $("#batches_search").keyup(function() {
        batches_table.search($(this).val()).draw();
    });

    $("#batches_filter_clear").click(function (e) { 
        e.preventDefault();
        $("#batches_search").val('');
        batches_table.search('').draw();
    });

    // add new trip to current batch
    $("#new_batchtrip_form").submit(function (e) { 
        e.preventDefault();

        var loadingDate = new Date($('#trp_loadingdate').val());
        var startDate = new Date($('#trp_startdate').val());

        if (startDate >= loadingDate) {
            var formdata = new FormData($(this)[0])
            formdata.append('trucks', [$("#trp_truck").val()]);

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
                    $("#trp_submit_btn").text("Add").attr('type', 'submit');

                    var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                    
                    $('#new_batchtrip_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                    $("#new_batchtrip_form .formsms").html(fdback);
                    
                    if(response.success) {
                        $("#new_batchtrip_form")[0].reset();
                        $("#batch_trips_table").load(location.href + " #batch_trips_table");
                    }
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            });
        } else {
            var fdback = `<div class="alert alert-danger alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-exclamation-circle'></i> Trip start datetime can't be less that loading date. <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
            $("#new_batchtrip_form .formsms").html(fdback);
        }
    });
});