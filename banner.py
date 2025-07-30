import random


class Banner:
    """A class simulating a basic banner in Arknights.

    A basic banner has a basic six-star rate of 2%, and a pity-rule where:
     - If a six-star character does not appear in 50 continuous pulls, beginning
     from the 51th pull, the rate of six-star increase by 2% each pull. (i.e.
     51th: 4%, 52th: 6%, etc.)
     - Once gained a six-star character, the rate returns to 2%.

    Attributes:
     - pulls: current number of pulls used.
     - records: a list of integers containing the # of pulls of each six-star.
    """

    pulls: int
    records: list[int]

    def __init__(self) -> None:
        self.pulls = 0
        self.records = []

    def reset(self) -> None:
        """Reset the Banner to default state."""
        self.pulls = 0
        self.records = []

    def _is_6star(self) -> bool:
        """Return True if this pull obtained a six-star character."""
        pulls_since_last_6star = self.pulls - (self.records[-1] if self.records else 0)

        if pulls_since_last_6star <= 50:
            prob_6star = 0.02
        else:
            prob_6star = 0.02 + 0.02 * (pulls_since_last_6star - 50)

        return random.random() < prob_6star

    def pull_once(self) -> bool:
        """Make a pull!

        Return True if the resulting character is a 6-star, and append the current
        number of pulls to self.records.
        """
        self.pulls += 1
        # If got a six-star:
        if self._is_6star():
            self.records.append(self.pulls)
            return True

        # Didn't get a six-star
        return False

    def pull_n_times(self, n: int) -> list:
        """Make n pulls!

        Return the result of pulls in a list[bool]."""
        for _ in range(n):
            self.pull_once()
        return self.records

    def pull_n_desired(self, n: int) -> list:
        """Make a number of pulls to get n desired characters.

        In this case, pull n six-stars."""
        while len(self.records) < n:
            self.pull_once()
        return self.records

if __name__ == '__main__':
    random.seed(123)
    b = Banner()
    for i in range(20):
        print(f"第{i + 1}抽出现六星：", b.pull_once())
    print(b.records)
    b.reset()

    n = 3
    b.pull_n_desired(n)
    print(f"{n}个六星出现的抽数：")
    print(b.records)
