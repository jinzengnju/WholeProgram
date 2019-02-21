/**
 * Created by jin on 2019/2/17.
 */
$(document).ready(function(){
      $("#searchBtn1").click(function(){
        var fact = $("#searchInput").val();
        $.ajax({
            type: 'GET',
            cache:'false',
            url: '/resultcalculate/',
            data: {'fact':fact},
            dataType: 'json',
            async: false,
            success: function(data){
                if (data["status"]==1){
                    window.location.href='result_law';
                }
            }
        });
      });

      $("#complexSearch").click(function(){
        var fact = $("#searchInput").val();
        var accu=$("#ay").val();
        $.ajax({
            type: 'GET',
            cache:'false',
            url: '/resultFactCalculate/',
            data: {'fact':fact,'accu':accu},
            dataType: 'json',
            async: false,
            success: function(data){
                if (data["status"]==1){
                    window.location.href='result_fact';
                }
            }
        });
      });

    });