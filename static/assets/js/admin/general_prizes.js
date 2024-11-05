var KTChartForAttendees = function () {
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
                url: "/api/v1/general/report/participation/prizes/",
                data: function (d) {
                    d.semester = semester;
                },
            },
            dataSrc: 'data',
            columns: [
                { data: 'prize' },
                { data: 'semester' },
                { data: 'total_redemptions' },
            ],
            columnDefs: [
                {
                    targets: 0,
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
                    targets: 1,
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
                    targets: 2,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                        <td class="text-end pe-0">
                            <p class="font-size-sm font-weight-bolder">${row.total_redemptions}</p>
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
        const documentTitle = 'reporte_global_premios' + formattedDate;
        
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

    var initAttendeesChart = async function() {
        var fetchData = async function() {
            try {
                const response = await fetch('/api/v1/general/report/participation/prizes/monthly/');
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error fetching data:', error);
                return null;
            }
        };
        const asd = await fetchData();
        
        var element = document.getElementById('kt_attendees_chart');

        var height = parseInt(KTUtil.css(element, 'height'));
        var labelColor = KTUtil.getCssVariableValue('--bs-gray-600');
        var borderColor = KTUtil.getCssVariableValue('--bs-gray-600');
        var baseColor = KTUtil.getCssVariableValue('--bs-gray-600');
        var lightColor = KTUtil.getCssVariableValue('--bs-gray-600');
        
        if (!element) {
            return;
        }

        var adaptedData = [];
        for (var key in asd.data) {
            if (asd.data.hasOwnProperty(key)) {
                adaptedData.push({
                    name: key,
                    data: asd.data[key]
                });
            }
        }

        var options = {
            series: adaptedData,
            chart: {
                fontFamily: 'inherit',
                type: 'area',
                height: height,
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
        
            },
            legend: {
                show: false
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                type: 'solid',
                opacity: 1
            },
            stroke: {
                curve: 'smooth',
                show: true,
                width: 3,
                colors: [baseColor]
            },
            xaxis: {
                categories: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false
                },
                labels: {
                    style: {
                        colors: labelColor,
                        fontSize: '12px'
                    }
                },
                crosshairs: {
                    position: 'front',
                    stroke: {
                        color: baseColor,
                        width: 1,
                        dashArray: 3
                    }
                },
                tooltip: {
                    enabled: true,
                    formatter: undefined,
                    offsetY: 0,
                    style: {
                        fontSize: '12px'
                    }
                }
            },
            yaxis: {
                labels: {
                    style: {
                        colors: labelColor,
                        fontSize: '12px'
                    }
                }
            },
            states: {
                normal: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                hover: {
                    filter: {
                        type: 'none',
                        value: 0
                    }
                },
                active: {
                    allowMultipleDataPointsSelection: false,
                    filter: {
                        type: 'none',
                        value: 0
                    }
                }
            },
            tooltip: {
                style: {
                    fontSize: '12px'
                },
                y: {
                    formatter: function (val) {
                        return val + ' Canjes'
                    }
                }
            },
            colors: [lightColor],
            grid: {
                borderColor: borderColor,
                strokeDashArray: 4,
                yaxis: {
                    lines: {
                        show: true
                    }
                }
            },
            markers: {
                strokeColor: baseColor,
                strokeWidth: 3
            }
        };
        
        var chart = new ApexCharts(element, options);
        chart.render();
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
            initAttendeesChart();
        }
    }
}();

KTUtil.onDOMContentLoaded(function () {
    KTChartForAttendees.init();
});