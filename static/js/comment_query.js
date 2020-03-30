$(document).ready(function () {
    $('#next').click(function(){
        $.ajax({
            data: {'page':$('#page').attr('value'), 'to':'1'},
            type: 'GET',
            url: $('#page').attr('action'),
            success:function(response){
                $('#comments').html(response.html);
                $('#page').attr('value',response.page);
            }
        });
    });
    $('#previous').click(function(){
        $.ajax({
            data: {'page':$('#page').attr('value'), 'to':'-1'},
            type: 'GET',
            url: $('#page').attr('action'),
            success:function(response){
                $('#comments').html(response.html);
                $('#page').attr('value', response.page);
            }
        });
    });
});