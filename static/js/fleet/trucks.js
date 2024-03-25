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

    // register new truck
    $("#addnew_truck_form").submit(function (e) { 
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
                $("#trk_cancel_btn").hide();
                $("#trk_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#trk_cancel_btn").show();
                $("#trk_submit_btn").text("Save").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#new_truck_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                $("#addnew_truck_form .formsms").html(fdback);

                if(response.success) {
                    $("#addnew_truck_form")[0].reset();
                    trucks_table.draw();
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    var trk_horsetype_val = $("#update_truck_horse").val();
    $("#trk_horse option[value='"+trk_horsetype_val+"']").prop("selected", true);
    
    
    // update truck details
    $("#update_truck_form").submit(function (e) { 
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
                $("#trk_cancel_btn").hide();
                $("#trk_submit_btn").html("<i class='fas fa-spinner fa-pulse'></i>").attr('type', 'button');
            },
            success: function(response) {
                $("#trk_cancel_btn").show();
                $("#trk_submit_btn").text("Update").attr('type', 'submit');

                var fdback = `<div class="alert alert-${response.success ? 'success' : 'danger'} alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-${response.success ? 'check' : 'exclamation'}-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;
                
                $('#update_truck_canvas .offcanvas-body').animate({ scrollTop: 0 }, 'slow');
                $("#update_truck_form .formsms").html(fdback);

                if(response.success) {
                    $("#truck_basic_info").load(location.href + " #truck_basic_info");
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    // delete driver
    $("#confirm_delete_btn").click(function (e) { 
        e.preventDefault();

        var formData = new FormData();
        formData.append("truck_id", $("#truck_update_id").val());
        formData.append("delete_truck", "delete");

        $.ajax({
            type: 'POST',
            url: $("#update_truck_form").attr('action'),
            data: formData,
            dataType: 'json',
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            beforeSend: function() {
                $("#cancel_delete_btn").hide();
                $("#confirm_delete_btn").html("<i class='fas fa-spinner fa-pulse'></i>");
            },
            success: function(response) {
                if(response.success) {
                    var url = location.href;
                    url = url.replace(/\d+\/?$/, '');
                    location.href = url
                } else {
                    $("#cancel_delete_btn").show();
                    $("#confirm_delete_btn").html("<i class='fas fa-check-circle'></i> Yes");

                    var fdback = `<div class="alert alert-danger alert-dismissible fade show px-2 m-0 d-block w-100"><i class='fas fa-exclamation-circle'></i> ${response.sms} <button type="button" class="btn-close d-inline-block" data-bs-dismiss="alert"></button></div>`;

                    $("#confirm_delete_modal .formsms").html(fdback);
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

    $("#trucks_table thead tr").clone(true).attr('class','filters').appendTo('#trucks_table thead');
    var trucks_table = $("#trucks_table").DataTable({
        fixedHeader: true,
        processing: true,
        serverSide: true,
        ajax: {
            url: $("#truck_url").val(),
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
            { data: 'regnumber' },
            { data: 'type' },
            { data: 'horse' },
            { data: 'model' },
            { data: 'trailer' },
            { data: 'driver' },
            { data: 'status' },
            { data: 'action' },
        ],
        order: [[1, 'asc']],
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
            "targets": [0, 9],
            "orderable": false,
        },
        {
            targets: [3, 4, 5, 7, 8],
            className: 'text-start',
        },
        {
            targets: 8,
            visible: false
        },
        {
            targets: 9,
            className: 'align-middle text-nowrap text-center',
            createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
                var cell_content =`<a href="${$("#truck_url").val()}${rowData.id}/" class="btn btn-bblight btn-sm text-white">View</a>`;
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
                title: "Trucks - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7]
                }
            },
            { // PDF button
                extend: "pdf",
                text: "<i class='fas fa-file-pdf'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Export to PDF",
                title: "Trucks - Multiplier ltd",
                filename: 'trucks-multiplier-ltd',
                orientation: 'portrait',
                pageSize: 'A4',
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7],
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
                        doc.content[1].table.body[i][2].alignment = 'center';
                        doc.content[1].table.body[i][3].alignment = 'left';
                        doc.content[1].table.body[i][4].alignment = 'left';
                        doc.content[1].table.body[i][5].alignment = 'left';
                        doc.content[1].table.body[i][6].alignment = 'center';
                        doc.content[1].table.body[i][7].alignment = 'left';
                        doc.content[1].table.body[i][7].margin = [0, 0, 3, 0];

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
                title: "Trucks - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7]
                }
            },
            { // Print button
                extend: "print",
                text: "<i class='fas fa-print'></i>",
                className: "btn btn-bblight text-white",
                title: "Trucks - Multiplier ltd",
                orientation: 'portrait',
                pageSize: 'A4',
                titleAttr: "Print",
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7],
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
            api.columns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).eq(0).each(function (colIdx) {
                var cell = $(".filters th").eq($(api.column(colIdx).header()).index());
                if (colIdx == 1) {
                    var calendar =`<button type="button" class="btn btn-sm btn-bblight text-white" data-bs-toggle="modal" data-bs-target="#date_filter_modal"><i class="fas fa-calendar-alt"></i></button>`;
                    cell.html(calendar);
                    $("#date_clear").on("click", function() {
                        $("#min_date").val("");
                        $("#max_date").val("");
                    });
                    $("#date_filter_btn").on("click", function() {
                        trucks_table.draw();
                    });
                } else if (colIdx == 0 || colIdx == 9) {
                    cell.html("");
                } else if (colIdx == 4) {
                    var select = document.createElement("select");
                    select.className = "select-filter text-ttxt float-start";
                    select.innerHTML = `<option value="">All</option>` +
                    `<option value="Terias">Terias</option>` +
                    `<option value="Double diff">Double diff</option></select>`;
                    cell.html(select);
                    
                    // Add change event listener to the select
                    $(select).on("change", function() {
                        api.column(colIdx).search($(this).val()).draw();
                    });
                } else {
                    if (colIdx == 3 || colIdx == 4 || colIdx == 5 || colIdx == 7 || colIdx == 8) {
                        $(cell).html("<input type='text' class='text-ttxt float-start' placeholder='Filter..'/>");
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

    $("#trucks_search").keyup(function() {
        trucks_table.search($(this).val()).draw();
    });

    $("#trucks_filter_clear").click(function (e) {
        e.preventDefault();
        $("#trucks_search").val('');
        trucks_table.search('').draw();
    });
});