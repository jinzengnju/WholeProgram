/**
 * Created by jin on 2019/2/17.
 */
$(document).on('click','.asas',function () {
    var id=$(this).data('id');
    console.log(id);
    $.ajax({
            type: 'GET',
            cache:'false',
            url: '/case_content/',
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

