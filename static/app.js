class BoggleGame {

  constructor(boardId, time = 60) {
    this.time = time;
    this.setTimer();

    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);

    this.timer = setInterval(this.tick.bind(this), 1000);
    $(".word-submission", this.board).on("submit", this.submit.bind(this));
  }

  makeWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }

  setScore() {
    $(".score", this.board).text(this.score);
  }

  makeMessage(msg, cls) {
    $(".msg", this.board)
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`)
  }

  setTimer() {
    $(".time", this.board).text(this.time);
  }

  async submit(evt) {
    evt.preventDefault();
    const $word = $(".word", this.board);

    let word = $word.val();
    if (!word) return;

    if (this.words.has(word)) {
      this.makeMessage(`You have already found ${word}`, "err");
      return;
    }

    const res = await axios.get("/check", { params: { word: word }});
    if (res.data.result === "not-word") {
      this.makeMessage(`${word} is not a valid word`, "err");
    } else if (res.data.result === "not-on-board") {
      this.makeMessage(`${word} that word is not found on this board`, "err");
    } else {
      this.score += word.length;
      this.setScore();
      this.makeWord(word);
      this.words.add(word);
      this.makeMessage(`You guessed ${word} correctly`, "ok");
    }

    $word.val("").focus();
  }

  async tick() {
    this.time -= 1;
    this.setTimer();

    if (this.time === 0) {
      clearInterval(this.timer);
      await this.gameScore();
    }
  }

  async gameScore() {
    $(".word-submission", this.board).hide();
    const res = await axios.post("/submit-score", { score: this.score });
    if (res.data.brokeRecord) {
      this.makeMessage(`New record: ${this.score}`, "ok");
    } else {
      this.makeMessage(`Final score: ${this.score}`);
    }
  }
}