$(document).ready(function(){
var timer = setInterval(function(){ajax_func()},2000);
var game = new Phaser.Game(900, 450, Phaser.AUTO, 'TutContainer', { preload: preload, create: create, update:update });
var upKey;
var downKey;
var leftKey;
var rightKey;

var IsNavigation = 1;
var line = 0;
var pre_dir = "nofacing";
//level array

/*var levelData=
[[1,1,1,1,1,1],
[1,0,0,0,0,1],
[1,0,1,2,0,1],
[1,0,0,0,0,1],
[1,0,0,0,0,1],
[1,1,1,1,1,1]];
*/
var levelData=
[[1,1,4,1,1,1,1,5,1],
[1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,1], 
[6,0,1,1,1,1,1,0,1],
[1,0,0,0,2,0,0,0,1],
[1,0,0,0,0,0,0,0,1],
[1,0,1,1,8,1,1,1,1]];

//x & y values of the direction vector for character movement
var pred_x;
var pred_y;
var dX=0;
var dY=0;
var tileWidth=50;// the width of a tile
var borderOffset = new Phaser.Point(350,50);//to centralise the isometric level display
var wallGraphicHeight=98;
var floorGraphicWidth=103;
var floorGraphicHeight=53;
var heroGraphicWidth=41;
var heroGraphicHeight=62;
var wallHeight=wallGraphicHeight-floorGraphicHeight; 
var heroHeight=(floorGraphicHeight/2)+(heroGraphicHeight-floorGraphicHeight)+6;//adjustments to make the legs hit the middle of the tile for initial load
var heroWidth= (floorGraphicWidth/2)-(heroGraphicWidth/2);//for placing hero at the middle of the tile
var facing='south';//direction the character faces
var sorcerer;//hero
var sorcererShadow;//duh
var shadowOffset=new Phaser.Point(heroWidth+7,11);
var bmpText;//title text
var normText;//text to display hero coordinates
var minimap;//minimap holder group
var heroMapSprite;//hero marker sprite in the minimap
var gameScene;//this is the render texture onto which we draw depth sorted scene
var floorSprite;
var wallSprite;
var ovenSprite;
var eggSprite;
var woodfloorSprite;
var washmachineSprite;
var woodSprite;
var detergentSprite;
var meatSprite;
var chrisSprite;
var tntSprite;
var naviSprite;
var heroMapTile;//hero tile values in array
var heroMapPos;//2D coordinates of hero map marker sprite in minimap, assume this is mid point of graphic
var heroSpeed=1;//well, speed of our hero 


function preload() {
		game.load.crossOrigin='Anonymous';
    //load all necessary assets
    game.load.bitmapFont('font', 'https://dl.dropboxusercontent.com/s/z4riz6hymsiimam/font.png?dl=0', 'https://dl.dropboxusercontent.com/s/7caqsovjw5xelp0/font.xml?dl=0');
    game.load.image('greenTile', 'https://dl.dropboxusercontent.com/s/nxs4ptbuhrgzptx/green_tile.png?dl=0');
    game.load.image('blueTile', './images/blue_tile.png');
    game.load.image('orangeTile', './images/orange_tile.png');
    game.load.image('redTile', 'https://dl.dropboxusercontent.com/s/zhk68fq5z0c70db/red_tile.png?dl=0');
    game.load.image('heroTile', 'https://dl.dropboxusercontent.com/s/8b5zkz9nhhx3a2i/hero_tile.png?dl=0');
    game.load.image('heroShadow', 'https://dl.dropboxusercontent.com/s/sq6deec9ddm2635/ball_shadow.png?dl=0');
    game.load.image('floor', 'https://dl.dropboxusercontent.com/s/h5n5usz8ejjlcxk/floor.png?dl=0');
    game.load.image('wall', 'https://dl.dropboxusercontent.com/s/uhugfdq1xcwbm91/block.png?dl=0');
    game.load.image('detergent', './images/detergent_block.png');
    game.load.image('washmachine', './images/washmachine.png');
    game.load.image('chris', './images/chris.png');
    game.load.image('meat', './images/meat.png');
    game.load.image('tnt', './images/tnt.png');
    game.load.image('oven', './images/oven.png');
    game.load.image('wood', './images/wood.png');
    game.load.image('egg', './images/egg.png');
    game.load.image('woodfloor', './images/woodfloor.png');
    game.load.image('navi', './images/navi.png');
    game.load.image('ball', 'https://dl.dropboxusercontent.com/s/pf574jtx7tlmkj6/ball.png?dl=0');
    game.load.atlasJSONArray('hero', 'https://dl.dropboxusercontent.com/s/hradzhl7mok1q25/hero_8_4_41_62.png?dl=0', 'https://dl.dropboxusercontent.com/s/95vb0e8zscc4k54/hero_8_4_41_62.json?dl=0');
}

function create() {
    bmpText = game.add.bitmapText(10, 10, 'font', 'ES Mart Map', 20);
    normText=game.add.text(10,360,"hi");
    upKey = game.input.keyboard.addKey(Phaser.Keyboard.UP);
    downKey = game.input.keyboard.addKey(Phaser.Keyboard.DOWN);
    leftKey = game.input.keyboard.addKey(Phaser.Keyboard.LEFT);
    rightKey = game.input.keyboard.addKey(Phaser.Keyboard.RIGHT);
    game.stage.backgroundColor = '#cccccc';
    //we draw the depth sorted scene into this render texture
    gameScene=game.add.renderTexture(game.width,game.height);
    game.add.sprite(0, 0, gameScene);
    floorSprite= game.make.sprite(0, 0, 'floor');
    wallSprite= game.make.sprite(0, 0, 'wall');
    woodSprite= game.make.sprite(0, 0, 'wood');
    detergentSprite= game.make.sprite(0, 0, 'detergent');
    washmachineSprite= game.make.sprite(0, 0, 'washmachine');
    ovenSprite= game.make.sprite(0, 0, 'oven');
    tntSprite= game.make.sprite(0, 0, 'tnt');
    meatSprite= game.make.sprite(0, 0, 'meat');
   chrisSprite= game.make.sprite(0, 0, 'chris');
    naviSprite= game.make.sprite(0, 0, 'navi');
    eggSprite= game.make.sprite(0, 0, 'egg');
    woodfloorSprite= game.make.sprite(0, 0, 'woodfloor');
    sorcererShadow=game.make.sprite(0,0,'heroShadow');
    sorcererShadow.scale= new Phaser.Point(0.5,0.6);
    sorcererShadow.alpha=0.4;
    createLevel();
    ajax_func();

}

function update(){
    //check key press
    //detectKeyInput();
    pos = predictPos();
	if(pos == null){
		dX = 0
		dY = 0
	}else{
		dX = pos[0];
    	dY = pos[1];
    }
	/*
    if(pos[0]==0){
        if(pos[1]>0){
            facing = "south";
        }else
            facing = "north";
            
    }else if(pos[1]==0){
        if(pos[0]>0){
            facing = "east";
        }else
            facing = "west";
            
    }*/
    
    //if no key is pressed then stop else play walking animation
    if (dY == 0 && dX == 0)
    {
        sorcerer.animations.stop();
        sorcerer.animations.currentAnim.frame=0;
    }else{
        if(sorcerer.animations.currentAnim!=facing){
            sorcerer.animations.play(facing);
        }
    }
    //check if we are walking into a wall else move hero in 2D
    
    
    if (isWalkable())
    {   
        
        
        heroMapPos.x +=  heroSpeed * dX;
        heroMapPos.y +=  heroSpeed * dY;
        //heroMapPos.x = 375;
        //heroMapPos.y = 175;
        heroMapSprite.x=heroMapPos.x-heroMapSprite.width/2;
        heroMapSprite.y=heroMapPos.y-heroMapSprite.height/2;
        //get the new hero map tile
        heroMapTile=getTileCoordinates(heroMapPos,tileWidth);
        
        //depthsort & draw new scene
        renderScene();
    }
}

function createLevel(){//create minimap
    minimap= game.add.group();
    var tileType=0;
    for (var i = 0; i < levelData.length; i++)
    {
        for (var j = 0; j < levelData[0].length; j++)
        {
            tileType=levelData[i][j];
            placeTile(tileType,i,j);
            if(tileType==2){//save hero map tile
               heroMapTile=new Phaser.Point(i,j);
            }
        }
    }
    addHero();
    heroMapSprite=minimap.create(heroMapTile.y * tileWidth, heroMapTile.x * tileWidth, 'heroTile');
    heroMapSprite.x+=(tileWidth/2)-(heroMapSprite.width/2);
    heroMapSprite.y+=(tileWidth/2)-(heroMapSprite.height/2);
    //heroMapPos=new Phaser.Point(heroMapSprite.x+heroMapSprite.width/2,heroMapSprite.y+heroMapSprite.height/2);
    heroMapPos=new Phaser.Point(225,225); //起始位置
    heroMapTile=getTileCoordinates(heroMapPos,tileWidth);
    minimap.scale= new Phaser.Point(0.3,0.3);
    minimap.x=690;
    minimap.y=10;
    renderScene();//draw once the initial state
}
function addHero(){
    // sprite
    sorcerer = game.add.sprite(-50, 0, 'hero', '1.png');// keep him out side screen area
   
    // animation
    sorcerer.animations.add('southeast', ['1.png','2.png','3.png','4.png'], 6, true);
    sorcerer.animations.add('south', ['5.png','6.png','7.png','8.png'], 6, true);
    sorcerer.animations.add('southwest', ['9.png','10.png','11.png','12.png'], 6, true);
    sorcerer.animations.add('west', ['13.png','14.png','15.png','16.png'], 6, true);
    sorcerer.animations.add('northwest', ['17.png','18.png','19.png','20.png'], 6, true);
    sorcerer.animations.add('north', ['21.png','22.png','23.png','24.png'], 6, true);
    sorcerer.animations.add('northeast', ['25.png','26.png','27.png','28.png'], 6, true);
    sorcerer.animations.add('east', ['29.png','30.png','31.png','32.png'], 6, true);
}
function placeTile(tileType,i,j){//place minimap
    var tile='greenTile';
    if(tileType==1){
        tile='redTile';
    }else if(tileType==3){
        tile='blueTile';
    }else if(tileType>=4){
        tile='orangeTile';
    }
    minimap.create(j * tileWidth, i * tileWidth, tile);
}
function renderScene(){
    gameScene.clear();//clear the previous frame then draw again
    var tileType=0;
    for (var i = 0; i < levelData.length; i++){ //clear map
            for (var j = 0; j < levelData[0].length; j++){
                if(levelData[i][j]==3)
                    levelData[i][j]=0;
            }
        }
    if(IsNavigation==1){
        //alert(heroMapTile.x);
        NaviPath(line);
        //levelData[6][1]=1;
    }
    for (var i = 0; i < levelData.length; i++)
    {
        for (var j = 0; j < levelData[0].length; j++)
        {
            
            tileType=levelData[i][j];
            placeTile(tileType,i,j);
            drawTileIso(tileType,i,j);
            if(i==heroMapTile.y&&j==heroMapTile.x){
                drawHeroIso();
            }
        }
    }
    //normText.text='Customer is on x,y: '+heroMapTile.x +','+heroMapTile.y;
    //normText.text='Customer is on x,y: '+Math.round(heroMapPos.x) +','+Math.round(heroMapPos.y);
    normText.text=''
}
function drawHeroIso(){
    var isoPt= new Phaser.Point();//It is not advisable to create points in update loop
    var heroCornerPt=new Phaser.Point(heroMapPos.x-heroMapSprite.width/2,heroMapPos.y-heroMapSprite.height/2); //hero 位置
    isoPt=cartesianToIsometric(heroCornerPt);//find new isometric position for hero from 2D map position
    gameScene.renderXY(sorcererShadow,isoPt.x+borderOffset.x+shadowOffset.x, isoPt.y+borderOffset.y+shadowOffset.y, false);//draw shadow to render texture
    gameScene.renderXY(sorcerer,isoPt.x+borderOffset.x+heroWidth, isoPt.y+borderOffset.y-heroHeight, false);//draw hero to render texture
}
function drawTileIso(tileType,i,j){//place isometric level tiles
    var isoPt= new Phaser.Point();//It is not advisable to create point in update loop
    var cartPt=new Phaser.Point();//This is here for better code readability.
    cartPt.x=j*tileWidth;
    cartPt.y=i*tileWidth;
    isoPt=cartesianToIsometric(cartPt);
    if(tileType==1){
        gameScene.renderXY(woodSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-wallHeight, false);
    }else if(tileType==0 || tileType ==2){
        gameScene.renderXY(woodfloorSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y, false);
    }else if(tileType ==3){
        gameScene.renderXY(naviSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y, false);
    }else if(tileType ==4){
        gameScene.renderXY(washmachineSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-wallHeight, false);
    }else if(tileType ==5){
        gameScene.renderXY(meatSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-wallHeight, false);
    }else if(tileType ==6){
        gameScene.renderXY(ovenSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-wallHeight, false);
    }else if(tileType ==7){
        gameScene.renderXY(tntSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-wallHeight, false);
    }else if(tileType ==8){
        gameScene.renderXY(eggSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-wallHeight, false);
    }else if(tileType ==9){
        gameScene.renderXY(chrisSprite, isoPt.x+borderOffset.x, isoPt.y+borderOffset.y-1.665*wallHeight, false);
    }
}
function isWalkable(){//It is not advisable to create points in update loop, but for code readability.
    var able=true;
    var heroCornerPt=new Phaser.Point(heroMapPos.x-heroMapSprite.width/2,heroMapPos.y-heroMapSprite.height/2);
    var cornerTL =new Phaser.Point();
    cornerTL.x=heroCornerPt.x +  (heroSpeed * dX);
    cornerTL.y=heroCornerPt.y +  (heroSpeed * dY);
    // now we have the top left corner point. we need to find all 4 corners based on the map marker graphics width & height
    //ideally we should just provide the hero a volume instead of using the graphics' width & height
    var cornerTR =new Phaser.Point();
    cornerTR.x=cornerTL.x+heroMapSprite.width;
    cornerTR.y=cornerTL.y;
    var cornerBR =new Phaser.Point();
    cornerBR.x=cornerTR.x;
    cornerBR.y=cornerTL.y+heroMapSprite.height;
    var cornerBL =new Phaser.Point();
    cornerBL.x=cornerTL.x;
    cornerBL.y=cornerBR.y;
    var newTileCorner1;
    var newTileCorner2;
    var newTileCorner3=heroMapPos;
    //let us get which 2 corners to check based on current facing, may be 3
    switch (facing){
        case "north":
            newTileCorner1=cornerTL;
            newTileCorner2=cornerTR;
        break;
        case "south":
            newTileCorner1=cornerBL;
            newTileCorner2=cornerBR;
        break;
        case "east":
            newTileCorner1=cornerBR;
            newTileCorner2=cornerTR;
        break;
        case "west":
            newTileCorner1=cornerTL;
            newTileCorner2=cornerBL;
        break;
        case "northeast":
            newTileCorner1=cornerTR;
            newTileCorner2=cornerBR;
            newTileCorner3=cornerTL;
        break;
        case "southeast":
            newTileCorner1=cornerTR;
            newTileCorner2=cornerBR;
            newTileCorner3=cornerBL;
        break;
        case "northwest":
            newTileCorner1=cornerTR;
            newTileCorner2=cornerBL;
            newTileCorner3=cornerTL;
        break;
        case "southwest":
            newTileCorner1=cornerTL;
            newTileCorner2=cornerBR;
            newTileCorner3=cornerBL;
        break;
    }
    //check if those corners fall inside a wall after moving
    newTileCorner1=getTileCoordinates(newTileCorner1,tileWidth);
    if(levelData[newTileCorner1.y][newTileCorner1.x]==1){
        able=false;
    }
    newTileCorner2=getTileCoordinates(newTileCorner2,tileWidth);
    if(levelData[newTileCorner2.y][newTileCorner2.x]==1){
        able=false;
    }
    newTileCorner3=getTileCoordinates(newTileCorner3,tileWidth);
    if(levelData[newTileCorner3.y][newTileCorner3.x]==1){
        able=false;
    }
    return able;
}
function detectKeyInput(){//assign direction for character & set x,y speed components
    if (upKey.isDown)
    {
        dY = -1;
    }
    else if (downKey.isDown)
    {
        dY = 1;
    }
    else
    {
        dY = 0;
    }
    if (rightKey.isDown)
    {
        dX = 1;
        if (dY == 0)
        {
            facing = "east";
        }
        else if (dY==1)
        {
            facing = "southeast";
            dX = dY=0.5;
        }
        else
        {
            facing = "northeast";
            dX=0.5;
            dY=-0.5;
        }
    }
    else if (leftKey.isDown)
    {
        dX = -1;
        if (dY == 0)
        {
            facing = "west";
        }
        else if (dY==1)
        {
            facing = "southwest";
            dY=0.5;
            dX=-0.5;
        }
        else
        {
            facing = "northwest";
            dX = dY=-0.5;
        }
    }
    else
    {
        dX = 0;
        if (dY == 0)
        {
            //facing="west";
        }
        else if (dY==1)
        {
            facing = "south";
        }
        else
        {
            facing = "north";
        }
    }
}

function cartesianToIsometric(cartPt){
    var tempPt=new Phaser.Point();
    tempPt.x=cartPt.x-cartPt.y;
    tempPt.y=(cartPt.x+cartPt.y)/2;
    return (tempPt);
}
function isometricToCartesian(isoPt){
    var tempPt=new Phaser.Point();
    tempPt.x=(2*isoPt.y+isoPt.x)/2;
    tempPt.y=(2*isoPt.y-isoPt.x)/2;
    return (tempPt);
}
function getTileCoordinates(cartPt, tileHeight){
    var tempPt=new Phaser.Point();
    tempPt.x=Math.floor(cartPt.x/tileHeight);
    tempPt.y=Math.floor(cartPt.y/tileHeight);
    return(tempPt);
}
function getCartesianFromTileCoordinates(tilePt, tileHeight){
    var tempPt=new Phaser.Point();
    tempPt.x=tilePt.x*tileHeight;
    tempPt.y=tilePt.y*tileHeight;
    return(tempPt);
}
function NaviPath(line){
    navilabel = 3;
    if(line == 0){
        //target:(2,0)
        x = heroMapTile.x;
        y = heroMapTile.y;
        if(y==4){
            for (var i = 1; i <=x ; i++){
                levelData[4][i] = 3;
            }
            levelData[3][1] = navilabel;
            levelData[2][1] = navilabel;
            levelData[1][1] = navilabel;
            levelData[1][2] = navilabel;
        }else if(x==1 && y!=4){
            for (var j = 1; j <=y ; j++){
                levelData[j][1] = navilabel;
            }
            levelData[1][2] = navilabel;
        }else if(x==7 && y!=4){
            for (var i = 2; i <=6 ; i++){
                levelData[1][i] = navilabel;
            }
             for (var j = 1; j <=y ; j++){
                levelData[j][7] = navilabel;
             }
        }
        else if(y == 1 && x!=1 && x!=7){
            for (var i = 2; i <=x ; i++){
                levelData[1][i] = navilabel;
            }
        }
        
        
    }
   
     
}
function predictPos(){
    
    //var location = ajax_func();
    //console.log(location)
    //pred_x = 1;
    //pred_y = 1;
    //pred_x = location.x;
    //pred_y = location.y;

    var pred_x_pos = 75 + (pred_x-1)*50;
    var pred_y_pos = 75 + (pred_y-1)*50;
    //console.log(pre_dir)
    if(heroMapPos.x == pred_x_pos && heroMapPos.y == pred_y_pos)
        return [0,0];
    else{
        if(heroMapPos.x > 75 && heroMapPos.x < 375 &&  pred_x_pos > 75 && pred_x_pos < 375 && heroMapPos.y != pred_y_pos){
            if(heroMapPos.x > 225){
                facing = "east";
                pre_dir = facing;
                return [0.5,0];
            }else{
                facing = "west";
                pre_dir = facing;
                return [-0.5,0];
            }
        }else if(heroMapPos.y < 225 && heroMapPos.y > 75 && pred_y_pos <225 && pred_y_pos >75 && heroMapPos.x != pred_x_pos ){
            if(heroMapPos.y > 150){

                facing = "south";
                if(pre_dir == "north"){
                    pre_dir = facing;
                    //pre_dir = facing;
                    return [0,-0.5];
                    
                
                }else{

                    pre_dir = facing;
                    
                    return [0,0.5];
                }
                
            }else{
                
                facing = "north";
                if(pre_dir == "south"){
                    pre_dir = facing;
                    return [0,0.5];
                    
                }else{
                    pre_dir = facing;
                    return [0,-0.5];
                }
                
            }
        }else{
            if( (heroMapPos.x == 75 || heroMapPos.x == 375) && heroMapPos.y > pred_y_pos){
                facing="north";
                if(pre_dir == "south"){
                    pre_dir = facing;
                    return [0,0.5];
                    
                }
                else{
                    pre_dir = facing;
                    return [0,-0.5];
                    console.log("fuck");
                }
                
            }else if( (heroMapPos.x == 75 || heroMapPos.x == 375) && heroMapPos.y < pred_y_pos){
                facing="south";
                if(pre_dir == "north"){
                     pre_dir = facing ;
                    return [0,-0.5];
                }
                else{
                    pre_dir = facing;
                    return [0,0.5];
                }
                
            }
            
            if( (heroMapPos.y == 75 || heroMapPos.y == 225) && heroMapPos.x > pred_x_pos){
                facing="west";
                if(pre_dir == "east"){
                    pre_dir = facing ;
                    return [0.5,0];
                }
                else{
                    pre_dir = facing;
                    return [-0.5,0];
                }
                
            }
            else if( (heroMapPos.y == 75 || heroMapPos.y == 225) && heroMapPos.x < pred_x_pos){
                facing="east";
                if(pre_dir == "west"){
                     pre_dir = facing;
                    return [-0.5,0];
                }
                else{
                    pre_dir = facing;
                    return [0.5,0];
                }
                
            }
        
        }
        
    }

    
    
}
function ajax_func(){
      var location;
      $.ajax({
                url: '/predictLocation',
                type: 'GET',
                cache:false,
                //async:false,
                data: {
                    'mode':1,
                },
                error: function(xhr) {
                    console.log('location Ajax request 發生錯誤');
                },
                success: function(response) {
                    //alert("ajax success");
                    location = response;
                    pred_x = location.x;
                    pred_y = location.y;
                    console.log(location);
                }
          
        });
    //alert(location);
    //return location;
    //pred_x = location.x;
    //pred_y = location.y;
    //console.log(location);
};

var Ajax_Barcode = function(){
      $.ajax({
                url: '/Ajax_Barcode',
                type: 'GET',
                data: {
                    'mode':1,
                },
                error: function(xhr) {
                    console.log('barcode Ajax request 發生錯誤');
                },
                success: function(response) {
                    alert(response.barcodeData)
                }

        });
    };

  var ajax_audio = function(){
      $.ajax({
                url: '/Ajax_Audio',
                type: 'GET',
                data: {
                    'mode':1,
                },
                error: function(xhr) {
                    console.log('Ajax Audio 發生錯誤');
                },
                success: function(response) {
					IsNavigation = 1;
					line = response.path;
                		
				}

        });
    };

	$('#search').click(function(){
        ajax_audio()
    });
    $('#scan').click(function(){
        //Ajax_Barcode()
    });

     $('#canel').click(function(){
		IsNavigation = 0;
    });
    $('#showpos').click(function(){
        alert('customer is on x:'+pred_x + '  y:' +pred_y)
    	//normText.text='Customer is on x,y: '+ pred_x+',' + pred_y;
		//setTimeout('normText.text=""',3000);
	});



    
}); //document ready
