import unittest
import jagss


class TestJagss(unittest.TestCase):
    def test_good_md(self):
        filePath = 'jagss/tests/good_md.md'
        good_dict = {'url': '/tests/good_md.html',
                     'relativePath': '/tests',
                     'html': """<h1>This is an h1</h1>

<h2>This is an h2</h2>

<p>this is <a href="\'https://rpy.xyz\'">a link</a>.</p>

<p>This is a second paragraph.</p>
""",
                     'type': 'markdown'}
        test_dict = jagss.dictFromMarkdown(filePath, '/tests')
        self.assertEqual(good_dict, test_dict)

    def test_good_yaml_md(self):
        filePath = 'jagss/tests/good_yaml_md.md'
        good_dict = {'title': 'Test File',
                     'url': '/tests/good_yaml_md.html',
                     'relativePath': '/tests',
                     'html': """<h1>This is a test file!</h1>

<p>This exists to test the base functionality of Jagss.</p>
""",
                     'template': 'base.html',
                     'type': 'yaml+markdown'}
        test_dict = jagss.dictFromMarkdown(filePath, '/tests')
        self.assertEqual(good_dict, test_dict)

    def test_good_yaml(self):
        filePath = 'jagss/tests/good_yaml.yaml'
        good_dict = {'url': '/tests/good_yaml.html',
                     'relativePath': '/tests',
                     'type': 'yaml',
                     'template': 'default.html',
                     'title': 'Test Yaml Data',
                     'key1': 'value 1'}
        test_dict = jagss.dictFromYaml(filePath, '/tests')
        self.assertEqual(good_dict, test_dict)
