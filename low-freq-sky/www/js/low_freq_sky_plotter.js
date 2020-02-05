//
// Client side of sky ploting code.
// Stephen Bourke
// Caltech, Oct 2013
// Onsala Space Observatory, Jul 2017
//

"use strict";

var LowFreqSkyPlotter = function(canvas_id) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    var plotRadius = 0.45 * Math.min(canvas.width, canvas.height);
    var skyData = null;
    var dateTimeText = "";
    var observatory = "ovro";
    var projection = "sin";
    
    var axesStroke = "rgba(0,0,0,0.4)";
    var axesFill = axesStroke;
    var axesWidth = 1;
    
    var skyObjectStroke = "rgba(0,0,255,1)";
    var skyObjectFill = "rgba(0,0,255,0.5)";
    var skyObjectRadius = plotRadius * 0.02;
    var skyObjectLineWidth = 1;
    
    var galaxyStroke = "rgba(0,64,255,0.5)";
    var galaxyWidth = 3;

    var clearCanvas = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    };
        
    var azel2canvas_linearDec = function(az, el) {
        // Function to convert from an AZ,EL value to
        // a position on the cavnas where the horizon
        // is at "plotRadius" distance from the center.
        //
        var x_1 = (1 - 2*el/Math.PI) * Math.sin(az);
        var y_1 = (1 - 2*el/Math.PI) * Math.cos(az);
        var x = canvas.width/2 - plotRadius*x_1;
        var y = canvas.height/2 - plotRadius*y_1;
        return [x, y];
    };
    
    var azel2canvas_sin = function(az, el) {
        // Function to convert from an AZ,EL value to
        // a position on the cavnas where the horizon
        // is at "plotRadius" distance from the center.
        //
        if (el < 0) {
           throw {
               name: "ValueError",
               message: "Sin projection error: Below Horizon"
           };
        }
        var x_1 = Math.sin(az) * Math.cos(el);
        var y_1 = Math.cos(az) * Math.cos(el);
        var x = canvas.width/2 - plotRadius*x_1;
        var y = canvas.height/2 - plotRadius*y_1;
        return [x, y];
    };
    
    var azel2canvas = function(az,el) {
        if (projection === "sin") {
            return azel2canvas_sin(az, el);
        } else {
            return azel2canvas_linearDec(az, el);
        }
    };
    
    var drawSkyObject = function(az, el, label) {
        try {
            var xy = azel2canvas(az, el);
        } catch (err) {
            return;
        }
        ctx.beginPath();
        ctx.strokeStyle = skyObjectStroke;
        ctx.fillStyle = skyObjectFill;
        ctx.lineWidth = skyObjectLineWidth;
        ctx.arc(xy[0], xy[1], 0.02*plotRadius, 0, 2*Math.PI);
        ctx.stroke();
        ctx.fill();
        ctx.fillText(label, xy[0] + 1.5*skyObjectRadius, xy[1]);
    };
    
    var drawGalaxy = function(points) {
        // Draw an arc (as line segments) between the provided points.
        ctx.beginPath();
        ctx.strokeStyle = galaxyStroke;
        ctx.lineWidth = galaxyWidth;
        var xy, line_initialised = false;
        for (var i in points) {
            try {
                xy = azel2canvas(points[i].AZ, points[i].EL);
            } catch (err) {
                continue;
            }
            if (!line_initialised) {
                ctx.moveTo(xy[0], xy[1]);
                line_initialised = true;
            } else {
                ctx.lineTo(xy[0], xy[1]);
            }
        }
        ctx.stroke();
    };
    
    var drawSources = function(sources) {
        for (var i in sources) {
            drawSkyObject(sources[i].AZ, sources[i].EL, sources[i].Name);
        }
    };
    
    var drawAxes = function() {
        // Draw circles
        ctx.strokeStyle = axesStroke;
        ctx.fillStyle = axesFill;
        ctx.lineWidth = axesWidth;
        for (var i=0; i<=1.01; i+=1/6) {
            ctx.beginPath();
            if (projection === "sin") {
                ctx.arc(canvas.width/2, canvas.height/2, plotRadius*Math.sin(Math.PI/2*i), 0, 2*Math.PI);
            } else {
                ctx.arc(canvas.width/2, canvas.height/2, plotRadius*i, 0, 2*Math.PI);
            }
            ctx.stroke();
        }
        // Draw vertical axis
        var len = 1.05 * plotRadius;
        ctx.beginPath();
        ctx.moveTo(canvas.width/2, canvas.height/2-len);
        ctx.lineTo(canvas.width/2, canvas.height/2+len);
        ctx.stroke();
        // Draw horizontal axis
        ctx.beginPath();
        ctx.moveTo(canvas.width/2-len, canvas.height/2);
        ctx.lineTo(canvas.width/2+len, canvas.height/2);
        ctx.stroke();
    };
    
    var drawSky = function() {
        clearCanvas();
        drawAxes();
        drawSources(skyData.sources);
        drawGalaxy(skyData.galaxy);
    };
    
    var updateSkyData = function(data) {
        skyData = data;
        drawSky();
    }

    var setDatetime = function(val) {
        dateTimeText = val;
        refresh();
    };
    
    var setProjection = function(val) {
        projection = val;
        refresh();
    };
    
    var setObservatory = function(val) {
        observatory = val;
        refresh();
    };
    
    var refresh = function() {
        $.ajax({
            dataType: "json",
            url: "/low-freq-sky-query/"+observatory+"/"+dateTimeText+"/",
            success: updateSkyData,
            cache: false
        });
    };

    return {
        drawAxes: drawAxes,
        setDatetime: setDatetime,
        setProjection: setProjection,
        setObservatory: setObservatory,
        refresh: refresh
    };
};
