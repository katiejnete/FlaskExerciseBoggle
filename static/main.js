"use strict";

const $form = $("form");
const $input = $("input");
const $response = $(".response div");
const $score = $("#current-score");
const $submitBtn = $("button");
const $timeLeft = $("#time-left");

let timer = 60;
$timeLeft.text(timer);

let score = 0;

// When page is ready, starts game and timer.

$(document).ready(function () {
  const intId = setInterval(() => {
    timer -= 1;
    $timeLeft.text(timer);
  }, 1000);
  // Once timer ends, call function to stop game and update stats.
  setTimeout(() => {
    gameOver();
    clearInterval(intId);
  }, 60000);
});

// When game-over, disables user's guess input and calls updateStats.

async function gameOver() {
    $submitBtn.attr("disabled", true);
    await Guess.updateStats(score)
  }

