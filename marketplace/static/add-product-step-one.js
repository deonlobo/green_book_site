$(document).ready(function () {
 $("#id_percent").parent().hide()
    $("#id_discounted").change(function(value){
        console.log($(this).val()=="True")
        // $(this).val()
        if($(this).val()=="True"){
            $("#id_percent").parent().show()
        }else{
            $("#id_percent").parent().hide()
        }
    });
});