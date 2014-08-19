function makeGame(gridSize, numMines) {
/**
* makeGame takes two ints as parameters for the grid size and number of mines.
* it creates a table where the tds have ids like "tile0103".
* the four digits are a pair of two digit ints correspoding to the row and
* column of the tile (zero-indexed). The three function calls at the end
* then add mines and numbers to the table and then adds the click function to
* each tile.
*/
  var theTable = $("#mineSweeperGame");
  theTable.html('');
  var trCounter = 0;
  for(var x=0; x<gridSize; x++) {
    var tdCounter = 0;
    var trString = '<tr>';
    for(var y=0; y<gridSize; y++) {
      trString += '<td id="tile' + pad2(trCounter) + pad2(tdCounter) + '"></td>';
      tdCounter += 1
    }
    trString += '</tr>';
    theTable.append(trString);
    trCounter += 1;
  }
  addMines(numMines);
  addAllNumbers();
  makeClickable();
}
function borderingTiles(td){
/**
* borderingTiles takes a jquery object of a td in the game as a parameter
* it returns an array of jquery objects of the all the bordering tds.
*/
  var borderingArray = [];
  var tileID = td.attr('id');
  var tileTR = parseInt(tileID.slice(4,6), 10);
  var tileTD = parseInt(tileID.slice(6), 10);
  var right = $('#tile' + pad2(tileTR) + pad2(tileTD + 1) );
  if (right.length > 0){
    borderingArray.push(right);
  }
  var left = $('#tile' + pad2(tileTR) + pad2(tileTD - 1) );
  if (left.length > 0){
    borderingArray.push(left);
  }
  var downRight = $('#tile' + pad2(tileTR + 1) + pad2(tileTD + 1) );
  if (downRight.length > 0){
    borderingArray.push(downRight);
  }
  var down = $('#tile' + pad2(tileTR + 1) + pad2(tileTD) );
  if (down.length > 0){
    borderingArray.push(down);
  }
  var downLeft = $('#tile' + pad2(tileTR + 1) + pad2(tileTD - 1) );
  if (downLeft.length > 0){
    borderingArray.push(downLeft);
  }
  var upRight = $('#tile' + pad2(tileTR - 1) + pad2(tileTD + 1) );
  if (upRight.length > 0){
    borderingArray.push(upRight);
  }
  var up = $('#tile' + pad2(tileTR - 1) + pad2(tileTD) );
  if (up.length > 0){
    borderingArray.push(up);
  }
  var upLeft = $('#tile' + pad2(tileTR - 1) + pad2(tileTD - 1) );
  if (upLeft.length > 0){
    borderingArray.push(upLeft);
  }
  return borderingArray;
}
function revealTile(td){
/**
* revealTile takes a jquery object of a td in the game as a parameter
* it checks for classes like 'mine' and 'borders2' to see what it should reveal
* and then changes the text and css accordingly.
* If tiles have the 'flagged' class, we don't reveal them when clicked.
* Also, when we reveal tiles not bordering any mines, we want to reveal all bordering tiles.
* This is called recursively to reveal the area on the board not bordering any mines.
*/
  if (!td.hasClass('flagged')){
    td.addClass('revealed');
    td.css("background-color","#aaa");
    if (td.hasClass('mine')){
      td.html('<img src="/img/glyphicons_021_snowflake.png" />');
      td.css("background-color","#f00");
      validateGame();
    } else if (td.hasClass('borders0')){
      var borderTiles = borderingTiles(td);
      for (i in borderTiles){
        if (!borderTiles[i].hasClass('revealed')){
          revealTile(borderTiles[i]);
        }
      }
    } else if (td.hasClass('borders1')){
      td.text('1');
      td.css("color",colorForNumber(1));
    } else if (td.hasClass('borders2')){
      td.text('2');
      td.css("color",colorForNumber(2));
    } else if (td.hasClass('borders3')){
      td.text('3');
      td.css("color",colorForNumber(3));
    } else if (td.hasClass('borders4')){
      td.text('4');
      td.css("color",colorForNumber(4));
    } else if (td.hasClass('borders5')){
      td.text('5');
      td.css("color",colorForNumber(5));
    } else if (td.hasClass('borders6')){
      td.text('6');
      td.css("color",colorForNumber(6));
    } else if (td.hasClass('borders7')){
      td.text('7');
      td.css("color",colorForNumber(7));
    } else if (td.hasClass('borders8')){
      td.text('8');
      td.css("color",colorForNumber(8));
    }
    td.css("border","1px solid");
    td.css("border-color","#777");
    td.css("height","38px");
    td.css("width","38px");
  }
}
function flagTile(td){
/**
* flagTile takes a jquery object of a td in the game as a parameter
* If the tile is not already flagged, it adds a class of 'flagged' to the td and adds a flag
* otherwise, both are removed.
*/
  if (td.hasClass('flagged')){
    td.removeClass('flagged');
    td.text('');
  } else {
    if (!td.hasClass('revealed')){
      td.addClass('flagged');
      td.html('<img src="/img/glyphicons_266_flag.png" />');
    }
  }
}
function addNumber(td){
/**
* addNumber takes a jquery object of a td in the game as a parameter
* it counts how many bordering tiles have the class of 'mine' and adds a class
* of 'bordersX' where X is the number of mines it borders.
*/
  if (td.hasClass('notmine')){
    var numMines = 0;
    var borderTiles = borderingTiles(td);
    for (a in borderTiles){
      if (borderTiles[a].hasClass('mine')){
        numMines += 1;
      }
    }
    td.addClass('borders' + numMines);
  }
}
function addAllNumbers(){
/**
* addAllNumbers finds all the tds in the game and runs addNumber on them.
*/
  $('td').each(function(index) {
    addNumber($(this));
  });
}
function makeClickable(){
/**
* makeClickable adds the click functionality to all the tds in the game
* for each click, it first checks if the game is over and then if the '#clickFlags'
* checkbox is checked and then calls flagTile or revealTile appropriately.
*/
  $('td').each(function(index) {
    $(this).click(function() {
      if (!$("#mineSweeperGame").hasClass('gameOver')){
        if ($('#clickFlags').is(':checked')){
          flagTile($(this));
        } else {
          revealTile($(this));
        }
      }
    });
  });
}
function pad2(number) {
/**
* pad2 takes a positive int 0 <= number < 100 and returns a 2 digit zero padded string
*/
  var str = '' + number;
  while (str.length < 2) {
    str = '0' + str;
  }
  return str;
}
function colorForNumber(number){
/**
* colorForNumber takes an int and returns the css color for text for tiles bordering mines.
* borrowed from http://inflashstudios.com/minesweeper/tutorial-3.aspx
*/
  if (number == 1){
    return '#0004FF';
  }
  else if (number == 2){
    return '#007000';
  }
  else if (number == 3){
    return '#FE0100';
  }
  else if (number == 4){
    return '#05006C';
  }
  else if (number == 5){
    return '#840800';
  }
  else if (number == 6){
    return '#008284';
  }
  else if (number == 7){
    return '#840084';
  }
  else {
    return '#000000'
  }
}
function addMines(numMines){
/**
* addMines takes an int for the number of mines and adds them to the game.
* for each tile, randomNum is a random int from zero to the number of remaining tiles -1.
* if randomNum is less than the number of mines we still need to add, we add a class of 'mine'.
* otherwise we add a class of 'notmine'
*/
  var tds = $("td");
  var tilesLeft = tds.length;
  var minesLeft = numMines;
  $('td').each(function(index) {
    var randomNum = Math.floor(Math.random()*tilesLeft);
    if (randomNum < minesLeft){
      $(this).addClass('mine');
      minesLeft -= 1;
    } else {
      $(this).addClass('notmine');
    }
    tilesLeft -= 1;
  });
}
function cheatGame(){
/**
* cheatGame reveals all tds that don't have the class of 'mine'
*/
  $('td').each(function(index) {
    if (!$(this).hasClass('mine')){
      revealTile($(this));
    }
  });
}
function isGameWon(){
/**
* isGameWon checks every td with a class of 'notmine' to see if it has been revealed.
* if so, it returns true, otherwise, returns false.
*/
  var returnVal = true;
  $('.notmine').each(function() {
    if (!$(this).hasClass('revealed')){
      returnVal = false;
    }
  });
  return returnVal;
}
function endGameWin(){
/**
* endGameWin congratulates the user, shows flags where the mines were, and adds the
* gameOver class to the table to prevent further clicks.
*/
  $('#winLossRow').text('You win! Congratulations!');
  $('.mine').each(function() {
    $(this).html('<img src="/img/glyphicons_266_flag.png" />');
  });
  $("#mineSweeperGame").addClass('gameOver');
}
function endGameLose(){
/**
* endGameLose shows all the mines in the game, alerts the user to their loss, and adds the
* gameOver class to the table to prevent further clicks.
*/
  $('#winLossRow').text('You lose!');
  $('.mine').each(function() {
    $(this).html('<img src="/img/glyphicons_021_snowflake.png" />');
    $(this).css("border","1px solid");
    $(this).css("border-color","#777");
    $(this).css("height","38px");
    $(this).css("width","38px");
    if ($(this).css("background-color") == 'rgb(187, 187, 187)'){
      $(this).css("background-color","#aaa");
    }
  });
  $("#mineSweeperGame").addClass('gameOver');
}
function validateGame(){
/**
* validateGame checks to see if the game is won and then calls the function to end the game.
*/
  var gameWon = isGameWon();
  if (gameWon){
    endGameWin();
  } else {
    endGameLose();
  }
}
function saveGame(){
/**
* minesweeperGames is a localStorage item that is an array of arrays, encoded into JSON
* each saved game consists of the epoch time in milliseconds at index 0
* and the html of the #mineSweeperGame table at index 1
* saveGame gets mineSweeperGames from localStorage, parses it into an array, creates a new
* saved game, pushes it into the array, sets the localStorage item, and refreshes the list
* of saved games
*/
  if (localStorage.getItem('minesweeperGames')){
    var games = JSON.parse(localStorage.getItem('minesweeperGames'));
  } else {
    var games = [];
  }
  var newGame = [new Date().getTime(), $("#mineSweeperGame").html()];
  games.push(newGame);
  localStorage.setItem('minesweeperGames', JSON.stringify(games));
  displaySavedGames();
}
function displaySavedGames(){
/**
* minesweeperGames is a localStorage item that is an array of arrays, encoded into JSON
* each saved game consists of the epoch time in milliseconds at index 0
* and the html of the #mineSweeperGame table at index 1
* displaySavedGames gets the games from storage and makes links to load and delete each game.
*/
  if (localStorage.getItem('minesweeperGames')){
    $("#savedGames").html('');
    var games = JSON.parse(localStorage.getItem('minesweeperGames'));
    for (i in games){
      var dt = new Date(games[i][0]);
      var timeString = pad2(dt.getMonth() + 1) + '/' + pad2(dt.getDate()) + '/' + pad2(dt.getFullYear()) + ' ' + pad2(dt.getHours()) + ':' + pad2(dt.getMinutes());
      var loadLink = '<a href="#" onclick="loadGame(\'' + games[i][0] + '\')">' + timeString + '</a>';
      var deleteLink = '<a href="#" onclick="deleteGame(\'' + games[i][0] + '\')">delete</a>';
      $("#savedGames").append('<div class="savedGame">' + loadLink + ' (' + deleteLink +')</div>');
    }
  }
}
function loadGame(time){
/**
* minesweeperGames is a localStorage item that is an array of arrays, encoded into JSON
* each saved game consists of the epoch time in milliseconds at index 0
* and the html of the #mineSweeperGame table at index 1
* loadGame takes the epoch time as a parameter, searches through the saved games for the matching
* item and then replaces the #mineSweeperGame table with the contents from the saved game.
*/
  var games = JSON.parse(localStorage.getItem('minesweeperGames'));
  for (i in games){
    if (games[i][0] == time){
      $("#mineSweeperGame").html(games[i][1]);
      $("#mineSweeperGame").removeClass('gameOver');
      $('#winLossRow').text("Minesweeper in Javascript");
      makeClickable();
    }
  }
}
function deleteGame(time){
/**
* minesweeperGames is a localStorage item that is an array of arrays, encoded into JSON
* each saved game consists of the epoch time in milliseconds at index 0
* and the html of the #mineSweeperGame table at index 1
* deleteGame takes the epoch time as a parameter, loops through the saved games for everything
* except the matching item and then replaces the localStorage with the new array.
*/
  var games = JSON.parse(localStorage.getItem('minesweeperGames'));
  var editedGames = []
  for (i in games){
    if (games[i][0] != time){
      editedGames.push(games[i]);
    }
  }
  localStorage.setItem('minesweeperGames', JSON.stringify(editedGames));
  displaySavedGames();
}
function makeMineSweeper(){
/**
* makeMineSweeper checks the selected values for gridSize and numMines, resets the #winLossRow
* message and the 'gameOver' class, and then calls makeGame
*/
  var gridSize = $('#gridSize').val();
  var numMines = $('#numMines').val();
  $("#mineSweeperGame").removeClass('gameOver');
  $('#winLossRow').text("Minesweeper in Javascript");
  makeGame(gridSize,numMines);
}
$(document).ready(function() {
/**
* when the document is ready, we make the link the buttons to their functions and create the game.
*/
  $('#newGame').click(function(){
    makeMineSweeper();
  });
  $('#cheat').click(function(){
    cheatGame();
  });
  $('#validate').click(function(){
    validateGame();
  });
  $('#saveGame').click(function(){
    saveGame();
  });
  makeMineSweeper();
  displaySavedGames();
});
