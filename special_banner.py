import random
from banner import Banner, export_to_csv

class SpecialBanner(Banner):
    """A class for the Special Banner.

    Special Banner:
    - This banner features one rate-up six-star character.
    - When a six-star is pulled, there is a 50% chance it will be the rate-up.
    - Pity rule: If the rate-up character is not obtained in 150 consecutive pulls,
    the next six-star is guaranteed to be the rate-up character. This rule only
    apply once.

    Attributes:
    - records_rate_up: A list of integers indicating the pull numbers where
    the rate-up character was obtained.
    - pity_used: An indicator of whether the pity rule was already used. True if
    the rule is used, False if the rule is still available.
    """

    records_rate_up: list[int]
    pity_used: bool

    def __init__(self) -> None:
        super().__init__()
        self.records_rate_up = []
        self.pity_used = False

    def reset(self) -> None:
        super().reset()
        self.records_rate_up = []
        self.pity_used = False

    def pull_once(self) -> bool:
        """Make one pull.

        Return True if results in a six-star."""
        is_6star = super().pull_once()
        if is_6star:
            pulls_since_last_rate_up = self.pulls - (self.records_rate_up[-1] if self.records_rate_up else 0)
            guaranteed_rate_up = pulls_since_last_rate_up >= 150 and not self.pity_used

            if guaranteed_rate_up or random.random() < 0.5:
                self.records_rate_up.append(self.pulls)
                if guaranteed_rate_up:
                    self.pity_used = True

        return is_6star

    def pull_n_desired(self, n) -> list:
        """Make a number of pulls to get n rate-up characters."""
        while len(self.records_rate_up) < n:
            self.pull_once()
        return self.records_rate_up

if __name__ == "__main__":
    random.seed(123)
    b = SpecialBanner()
    n_sample = 10000  # number of samples
    n_rate_up = 6  # the number of rate-up characters from each sample.

    results = []
    for _ in range(n_sample):
        results.append(max(b.pull_n_desired(n_rate_up)))
        b.reset()
    print(results)

    export_to_csv(results, "Special Banner: 6 desired")
