import unittest
import main


class MainTestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main.main(), None)


if __name__ == "__main__":
    unittest.main()
