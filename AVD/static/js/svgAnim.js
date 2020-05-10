/*
 * vi: sw=4 ts=4 expandtab
 */

class SvgAnim {
    //------------------------------
    // find a node whose id=lookFor
    svgLocateGroup(lookFor) {
        var grpList = this._draw.find('g')
        var i=0
        while (i < grpList.length) {
           var grp=grpList[i]
           if ( grp.node.id == lookFor ) {
               return grp
           }
           i++
        }
        return null
    }

    //--------------------------------
    constructor (svgDivId) {
    	this._svgDivId=svgDivId
	  this._nodeColors=[]
	    this._nodeList=[]
    }

    //--------------------------------
    svgLoadOK(data) {
        var sel1=`#${this._svgDivId}`
	var sel2=`#${this._svgDivId} svg`
	$(sel1).prepend(data)
	this._draw=SVG(sel2).size(this._width, this._height)
	var container=this._draw.find('g')[1]
	this._xOff=container.transform().translateX
	this._yOff=container.transform().translateY
	this._sprite=this._draw.circle({cx:0, cy:0, r:7, fill:'red'} )
	console.log(`sprite created xoff=${this._xOff} yoff=${this._yOff}`)
    }
    //-----------------------------------
    fetchSvgAsHtml(svgUrl, width, height, appIdsObj, arrowIdsObj, yourClickCB ) {
        this._width=width
        this._height=height
        console.log(`Fetching ${svgUrl}`)
        var self=this
        $.ajax (
            {
               url: svgUrl,
               dataType : 'html',
               type : 'GET',
               success: function(data) {
                   self.svgLoadOK(data)
                   for ( const oneKey of Object.keys(appIdsObj) ) {
                       self.nodeInjectClickHandler(oneKey, appIdsObj[oneKey], yourClickCB)
                   } 
                   for ( const oneKey of Object.keys(arrowIdsObj) ) {
                       self.nodeInjectClickHandler(oneKey, arrowIdsObj[oneKey], yourClickCB)
                   } 
               }, 
               error: function(err ) {
                   console.log(err)
               }
            }
        )
    }
    //---------------------------------
    // set some attrib to newValue - return prev value
    setNodeAttribute(someNodeId, attrName, newValue) {
        var nodeGrp=this.svgLocateGroup(someNodeId)
        if (nodeGrp != null ) { 
             var node2Fill = nodeGrp.node.instance.find('g')[0]
             const oldValue=node2Fill.attr(attrName)
             node2Fill.attr(attrName, newValue)
             return oldValue
        } else {
            return "_ERR_"
        }
    }
    //-----------------------------------
    // use this to reset color after some delay
    unsetNodeAttribute(someNodeId, attrName, someValue, delayInSecs) {
        var nodeGrp=this.svgLocateGroup(someNodeId)
        if (nodeGrp != null ) { 
             var node2Fill = nodeGrp.node.instance.find('g')[0]
             node2Fill.animate(delayInSecs*1000 ).after( function() { 
                node2Fill.attr(attrName, someValue)
                return "_OK_"
             } )
        } else {
            return "_ERR_"
        }
    }

    //-----------------------------------
    // nodeId <-- y.node1
    // appId <-- TdsTrig (your app component name)
    // yourCB <-- your click handler
    nodeInjectClickHandler(someNodeId, appId, yourCB) {
         console.log(`injecting  ${someNodeId} : ${appId}`)
         var someNode = this.svgLocateGroup(someNodeId)
         someNode.style('cursor: pointer')
         someNode.data("appId", appId )
         someNode.click( function(evt) {
            console.log(appId)
            yourCB(appId)
         } )
    }

    walkTheEdge(edgeId, dur ) {
       var traj = this.svgLocateGroup(edgeId) 
       var path1 = traj.find('path')[0].node.instance
       var delayMs = dur*1000 
       this._runner=this._sprite.animate(delayMs, '<>')
       self = this
       this._runner.during( function(pos, morph, eased) {
          var p = path1.pointAt (pos*path1.length() )
          self._sprite.center(p.x+self._xOff, p.y+self._yOff)
       } ).loop(1,true,0)
       return this._runner
    }

    triggerEdgeWalker (seqData, arrow2EdgeMap) {
       console.log("triggerEdgeWalker for",  seqData)
       let edgeId=arrow2EdgeMap[seqData[0].edge]
       let dur=seqData[0].dur
       let runner=this.walkTheEdge(edgeId, dur)
    }
}
//----------------------------------
// These are global functions - since 
// there can only be one sound playing at a time

hSound = null ;

playSound = function(url) {
    if (hSound && !hSound.ended) {
        hSound.pause()
        hSound.currentTime=0
    }
    hSound= new Audio(url)
    hSound.loop = false ;
    hSound.play()
}

//----------------------------------

stopSound = function() {
    if (hSound && !hSound.ended ) {
        console.log("stopping sound .." )
        hSound.pause() 
        hSound.currentTime = 0 
        hSound = null
    }
}
//----------------------------------

