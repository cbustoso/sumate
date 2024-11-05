"use strict";

var KTDatatablesServerSide = function () {
    let table;
    let dt;
    let semester;

    var initDatatable = function () {
        dt = $("#kt_generic_datatable").DataTable({
            searchDelay: 500,
            language: {
                "decimal":        "",
                "emptyTable":     "No hay datos disponibles en la tabla",
                "info":           "Mostrando _START_ a _END_ de _TOTAL_ entradas",
                "infoEmpty":      "Mostrando 0 a 0 de 0 entradas",
                "infoFiltered":   "(filtrado de _MAX_ entradas totales)",
                "infoPostFix":    "",
                "thousands":      ".",
                "lengthMenu":     "Mostrar _MENU_ entradas",
                "loadingRecords": "Cargando...",
                "processing":     "",
                "search":         "Buscar:",
                "zeroRecords":    "No se encontraron registros coincidentes",
                "paginate": {
                    "first":      "Primero",
                    "last":       "Último",
                    "next":       "Siguiente",
                    "previous":   "Anterior"
                },
                "aria": {
                    "orderable":  "Ordenar por esta columna",
                    "orderableReverse": "Orden inverso de esta columna"
                }
            },
            search: {
                return: true
            },
            ajax: {
                url: "/api/v1/general/report/users/redemptions/",
                data: function (d) {
                    d.semester = semester;
                },
            },
            dataSrc: 'data',
            columns: [
                { data: 'run' },
                { data: 'email' },
                { data: 'name' },
                { data: 'career' },
                { data: 'prize' },
                { data: 'points' },
                { data: 'created_at' },
                { data: 'updated_at' },
                { data: 'semester' },
                { data: 'status' },
            ],
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.run}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 1,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.email}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 2,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.name}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 3,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.career}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 4,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.prize}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 5,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.points}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 6,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">
                                ${new Date(row.created_at).toLocaleString()}
                            </p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 7,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">
                                ${new Date(row.updated_at).toLocaleString()}
                            </p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 8,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.semester}</p>
                        </td>
                        `;
                    }
                },
                {
                    targets: 9,
                    orderable: false,
                    render: function (data, type, row) {
                        const statusMap = {
                            'hold': 'Reservado',
                            'delivered': 'Entregado',
                            'canceled': 'Cancelado',
                            'expired': 'Expirado'
                        };
                    
                        const statusInSpanish = statusMap[row.status] || row.status;
                    
                        return `
                            <td class="text-end pe-0">
                                <p class="font-size-sm font-weight-bolder">
                                    ${statusInSpanish}
                                </p>
                            </td>
                        `;
                    }
                },
            ],
        });

        table = dt.$;
    }

    var handleSemester = () => {
        const semesterSelect = document.getElementById('kt_semesters');
        semesterSelect.onchange = function() {
            semester = this.value;
            dt.ajax.reload();
        };
    }

    var handleSearchDatatable = function () {
        const filterSearch = document.querySelector('[data-kt-docs-table-filter="search"]');
        filterSearch.addEventListener('keyup', function (e) {
            dt.search(e.target.value).draw();
        });
    }

    var exportButtons = () => {
        const date = new Date();
        const formattedDate = date.toLocaleString('es-ES', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).replace(/[\/:]/g, '-').replace(', ', '_');
        const documentTitle = 'reporte_usuarios_canjes_' + formattedDate;
        
        new $.fn.dataTable.Buttons(dt, {
            buttons: [
                {
                    extend: 'excelHtml5',
                    title: documentTitle
                }
            ]
        }).container().appendTo($('#kt_generic_datatable_buttons'));

        const exportButtons = document.querySelectorAll('#kt_datatable_example_export_menu [data-kt-export]');

        exportButtons.forEach(exportButton => {
            exportButton.addEventListener('click', e => {
                e.preventDefault();

                const exportValue = e.target.getAttribute('data-kt-export');
                const target = document.querySelector('.dt-buttons .buttons-' + exportValue);

                target.click();
            });
        });
    }

    return {
        init: function () {
            table = document.querySelector('#kt_generic_datatable');

            if ( !table ) {
                return;
            }
            
            initDatatable();
            handleSearchDatatable();
            exportButtons();
            handleSemester();
        }
    }
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTDatatablesServerSide.init();
});