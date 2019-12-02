var varTable;
$(document).ready(function () {
    $("#tbl_bice").dataTable().fnDestroy();
    LoadTable(); 
    
});

function LoadTable()
{
    vartable1 = $("#tbl_bice").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/bice_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.bice_id = 0;
            },
            error: function (e) {
                $("#tbl_qp tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Bice_Name" },
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    varButtons += '<a onclick="EditBiceDetail(\'' + row.Bice_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                    return varButtons;
                }
            }
            
        ],


    });
}
function EditBiceDetail(BiceId)
{
    $('#hdn_bice_id').val(BiceId);
    $('#form1').submit();
    
}