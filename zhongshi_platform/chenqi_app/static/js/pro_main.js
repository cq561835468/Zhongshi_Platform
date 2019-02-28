
    //搜索默认第一页
    $("#search_go_all").click(function(){
        $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
        });
        $.ajax({
                    url: '/project_main/',
                    type: 'POST',
                    data: {
                           select: $('#select_all').val(),
                           pro_state: $("#select_state").val(),
                           pro_name:$("#search_input").val(),
                           begin_time_manager:$("#begin_time_manager").val(),
                           end_time_manager:$("#end_time_manager").val(),
                           begin_time_ver:$("#begin_time_ver").val(),
                           end_time_ver:$("#end_time_ver").val(),
                           page_go:1,
                           },
                           success: function (result){
                                var datas = $.parseJSON(result); //列表
                                var str = "";
                                $.each(datas.data, function(ii,iitem){
                                    str += "<tr>";
                                    str += "<td>"+iitem[0]+"</td>"
                                    if(iitem[1] == '已结项'){
                                    str += "<td id=\"bug_table_green\">"+iitem[1]+"</td>"}
                                    else if(iitem[1] == '进行中'){
                                    str += "<td id=\"bug_table_yellow\">"+iitem[1]+"</td>"}
                                    else if(iitem[1] == '暂停中'){
                                    str += "<td id=\"bug_table_red\">"+iitem[1]+"</td>"}
                                    else{
                                    str += "<td id=\"bug_table_blue\">"+iitem[1]+"</td>"}
                                    str += "<td>"+iitem[2]+"</td>"
                                    str += "<td>"+iitem[3]+"</td>"
                                    str += "<td>"+iitem[4]+"</td>"
                                    str += "<td>"+iitem[5]+"</td>"
                                    str += "<td>"+iitem[6]+"</td>"
                                    str += "<td>"+iitem[7]+"</td>"
                                    str += "<td>"+iitem[8]+"</td>"
                                    str += "<td>"+iitem[9]+"</td>"
                                    str += "<td>"+iitem[10]+"</td>"
                                    str += "<td>"+iitem[11]+"</td>"
                                    str += "<td>"+iitem[12]+"</td>"
                                    str += "<td>"+iitem[13]+"</td>"
                                    str +="</tr>"
                                });
                                var page_s = "";
                                page_s += "<li><a href=\"#\" class=\"page_go\">&laquo;</a></li>"
                                $.each(datas.page_list, function(ii,iitem){
                                    if(iitem == 1){
                                        page_s += "<li><a href=\"#\" class=\"page_go_cur\">"+iitem+"</a></li>"
                                    }
                                    else{
                                        page_s += "<li><a href=\"#\" class=\"page_go\">"+iitem+"</a></li>"
                                    }
                                });
                                page_s += "<li><a href=\"#\" class=\"page_go\">&raquo;</a></li>"
                                $('#body').empty()
                                $('#tableSort').append(str)
                                $('#pagination').empty()
                                $('#pagination').append(page_s)
                                $('#search_num_get').text(datas.search_name);
                }


