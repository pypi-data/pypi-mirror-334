import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path for importing from the package
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from patchcommander.api import (
    find_class, find_method, find_function, get_file_content,
    list_classes, list_methods, list_functions, get_imports_section
)

class TestApiModules(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test_file.py')
        
        # Create a test file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("""import os
import sys
from typing import List, Dict, Optional

class TestClass:
    \"\"\"Test class docstring.\"\"\"
    
    def __init__(self, name: str):
        self.name = name
        
    def method1(self) -> str:
        return f"Hello, {self.name}"
        
    def method2(self, value: int) -> int:
        return value * 2

def standalone_function(param: str) -> str:
    \"\"\"Test function docstring.\"\"\"
    return f"Function received: {param}"

class AnotherClass:
    def another_method(self):
        pass
""")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_get_file_content(self):
        content = get_file_content(self.test_file)
        self.assertIn('class TestClass', content)
        self.assertIn('def standalone_function', content)
        
    def test_find_class(self):
        result = find_class(self.test_file, 'TestClass')
        self.assertIsNotNone(result)
        start_line, end_line, content = result
        self.assertGreater(start_line, 0)
        self.assertGreater(end_line, start_line)
        self.assertIn('Test class docstring', content)
        self.assertIn('def method1', content)
        
    def test_find_method(self):
        result = find_method(self.test_file, 'TestClass', 'method1')
        self.assertIsNotNone(result)
        start_line, end_line, content = result
        self.assertGreater(start_line, 0)
        self.assertGreater(end_line, start_line)
        self.assertIn('def method1', content)
        self.assertIn('return f"Hello', content)
        
    def test_find_function(self):
        result = find_function(self.test_file, 'standalone_function')
        self.assertIsNotNone(result)
        start_line, end_line, content = result
        self.assertGreater(start_line, 0)
        self.assertGreater(end_line, start_line)
        self.assertIn('def standalone_function', content)
        self.assertIn('Test function docstring', content)
        
    def test_list_classes(self):
        classes = list_classes(self.test_file)
        self.assertEqual(len(classes), 2)
        class_names = [cls.name for cls in classes]
        self.assertIn('TestClass', class_names)
        self.assertIn('AnotherClass', class_names)
        
    def test_list_methods(self):
        methods = list_methods(self.test_file, 'TestClass')
        self.assertEqual(len(methods), 3)  # __init__, method1, method2
        method_names = [m.name for m in methods]
        self.assertIn('__init__', method_names)
        self.assertIn('method1', method_names)
        self.assertIn('method2', method_names)
        
    def test_list_functions(self):
        functions = list_functions(self.test_file)
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0].name, 'standalone_function')
        
    def test_get_imports_section(self):
        result = get_imports_section(self.test_file)
        self.assertIsNotNone(result)
        start_line, end_line, content = result
        self.assertEqual(start_line, 1)
        self.assertGreaterEqual(end_line, 3)
        self.assertIn('import os', content)
        self.assertIn('from typing import', content)

if __name__ == '__main__':
    unittest.main()