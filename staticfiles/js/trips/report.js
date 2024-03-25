$(function () {
    $("#trips_menu_btn").click();

    var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    function get_dates(dt, type) {
        if (type == 'load') {
            var mindate = $('#min_load_date').val();
            var maxdate = $('#max_load_date').val();
        } else {
            var mindate = $('#min_start_date').val();
            var maxdate = $('#max_start_date').val();
        }
        let dt_start = "";
        let dt_end = "";
        if (mindate) dt_start = mindate + ' 00:00:00.000000';
        if (maxdate) dt_end = maxdate + ' 23:59:59.999999';
        return (dt === 0) ? dt_start : dt_end;
    }

    $("#report_table thead tr").clone(true).attr('class','filters').appendTo('#report_table thead');
    var report_table = $("#report_table").DataTable({
        fixedHeader: true,
        processing: true,
        serverSide: true,
        ajax: {
            url: $("#report_url_input").val(),
            type: "POST",
            data: function (d) {
                d.load_startdate = get_dates(0, 'load');
                d.load_enddate = get_dates(1, 'load');
                d.trip_startdate = get_dates(0, 'start');
                d.trip_enddate = get_dates(1, 'start');
            },
            dataType: 'json',
            headers: { 'X-CSRFToken': CSRF_TOKEN },
        },
        columns: [
            { data: 'count' },
            { data: 'batch' },
            { data: 'type' },
            { data: 'client' },
            { data: 'truck' },
            { data: 'driver' },
            { data: 'currentposition' },
            { data: 'status' },
            { data: 'loaddate' },
            { data: 'startdate' },
            { data: 'daysLoading' },
            { data: 'daysGoing' },
            { data: 'complete' },
            { data: 'goReturn' },
        ],
        order: [[10, 'desc']],
        paging: true,
        lengthMenu: [[10, 20, 30, 50, 100, -1], [10, 20, 30, 50, 100, "All"]],
        pageLength: 10,
        lengthChange: true,
        autoWidth: true,
        searching: true,
        bInfo: true,
        bSort: true,
        orderCellsTop: true,
        autoWidth: true,
        columnDefs: [{
            "targets": 0,
            "orderable": false,
        },
        {
            targets: [1, 2, 3, 5, 6, 7, 8, 9],
            className: 'text-start',
        },
        {
            targets: [3, 5, 6, 7],
            className: 'elipsis',
        }],
        dom: "lBfrtip",
        buttons: [
            { // Copy button
                extend: "copy",
                text: "<i class='fas fa-clone'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Copy",
                title: "Operations report - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                }
            },
            { // PDF button
                extend: "pdf",
                text: "<i class='fas fa-file-pdf'></i>",
                className: "btn btn-bblight text-white",
                titleAttr: "Export to PDF",
                title: "Operations report - Multiplier ltd",
                filename: 'multiplier-ltd-op-report',
                orientation: 'landscape',
                pageSize: 'A4',
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
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
                    // doc.content[1].table.widths = Array(doc.content[1].table.body[1].length + 1).join('*').split('');

                    var body = doc.content[1].table.body;
                    for (i = 1; i < body.length; i++) {
                        doc.content[1].table.body[i][0].margin = [5, 0, 0, 0];
                        doc.content[1].table.body[i][0].alignment = 'center';
                        doc.content[1].table.body[i][1].alignment = 'left';
                        doc.content[1].table.body[i][2].alignment = 'left';
                        doc.content[1].table.body[i][3].alignment = 'left';
                        doc.content[1].table.body[i][4].alignment = 'center';
                        doc.content[1].table.body[i][5].alignment = 'left';
                        doc.content[1].table.body[i][6].alignment = 'left';
                        doc.content[1].table.body[i][7].alignment = 'left';
                        doc.content[1].table.body[i][8].alignment = 'center';
                        doc.content[1].table.body[i][9].alignment = 'center';
                        doc.content[1].table.body[i][10].alignment = 'center';
                        doc.content[1].table.body[i][11].alignment = 'center';
                        doc.content[1].table.body[i][12].alignment = 'center';
                        doc.content[1].table.body[i][13].alignment = 'center';
                        doc.content[1].table.body[i][13].margin = [0, 0, 5, 0];
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
                title: "Operations report - Multiplier ltd",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                }
            },
            { // Print button
                extend: "print",
                text: "<i class='fas fa-print'></i>",
                className: "btn btn-bblight text-white",
                title: "Operations report - Multiplier ltd",
                orientation: 'landscape',
                pageSize: 'A4',
                titleAttr: "Print",
                footer: true,
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
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
            api.columns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]).eq(0).each(function (colIdx) {
                var cell = $(".filters th").eq($(api.column(colIdx).header()).index());
                if (colIdx == 0) {
                    cell.html("");
                } else if (colIdx == 8) {
                    var calendar =`<button type="button" class="btn btn-sm btn-bblight text-white" data-bs-toggle="modal" data-bs-target="#load_date_modal"><i class="fas fa-calendar-alt"></i></button>`;
                    cell.html(calendar);
                    $("#load_date_clear").on("click", function() {
                        $("#min_load_date").val("");
                        $("#max_load_date").val("");
                    });
                    $("#load_date_btn").on("click", function() {
                        report_table.draw();
                    });
                } else if (colIdx == 9) {
                    var calendar =`<button type="button" class="btn btn-sm btn-bblight text-white" data-bs-toggle="modal" data-bs-target="#start_date_modal"><i class="fas fa-calendar-alt"></i></button>`;
                    cell.html(calendar);
                    $("#start_date_clear").on("click", function() {
                        $("#min_start_date").val("");
                        $("#max_start_date").val("");
                    });
                    $("#start_date_btn").on("click", function() {
                        report_table.draw();
                    });
                } else if (colIdx == 2 || colIdx == 12) {
                    var select = document.createElement("select");
                    select.className = "select-filter text-ttxt float-start";
                    if (colIdx == 2) {
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
                    if (colIdx==1 || colIdx==2 || colIdx==3 || colIdx==5 || colIdx==6 || colIdx==7 || colIdx==8 || colIdx==9 || colIdx==12) {
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

    $("#report_search").keyup(function() {
        report_table.search($(this).val()).draw();
    });

    $("#report_filter_clear").click(function (e) { 
        e.preventDefault();
        $("#report_search").val('');
        report_table.search('').draw();
    });
});