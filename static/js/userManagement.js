 import { apiRequest } from './auth.js';
 import { loadRoles } from './validation.js';

 const GetAllUser = "/api/user/getAllUser";
 const DeleteUser = "/api/user/deleteUser";

 let userTable

 $(document).ready(async function () {
    await loadRoles()

    userTable = $('#userTable').DataTable({
   
      
        serverSide: true,
        searching: false,  
        ordering: true,
        pageLength: 10,
        order:[[0,'desc']],
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        language: {
            lengthMenu: "_MENU_&nbsp;&nbsp;Entries per page",
            emptyTable: "No user data available",
            processing: "Loading..."
        },
         columnDefs: [
            { targets: 4, orderable: false }
        ],
        
        ajax: async function (data, callback) {

            const page = (data.start / data.length) + 1;
            const pageSize = data.length
            const sortColumn = data.columns[data.order[0].column].data;
            const sortDirection = data.order[0].dir;

            const search = document.getElementById("searchUser").value;
            const roleId = document.getElementById("role").value ;
            const isActive = document.getElementById("statusFilter").value;
            

            const response = await apiRequest(`${GetAllUser}?page=${page}&pagesize=${pageSize}&search=${search}&roleid=${roleId}&isactive=${isActive}&sortcolumn=${sortColumn}&sortdirection=${sortDirection}`
                                );

            const result = await response.json();
            
            document.getElementById("totalUsers").textContent = result.data.totalRecords;

            callback({
                draw: data.draw,
                recordsTotal: result.data.totalRecords,
                recordsFiltered: result.data.totalRecords,
                data: result.data.items
            });
        },

        columns: [

            {
                data: "name",
                className: "text-center",
                orderSequence: ['asc', 'desc']
            },

            {
                data: "email",
                className: "text-center",
                orderSequence: ['asc', 'desc']
            },

            {
                data: "roleId",
                className: "text-center",
                orderSequence: ['asc', 'desc'],
                render: function(data) {

                    switch(data) {
                        case 1:
                            return '<span class="badge bg-primary">Admin</span>';

                        case 2:
                            return '<span class="badge bg-success">Manager</span>';

                        case 3:
                            return '<span class="badge bg-secondary">Employee</span>';

                        default:
                            return '-';
                    }
                }
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
                orderable: false,
                searchable: false,
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

    userTable.ajax.reload();

});
 $(document).on("click", ".edit-user", function () {

    const userId = $(this).data("id");

    window.location.href = `/Admin/editUser/${userId}`;

});


$(document).on("click", ".delete-user", async function () {

    const id = $(this).data("id");

    if (!confirm("Are you sure you want to delete this user?")) {
        return;
    }

    try{
        const response = await apiRequest(`${DeleteUser}/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (result.success) {

            userTable.ajax.reload();

        } else {

            alert(result.message);

        }
    }
    catch (error){
        console.error(error);
        alert("Something went wrong.");

    }
    

});

 document.getElementById("addbtn").addEventListener("click", function () {
    window.location.href = "/Admin/addUser";
});
