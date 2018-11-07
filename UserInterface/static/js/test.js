$(document).ready(function(){
    //alert("fuck");
    /*
    $(".btn").click(function(e){
        e.preventDefault();
        $(".div2").css("left","500px");     
        
    });
    */
    var x;
    var y;
/*
    if (!('webkitSpeechRecognition' in window)) {
        alert('doesn\'t exist');
    // do something...
    } else {
    // do something...
        alert('exist');
    }   
    */

    

    var ajax_func = function(){
      $.ajax({
                url: '/dataFromAjax',
                type: 'GET',
                data: {
                    'mode':1,
                },
                error: function(xhr) {
                    //alert('Ajax request 發生錯誤');
                },
                success: function(response) {
                    y = response.y;
                    x = response.x;
                    $(".div2").css("top",y+"vh");
                    $(".div2").css("left",x+"vw");
                    //alert('inner y ');
                    //alert(y)

                }
          
        });
        // if( typeof callback === 'function' ){
      //      callback();
      //  }
        
        
    };
    var show_path = function(){
            //alert('o y ');
            //alert(y)
            var canvas = document.getElementById('canvas');

            if (canvas.getContext){
                var ctx = canvas.getContext('2d');
                width =  document.documentElement.clientWidth*0.85
                height = document.documentElement.clientHeight

                ctx.canvas.width  = width;
                ctx.canvas.height = height;
                ctx.fillStyle="#ff0000";
                ctx.fillRect(width*6/100,height*19/100,0.03*width,0.08*height);
                ctx.fillRect(width*6/100,height*27/100,0.75*width,0.05*height);
                ctx.fillRect(width*6/100,height*32/100,0.03*width,0.37*height);
                ctx.fillRect(width*6/100,height*69/100,0.75*width,0.05*height);
                ctx.fillRect(width*81/100,height*27/100,0.03*width,0.47*height);
                ctx.fillRect(width*6/100,height*74/100,0.03*width,0.25*height);
                ctx.fillRect(width*40/100,height*32/100,0.03*width,0.07*height);
                ctx.fillRect(width*37/100,height*74/100,0.03*width,0.07*height);
                ctx.fillRect(width*84/100,height*47/100,0.03*width,0.05*height);
                //ctx.clearRect(0, 0, width, height);

            }
        
    };
    var show_path1 = function(){
        
            var canvas = document.getElementById('canvas');

            if (canvas.getContext){
                var ctx = canvas.getContext('2d');
                width =  document.documentElement.clientWidth*0.85
                height = document.documentElement.clientHeight

                ctx.canvas.width  = width;
                ctx.canvas.height = height;
                ctx.fillStyle="#ff0000";
                
                if(x > 0 && y > 0){
                    ctx.fillRect(width*6/100,height*19/100,0.03*width,0.08*height);
                    if(x>70){
                        ctx.fillRect(width*6/100,height*27/100,0.75*width,0.05*height);
                        ctx.fillRect(width*81/100,height*27/100,0.03*width,(y-27)/100*height);
                    }
                    else if(y<40){
                        ctx.fillRect(width*6/100,height*27/100,(x-6)/100*width,0.05*height);
                        
                    }else if(y>55){
                        ctx.fillRect(width*6/100,height*27/100,0.03*width,0.42*height);
                        ctx.fillRect(width*6/100,height*69/100,(x-6)/100*width,0.05*height);
                    }else if(x<10){
                        ctx.fillRect(width*6/100,height*27/100,0.03*width,(y-27)/100*height);  
                    }
                    
                    
                }

                //ctx.clearRect(0, 0, width, height);

            }
        
    };
    var show_path2 = function(){
        
            var canvas = document.getElementById('canvas');

            if (canvas.getContext){
                var ctx = canvas.getContext('2d');
                width =  document.documentElement.clientWidth*0.85
                height = document.documentElement.clientHeight

                ctx.canvas.width  = width;
                ctx.canvas.height = height;
                ctx.fillStyle="#ff0000";
                
                if(x > 0 && y > 0){
                    ctx.fillRect(width*40/100,height*32/100,0.03*width,0.07*height);
                    if(x>=40 && y<40){
                        ctx.fillRect(width*40/100,height*27/100,(x-40)/100*width,0.05*height);
                    }else if(x<40 && y<40){
                        ctx.fillRect(width*x/100,height*27/100,(43-x)/100*width,0.05*height);
                    }   
                    else if(y>55){
                        ctx.fillRect(width*6/100,height*27/100,0.37*width,0.05*height);
                        ctx.fillRect(width*6/100,height*32/100,0.05*width,0.37*height);
                        ctx.fillRect(width*6/100,height*69/100,(x-6)/100*width,0.05*height);
                    }else if(x>70){
                        ctx.fillRect(width*40/100,height*27/100,0.44*width,0.05*height);
                        ctx.fillRect(width*81/100,height*27/100,0.03*width,(y-27)/100*height);
                    }else if(x<10){
                        ctx.fillRect(width*6/100,height*27/100,0.37*width,0.05*height);
                        ctx.fillRect(width*6/100,height*32/100,0.03*width,(y-32)/100*height);
                    }
                    
                    
                }

                //ctx.clearRect(0, 0, width, height);

            }
        
    };
    var show_path3 = function(){
        
            var canvas = document.getElementById('canvas');

            if (canvas.getContext){
                var ctx = canvas.getContext('2d');
                width =  document.documentElement.clientWidth*0.85
                height = document.documentElement.clientHeight

                ctx.canvas.width  = width;
                ctx.canvas.height = height;
                ctx.fillStyle="#ff0000";
                
                if(x > 0 && y > 0){
                    ctx.fillRect(width*37/100,height*74/100,0.03*width,0.07*height);
                    if(x>=37 && y>55){
                        ctx.fillRect(width*37/100,height*69/100,(x-37)/100*width,0.05*height);
                    }else if(x<37 && y>55){
                        ctx.fillRect(width*x/100,height*69/100,(40-x)/100*width,0.05*height);
                    }   
                    else if(y<40){
                        ctx.fillRect(width*6/100,height*69/100,0.34*width,0.05*height);
                        ctx.fillRect(width*6/100,height*32/100,0.05*width,0.37*height);
                        ctx.fillRect(width*6/100,height*27/100,(x-6)/100*width,0.05*height);
                    }else if(x>70){
                        ctx.fillRect(width*37/100,height*69/100,0.44*width,0.05*height);
                        ctx.fillRect(width*81/100,height*y/100,0.03*width,(74-y)/100*height);
                    }else if(x<10){
                        ctx.fillRect(width*6/100,height*69/100,0.34*width,0.05*height);
                        ctx.fillRect(width*6/100,height*y/100,0.03*width,(74-y)/100*height);
                    }
                    
                    
                }

                //ctx.clearRect(0, 0, width, height);

            }
        
    };
    var show_path4 = function(){
        
            var canvas = document.getElementById('canvas');

            if (canvas.getContext){
                var ctx = canvas.getContext('2d');
                width =  document.documentElement.clientWidth*0.85
                height = document.documentElement.clientHeight

                ctx.canvas.width  = width;
                ctx.canvas.height = height;
                ctx.fillStyle="#ff0000";
                
                if(x > 0 && y > 0){
                    ctx.fillRect(width*84/100,height*47/100,0.04*width,0.04*height);
                    if(x>70 && y<47){
                        ctx.fillRect(width*81/100,height*y/100,0.03*width,(51-y)/100*height);
                    }else if(x>70 && y>=47){
                        ctx.fillRect(width*81/100,height*47/100,0.03*width,(y-47)/100*height);
                    }   
                    else if(y<40){
                        ctx.fillRect(width*81/100,height*27/100,0.03*width,0.24*height);
                        ctx.fillRect(width*x/100,height*27/100,(81-x)/100*width,0.05*height);
                    }else if(y>55){
                        ctx.fillRect(width*81/100,height*47/100,0.03*width,0.27*height);
                        ctx.fillRect(width*x/100,height*69/100,(81-x)/100*width,0.05*height);
                    }else if(x<10){
                        ctx.fillRect(width*81/100,height*27/100,0.03*width,0.24*height);
                        ctx.fillRect(width*6/100,height*27/100,0.75*width,0.05*height);
                        ctx.fillRect(width*6/100,height*27/100,0.03*width,(y-27)/100*height);
                    }
                    
                    
                }

                //ctx.clearRect(0, 0, width, height);

            }
        
    };
    setInterval(function(){ 
        ajax_func()
        
        
    }, 2000);
    
    $('#search').click(function(){
        if (!('webkitSpeechRecognition' in window)) {
            alert('此瀏覽器不支援語音辨識！')      
        } else {
            var show = document.getElementById('show');
            var recognition = new webkitSpeechRecognition()
            recognition.continuous=true
            recognition.interimResults=true
            ecognition.lang="cmn-Hant-TW"
            
            recognition.onstart=function(){
                console.log('開始辨識...')
                alert('start!')
            }
            recognition.onend=function(){
                console.log('停止辨識!')
            }
            recognition.onresult=function(event){
                var i = event.resultIndex
                var j = event.results[i].length-1
                show.innerHTML = event.results[i][j].transcript
                alert('show!')
            }

            recognition.start()   
            
        }
        var i = 1
        if(i == 1) show_path1()
        else if(i == 2) show_path2()
        else if(i == 3) show_path3()
        else if(i == 4) show_path4()
        //alert('path: '+i)
        
        
        
    });
     $('#canel').click(function(){
         var canvas = document.getElementById('canvas');

            if (canvas.getContext){
                var ctx = canvas.getContext('2d');
                width =  document.documentElement.clientWidth*0.85
                height = document.documentElement.clientHeight

                ctx.canvas.width  = width;
                ctx.canvas.height = height;
            }
        
        
    });
    $('#showpos').click(function(){
        alert('x: '+x + '\ny: ' +y)
    });

    
   

    
});


