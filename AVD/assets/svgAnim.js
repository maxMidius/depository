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
           if ( node.id == lookFor ) {
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
	this._draw=SVG(sel2).size(this._width, this_height)
	var container=this._draw.find('g')[1]
	this._xOff=container.transform().translateX
	this._yOff=container.transform().translateY
	this._sprite=this._draw.circle({cx:0, cy:0, r:7, fill:'red'} )
	console.log(`sprite created xoff=${this._xOff} yoff=${this._yOff}`)
    }
    //-----------------------------------
    fetchSvgAsHtml(svgUrl, width, height, appIdsObj, yourClickCB ) {
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
                       self.nodeInjectClickHandler(oneKey, appIdsObj[key], yourClickCB)
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
    // nodeId <-- y.node1
    // appId <-- TdsTrig (your app component name)
    // yourCB <-- your click handler
    nodeInjectClickHandler(someNodeId, appId, yourCB) {
         var someNode = this.svgLocateGroup(someNodeId)
         someNode.style('cursor: pointer')
         someNode.data("appId", appId )
         someNode.click( function(evt) {
            console.log(appId)
            yourCB(appId)
         } )
    }

    //----------------------------------
    /*
    SvgAnim.hSound = null ;

    SvgAnim.playSound = function(url) {
        if (SvgAnim.hSound && !SvgAnim.hSound.ended) {
            SvgAnim.hSound.pause()
            SvgAnim.hSound.currentTime=0
        }
        SvgAnim.hSound= new Audio(url)
        SvgAnim.hSound.loop = false ;
        SvgAnim.hSound.play()
    }

    //----------------------------------

    SvgAnim.stopSound = function() {
        if (SvgAnim.hSound && !SvgAnim.hSound.ended ) {
            console.log("stopping sound .." )
            SvgAnim.hSound.pause() 
            SvgAnim.hSound.currentTime = 0 
            SvgAnim.hSound = null
        }
    }
    */
    //----------------------------------
}

svgClick = function(x1)  {
    console.log(x1)
}

$(document).ready(function() {
    console.log("body Onload ...")
    svg1 = new SvgAnim("div1")
    svg1.fetchSvgAsHtml("/RuleManager.svg", 500, 500, {}, svgClick)
})
