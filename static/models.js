"use strict";

const BASE_URL = "http://127.0.0.1:5000/";

// Guess: a single guess in the system

class Guess {
  /** Make instance of Guess from guess input value.
   */

  constructor(val) {
    this.val = val;
  }

  // When game-over, disables user's guess input and sends AJAX request to server with the game's score.

  static async updateStats(score) {
    try {
      await axios.post(`${BASE_URL}/game-over`, {score});
    } catch (err) {
      console.error("updateStats failed", err.response.data);
      return null;
    }
  }

  // When user submits a guess, sends AJAX request to server with guess input value.

  static async makeRequest(guess) {
    try {
      const response = await axios.post(`${BASE_URL}/verify`, {guess});
      return response;
    } catch (err) {
      console.error("checkGuess failed", err.response.data);
      return null;
    }
  }
}
