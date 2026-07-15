import { apiRequest } from './auth.js';

 const GetAllDepartments = "/api/department/getAllDepartments";
 const DeleteDepartment = "/api/department/deleteDepartmentById";

 let datatable;
 
 $(document).ready(async function () {

    datatable = $('#departmentTable').DataTable({

        serverSide:true,
        searching:false,
        ordering:true,
        pageLengh:10,
        order:[[0,'desc']],
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        language: {
            lengthMenu: "_MENU_&nbsp;&nbsp;Entries per page",
            emptyTable: "No user data available",
            processing: "Loading..."
        },
        columnDefs:[
            {targets:3, orderable:false, searchable:false}
        ],
        ajax: async function (data, callback) {

                // const page = (data.start / data.length) + 1;
                // const pageSize = data.length
                // const sortColumn = data.columns[data.order[0].column].data;
                // const sortDirection = data.order[0].dir;

                const search = document.getElementById("searchDepartment").value;
                const isActive = document.getElementById("statusFilter").value;
                

                const response = await apiRequest(`${GetAllDepartments}?search=${search}&isactive=${isActive}`
                                    );

                const result = await response.json();
                
                document.getElementById("totalDepartments").textContent = result.data[0].totalRecords;

                callback({
                    draw: data.draw,
                    recordsTotal: result.data[0].totalRecords,
                    recordsFiltered: result.data[0].totalRecords,
                    data: result.data[0].items
                });
            },

            columns: [

                {
                    data: "DepartmentName",
                    className: "text-center",
                    orderSequence: ['asc', 'desc']
                },

                {
                    data: "ManagerName",
                    className: "text-center",
                    orderSequence: ['asc', 'desc'],
                    
                },

                {
                    data: "isActive",
                    className: "text-center",
                    orderSequence: ['asc', 'desc'],
                    render: function(data) {

                        return data
                            ? '<span class="badge bg-success">Active</span>'
                            : '<span class="badge bg-danger">Inactive</span>';
                    }
                },

                {
                    data: null,
                    className: "text-center",
                    render: function(data, row) {

                        return `
                            <button
                                class="btn btn-sm btn-outline-primary me-1 edit-user"
                                data-id="${data.id}">
                                <i class="bi bi-pencil-square"></i>
                            </button>

                            <button
                                class="btn btn-sm btn-outline-danger delete-user"
                                data-id="${data.id}">
                                <i class="bi bi-trash"></i>
                            </button>
                        `;
                    }
                }

            ]
    });
 })

 document.getElementById("filterBtn").addEventListener("click", function () {

    datatable.ajax.reload();

});