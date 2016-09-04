/**
 * Created by arikarchmer on 9/1/16.
 */

var ConnectingParts = function() {
    
    var collided = function(x, y, size) {
        return Math.abs(x.x - y.x) < (size / 2) && Math.abs(x.y - y.y) < (size / 2)
    };
    
    var animateDrop = function(drop) {
        drop.y = drop.y + drop.vy;
        drop.x = drop.x + drop.vx;
        drop.iters = drop.iters + 1;
        if (drop.r < 1) {
            drop.r = drop.r + 0.001;
        }

        if (drop.x > canvas.width) {
            drop.vx = -drop.vx;
        }
        if (drop.x < 0) {
            drop.vx = -drop.vx;
        }
        if (drop.y > canvas.height) {
            drop.vy = -drop.vy;
        }
        if (drop.y < 0) {
            drop.vy = -drop.vy;
        }
    };
    
    var draw = function() {
        canvas.width = canvas.width;  // clear

        /* replace array */
        drops = new_drops;

        for (var j = 0; j < drops.length; j++) {
            var drop = drops[j];
            animateDrop(drop);
            ctx.fillStyle = drop.c;
            ctx.beginPath();
            ctx.arc(drop.x, drop.y, drop.r, 0, 2 * Math.PI, false);
            ctx.fill();
            
            var d2 = drops[i];
            ctx.strokeStyle = 'darkgray';
            ctx.beginPath();
            ctx.moveTo(drop.x, drop.y);
            ctx.lineTo(d2.x, d2.y);
            ctx.stroke();
        }
    };
    
    var animation = function() {
        draw();
        setTimeout(animation, 1);
    };
    
    return {
        collided: collided,
        animateDrop: animateDrop,
        draw: draw,
        animation: animation
    }
}();