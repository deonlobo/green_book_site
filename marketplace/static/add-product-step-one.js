$(document).ready(function () {
    if($("#id_discounted").val()=="True"){
          $("#id_percent").parent().show()
    }else{
          $("#id_percent").parent().hide()
    }
    $("#id_discounted").change(function(value){
        // $(this).val()
        if($(this).val()=="True"){
            $("#id_percent").parent().show()
        }else{
            $("#id_percent").parent().hide()
        }
    });
});