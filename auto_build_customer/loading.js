(function(){
    var scene = new cc.Scene()
    var sp = new cc.Sprite("res/SplashScene/loading.jpg")
    var glView = cc.director.getOpenGLView();
    glView.setDesignResolutionSize(2208 , 1242 , 1)
    scene.addChild(sp)
    sp.setAnchorPoint(cc.p(0 , 0))
    sp.setPosition(cc.p(0 , 0))
    sp.setScale(cc.director.getWinSize().width / sp.getContentSize().width ,cc.director.getWinSize().height/sp.getContentSize().height)
    cc.director.runWithScene(scene)
})()