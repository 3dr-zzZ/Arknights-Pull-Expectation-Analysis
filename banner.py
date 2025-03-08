import random

class Banner:
    """A class simulating a basic banner in Arknights.

    A basic banner has a basic six-star rate of 2%, and a pity-rule where:
     - If a six-star character does not appear in 50 continuous pulls, beginning
     from the 51th pull, the rate of six-star increase by 2% each pull. (i.e. 
     51th: 4%, 52th: 6%, etc.)
     - Once gained a six-star character, the rate returns to 2%.
    
    Attributes:
     - prob_6star: the probability of getting a six-star of the next pull.
     - pity_counter_basic: pity counter for the basic pity rule.
     - pulls: current number of pulls used.
     - records: a list of integers containing the # of pulls of each six-star.
    """
    
    prob_desired: float
    pulls: int
    records: list

    def __init__(self) -> None:
        self.pulls = 0
        self.records = []

    def reset(self) -> None:
        """Reset the Banner to default state."""
        self.pulls = 0
        self.records = []

    def _is_6star(self) -> bool:
        """Return True if this pull obtained a six-star character."""
        if self.records:
            pulls_since_last_6star = self.pulls - self.records[-1]
        else:
            pulls_since_last_6star = self.pulls
        
        if pulls_since_last_6star <= 50:
            prob_6star = 0.02
        else:
            prob_6star = 0.02 + 0.02 * (pulls_since_last_6star - 50)
        
        return random.random() < prob_6star

        
    def pull_once(self) -> bool:
        """Make a pull!
        
        >>> banner = Banner()
        >>> banner.pull_once()
        False
        >>> banner.pull_once()
        True
        """
        self.pulls += 1
        # If got a six-star:
        if self._is_6star():
            self.records.append(self.pulls)
            return True
        
        # Didn't get a six-star
        return False
        
    def pull_times(self, n: int) -> list:
        """Make n pulls!"""
        for _ in range(n):
            self.pull_once()
        return self.records
    
    def pull_desired(self, n: int) -> list:
        """Make pulls to get n desired characters!"""
        while len(self.records) < n:
            self.pull_once()
        return self.records

    def convert_gap_records(self) -> list:
        """Output records based on the pulls used between the occurance of each
        six-star gained.
        """
        if not self.records:
            return []
        
        cur_pull = 0
        records_gap = []
        for pull_cnt in self.records:
            records_gap.append(pull_cnt - cur_pull)
            cur_pull = pull_cnt
        return records_gap

if __name__ == '__main__':
    random.seed(100)
    b = Banner()
    for _ in range(5):
        b.pull_desired(6)
        print(b.convert_gap_records())
        b.reset()
