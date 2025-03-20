import unittest

from result import Result

from pychemstation.analysis.process_report import process_csv_report


class TestReport(unittest.TestCase):

    def test_process_reporttxt(self):
        try:
            # TODO
            print('yes')
        except Exception as e:
            self.fail(f"Should have not failed, {e}")

    def test_report_csv(self):
        try:
            possible_peaks: Result = process_csv_report(folder_path="0_2025-03-15 19-14-35.D", num=1)
            self.assertTrue(len(possible_peaks.ok_value) == 16)
            print('yes')
        except Exception as e:
            self.fail(f"Should have not failed: {e}")


if __name__ == '__main__':
    unittest.main()
