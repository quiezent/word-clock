import unittest
import word_clock

class DummyDot:
    def configure(self, **kwargs):
        pass

class TestUpdateClockSpecifiedTime(unittest.TestCase):
    def test_handles_24_hour_input(self):
        wc = word_clock.WordClock.__new__(word_clock.WordClock)
        wc.specified_time = '13:15'
        wc.letters = []
        wc.dots = [DummyDot() for _ in range(4)]
        wc.reset_labels = lambda: None
        wc.highlight_word = lambda word: None
        # Bind method from class
        wc.get_time_representation = word_clock.WordClock.get_time_representation.__get__(wc)
        try:
            word_clock.WordClock.update_clock(wc)
        except KeyError:
            self.fail('update_clock raised KeyError for 24-hour time input')

if __name__ == '__main__':
    unittest.main()
