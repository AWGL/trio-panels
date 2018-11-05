import unittest
from apply_panel_trios import *
from query_panelapp import *
import csv

"""
Run with python -m test.tests in root project directory.

"""

class TestQueryPanelApp(unittest.TestCase):
	"""
	Tests the query_panelapp script actually works.

	"""

	def test_get_panel(self):
		"""
		Tests whether we can get a panel from panel app successfully.

		"""

		panel_df, panel_data = get_panel('90')

		self.assertEqual(panel_data['SpecificDiseaseName'][0], 'Brain channelopathy' )



class TestApplyStandard(unittest.TestCase):

	"""
	unit test for the apply_panel_trios script with normal variants e.g.
	ones that don't overlap bed boundaries. 

	"""
	def setUp(self):

		report_input = 'test/test_data/test_variant_reports/FAM001_sample1_VariantReport.txt'
		panel_input = ['test/test_data/test_panels/Intellectual_disability_v2.510_green_pad20.bed']

		(report_input, panel_input, bedtools_input, report_path, 
		panel_name) = load_variables(report_input, panel_input)

		make_report_bed(report_input, report_path)

		results_intersect_unique = intersect(report_path, bedtools_input)

		apply_panel(report_input, panel_name, results_intersect_unique)
		filter_denovo(report_input)


	def test_apply_panel_standard(self):
		"""
		Tests whether it successfully filters based on a standard variant report
		"""
		# we should only have one variant in the file.
		expected_variants = ['12:109915190C>T', '1:114437355C>T']

		with open('test/test_data/test_variant_reports/FAM001_sample1_VariantReport_Intellectual_disability_v2.510_green_pad20.txt', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')
			i = 0
			for row in spamreader:

				if row[0][0][0] != '#':

					self.assertEqual(row[2], expected_variants[i])

					i =i +1

	def test_denovo_standard(self):

		expected_variants = ['12:109915190C>T', '6:56492027G>A', '6:56492027G>A', '6:56492027G>A', '6:56492027G>A']

		with open('test/test_data/test_variant_reports/FAM001_sample1_VariantReport_DE_NOVO.txt', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')
			i = 0
			for row in spamreader:

				if row[0][0][0] != '#':

					self.assertEqual(row[2], expected_variants[i])

					i =i +1

	def tearDown(self):

		os.remove('test/test_data/test_variant_reports/FAM001_sample1_VariantReport_Intellectual_disability_v2.510_green_pad20.txt')
		os.remove('test/test_data/test_variant_reports/FAM001_sample1_VariantReport_DE_NOVO.txt')


class TestApplyVariantEdge(unittest.TestCase):

	"""
	unit tests for deletions near the edge of a region -for example

	1:4AAAAAAAAA>A with bed chr1 6 10

	may be missed as postion 4 lies outside of the region although the variant does go inside it.

	"""
	def setUp(self):

		report_input = 'test/test_data/test_variant_reports/indel_at_edge_report.txt'
		panel_input = ['test/test_data/test_panels/indel_at_edge.bed']

		(report_input, panel_input, bedtools_input, report_path, 
		panel_name) = load_variables(report_input, panel_input)

		make_report_bed(report_input, report_path)

		results_intersect_unique = intersect(report_path, bedtools_input)

		apply_panel(report_input, panel_name, results_intersect_unique)
		filter_denovo(report_input)


	def test_apply_panel_edge(self):
		"""
		Tests whether it successfully filters based on a standard variant report
		"""
		# we should only have one variant in the file.
		expected_variants = ['6:56492023TTTTTTTT>AAAAAAAA', '6:56492025AAAAAAA>GGGGGGGGGG', '6:56492025AAA>GGGGGGGGGGGGGGGG']

		with open('test/test_data/test_variant_reports/indel_at_edge_report_indel_at_edg.txt', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')
			i = 0
			for row in spamreader:

				if row[0][0][0] != '#':

					self.assertEqual(row[2], expected_variants[i])

					i =i +1

	def test_de_novo_edge(self):

		expected_variants = ['6:56492025A>GGGGGGGGGGGGGGGG']

		with open('test/test_data/test_variant_reports/indel_at_edge_report_DE_NOVO.txt', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')
			i = 0
			for row in spamreader:

				if row[0][0][0] != '#':

					self.assertEqual(row[2], expected_variants[i])

					i =i +1

	def tearDown(self):

		os.remove('test/test_data/test_variant_reports/indel_at_edge_report_indel_at_edg.txt')
		os.remove('test/test_data/test_variant_reports/indel_at_edge_report_DE_NOVO.txt')


if __name__ == '__main__':
    unittest.main()



