$(document).ready(function(){
                    alert("fuck");
                    $(".btn").click(function(e){
                        e.preventDefault;
                        alert("click");
                        $.ajax({
                            url:"/dataFromAjax", 
                            data:{
                                "mydata": "test data"
                            },
                            success:function(data){
                                alert(data[0]+ data[1]);
                            }
                        });
                    });
});