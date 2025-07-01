var pzpr = require('pzpr');

var arg = process.argv[2];
const grid = JSON.parse(arg);
var puzzle = new pzpr.Puzzle();
puzzle.open(`fillomino/${grid.length}/${grid.length}`)
for (let i = 0; i < grid.length; i++) {
    row = grid[i];
    for (let j=0; j < row.length; j++){
        number = row[j];
        if (number != 0) {
            cx = 2 * i + 1;
            cy = 2 * j + 1;
            puzzle.board.getc(cy,cx).qnum = number;
        }
    }   
}

console.log(puzzle.getURL());
