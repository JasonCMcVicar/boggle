"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  // loop over board and create the DOM tr/td structure
  $tableRow = $("tr");
  $tableData = $("td");

  for (let i = 0; i < board.length; i++) {
    $table.append($tableRow).attr("id", i)
    for (let j = 0; j < board[i].length; j++) {

    }
  }
}


start();
