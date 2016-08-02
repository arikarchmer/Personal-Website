/**
 * Created by arikarchmer on 7/20/16.
 */

var StarGame = function(){
    
    var stars = [];
    var colors = ['red', 'white', 'white'];

    /* private */
    
    var collided = function(x, y, size) {
        return Math.abs(x.x - y.x) < (size / 2) && Math.abs(x.y - y.y) < (size / 2)
    };

    /* public */
    
    var increaseDifficulty = function() {
        colors.push('red');
    };
    
    var createStars = function(num) {
        stars = [];
        for (var i = 0; i < num / 2; i++) {
            var s = {id: i, x: canvas.width * Math.random(), y: -5, r: 3 + Math.random() * 2, vx: 2 * Math.random() - 1,
                vy: 2 * Math.random() - 1, c: colors[Math.floor(colors.length * Math.random())]};
            stars.push(s);
        }
        for (var j = 0; j < num / 2; j++) {
            var s2 = {id: j, x: -5, y: canvas.height * Math.random(), r: 3 + Math.random() * 2, vx: 2 * Math.random() - 1,
                vy: 2 * Math.random() - 1, c: colors[Math.floor(colors.length * Math.random())]};
            stars.push(s2);
        }
    };
    
    var init = function(game_data) {
        game_data.powers = ['score', 'slow motion'];
        game_data.begin = false;
        createStars(200, colors);
    };

    var animate = function() {
        for (var i = 0; i < stars.length; i++) {
            var s = stars[i];
            s.x = s.x + s.vx;
            s.y = s.y + s.vy;
            if (s.x > canvas.width) {
                s.x = 1;
                s.y = Math.random() * canvas.height;
                s.vy = -s.vy;
            }
            if (s.x < 0) {
                s.x = canvas.width - 1;
                s.y = Math.random() * canvas.height;
                s.vy = -s.vy;
            }
            if (s.y > canvas.height) {
                s.y = 1;
                s.x = Math.random() * canvas.width;
                s.vx = -s.vx;
            }
            if (s.y < 0) {
                s.y = canvas.height;
                s.x = Math.random() * canvas.width;
                s.vx = -s.vx;
            }
        }
    };

    var checkCollisions = function(USER) {
        for (var i = 0; i < stars.length; i++) {
            var s = stars[i];
            if (collided(USER, s, USER.r)) {
                if (s.c == 'green') {
                    return {type: 'power'};
                }
                if (USER.c == s.c) {
                    return {type: 'hit', id: i};
                } else {
                    return {type: 'loss'};
                }
            }
        }
        return undefined;
    };
    
    var replaceStar = function(i) {
        stars.splice(i, 1);
        var new_s = {id: stars.length + 1, x: canvas.width * Math.random(), y: canvas.height * Math.random(),
            r: 3 + Math.random() * 2, vx: 2 * Math.random() - 1, vy: 2 * Math.random() - 1, c: "white"};
        stars.push(new_s);
    };
    
    var sparsify = function() {
        stars.splice(0, (stars.length / 2));
        setTimeout(function() {
            for (var i = 0; i < (stars.length / 4); i++) {
                var s = {id: i, x: canvas.width * Math.random(), y: -5, r: 3 + Math.random() * 2, vx: 2 * Math.random() - 1,
                    vy: 2 * Math.random() - 1, c: colors[Math.floor(colors.length * Math.random())]};
                stars.push(s);
            }
            for (var j = 0; j < (stars.length / 4); j++) {
                var s2 = {id: j, x: -5, y: canvas.height * Math.random(), r: 3 + Math.random() * 2, vx: 2 * Math.random() - 1,
                    vy: 2 * Math.random() - 1, c: colors[Math.floor(colors.length * Math.random())]};
                stars.push(s2);
            }
        }, 5000);
    };
    
    var warpspeed = function() {
        for (var i = 0; i < (stars.length); i++) {
            var s = stars[i];
            s.vx = 3 * s.vx;
            s.vy = 3 * s.vy;
        }
    };

    var slowMotion = function() {
        for (var i = 0; i < stars.length; i++) {
            var s = stars[i];
            s.vx = s.vx * 0.25;
            s.vy = s.vy * 0.25;
        }
        setTimeout(function () {
            for (var i = 0; i < stars.length; i++) {
                var s = stars[i];
                if (s.vx < 0.25 && s.vy < 0.25) {
                    s.vx = s.vx * 4;
                    s.vy = s.vy * 4;
                }
            }
        }, 5000)
    };
    
    var getStars = function() {
        return stars;
    };

    return {
        init: init,
        animate: animate,
        checkCollisions: checkCollisions,
        createStars: createStars,
        replaceStar: replaceStar,
        increaseDifficulty: increaseDifficulty,
        slowMotion: slowMotion,
        sparsify: sparsify,
        warpspeed: warpspeed,
        getStars: getStars
    }
}();

