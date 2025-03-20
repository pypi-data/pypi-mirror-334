import unittest
from ssc.links.checker import check_url


class TestLinkChecker(unittest.TestCase):

    def test_check_good_url(self):
        code = check_url('https://www.example.com')
        self.assertIn(code, range(200, 400))

    def test_link_bad(self):
        code = check_url('https://example.com/non-existing-url')
        self.assertEqual(code, 404)


if __name__ == '__main__':
    unittest.main()
