"use strict";

// Updates score if word is ok.

async function updateScore(input, result) {
    if (result === "ok") {
      score += input.length;
      $score.text(score);
    }
  }

// When guess submits, no page refresh, calls makeRequest to get result, and calls updateScore.

async function submitGuess(e) {
  e.preventDefault();
  const inputVal = $input.val();
  const response = await Guess.makeRequest(inputVal);
  const result = response.data.result;
  $response.text(result);
  updateScore(inputVal, result);

  $form.trigger("reset");
}

$form.on("submit", submitGuess);
