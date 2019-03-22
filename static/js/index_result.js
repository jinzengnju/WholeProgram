/**
 * Created by jin on 2019/2/17.
 */
$(document).on('click','.dataItem',function () {
    var id=$(this).attr('id');
    $.ajax({
            type: 'GET',
            cache:'false',
            url: '/analysis_content/',
            data: {'id':id},
            dataType: 'json',
            async: false,
            success: function(data){
                if (data["status"]==1){
                    window.location.href='case_content';
                }
            }
    });

})

