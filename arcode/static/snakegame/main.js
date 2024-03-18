var res = 20;
var s;
var col;
var row;
var score = 0;
var lastTime = 0;
var directionChangeInterval = 3000; // Change direction every 3 seconds

/* creating the square to play */
function setup() {
  createCanvas(400, 400);
  col = floor(width / res);
  row = floor(height / res);
  frameRate(5);
  s = new Snake();
}

function draw() {
  scale(res);
  background(50);
  
  // Check for direction change every 3 seconds
  if (millis() - lastTime > directionChangeInterval) {
    lastTime = millis();
    var randomDir = floor(random(4)); // Generate a random direction
    if (randomDir === 0) {
      s.setDir(-1, 0); // LEFT
    } else if (randomDir === 1) {
      s.setDir(1, 0); // RIGHT
    } else if (randomDir === 2) {
      s.setDir(0, -1); // UP
    } else if (randomDir === 3) {
      s.setDir(0, 1); // DOWN
    }
  }
  
  s.show();
  s.update();

  // Keep the snake within the canvas
  if (s.x > col - 1) {
    s.x = 0;
  } else if (s.x < 0) {
    s.x = col - 1;
  }
  if (s.y > row - 1) {
    s.y = 0;
  } else if (s.y < 0) {
    s.y = row - 1;
  }
  
  noStroke();
  fill(255, 100, 300);
}

function keyPressed() {
  // Check if Enter is pressed to increase snake's length
  if (keyCode === ENTER) {
    s.total++;
    score++; // Increase score
  } else {
    // Change the snake's direction based on arrow keys
    if (keyCode === LEFT_ARROW && s.xSpeed !== 1) {
      s.setDir(-1, 0);
    } else if (keyCode === RIGHT_ARROW && s.xSpeed !== -1) {
      s.setDir(1, 0);
    } else if (keyCode === DOWN_ARROW && s.ySpeed !== -1) {
      s.setDir(0, 1);
    } else if (keyCode === UP_ARROW && s.ySpeed !== 1) {
      s.setDir(0, -1);
    }
  }
}

function Snake() {
  this.x = 0;
  this.y = 0;
  this.xSpeed = 1;
  this.ySpeed = 0;
  this.total = 0;
  this.tail = [];

  this.update = function() {
    // Update the snake's position based on speed
    if (this.total === this.tail.length) {
      for (var i = 0; i < this.tail.length - 1; i++) {
        this.tail[i] = this.tail[i + 1];
      }
    }

    this.tail[this.total - 1] = createVector(this.x, this.y);
    
    this.x += this.xSpeed;
    this.y += this.ySpeed;
  };

  this.show = function() {
    // Render the snake's body
    for (var i = 0; i < this.tail.length; i++) {
      fill(255, 0, 0);
      strokeWeight(0.1);
      stroke(0);
      rect(this.tail[i].x, this.tail[i].y, 1, 1);
    }
    fill(255);
    strokeWeight(0.1);
    stroke(0);
    rect(this.x, this.y, 1, 1);
  };

  this.setDir = function(x, y) {
    // Set the direction of the snake
    this.xSpeed = x;
    this.ySpeed = y;
  };
}