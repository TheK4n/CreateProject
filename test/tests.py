import unittest
from src.utils import *


class MyTestCase(unittest.TestCase):
    def test_get_script_name(self):
        self.assertEqual(get_script_name('ImageCrypt'), 'image-crypt')
        self.assertEqual(get_script_name('Imagecrypt'), 'imagecrypt')
        self.assertEqual(get_script_name('ImageCrypt'), 'image-crypt')
        self.assertEqual(get_script_name('imagecrypt'), 'imagecrypt')
        self.assertEqual(get_script_name('imagecryptT'), 'imagecryptt')

        self.assertEqual(get_script_name('ImageCryptTEST'), 'image-crypt-test')
        self.assertEqual(get_script_name('ImageCRYPTTest'), 'image-crypt-test')
        self.assertEqual(get_script_name('IMAGECryptTest'), 'image-crypt-test')
        self.assertEqual(get_script_name('IMAGECryptTEST'), 'image-crypt-test')

        self.assertEqual(get_script_name('ImageCryptSave'), 'image-crypt-save')
        self.assertEqual(get_script_name('ImageCryptSave'), 'image-crypt-save')

        self.assertEqual(get_script_name('.ImageCryptSave'), 'image-crypt-save')
        self.assertEqual(get_script_name('ImageCryptSave.'), 'image-crypt-save.')

        self.assertEqual(get_script_name('_camelCase-'), '_camel-case')
        self.assertEqual(get_script_name('-camelCase_'), 'camel-case_')

        self.assertEqual(get_script_name('ImageCryptSaveSegaMegaDriveUltraSuper'),
                         'image-crypt-save-sega-mega-drive-ultra-super')

    def test_is_project_name_camelcase(self):
        self.assertTrue(is_camel_case('camelCase'))
        self.assertTrue(is_camel_case('CamelCase'))
        self.assertTrue(is_camel_case('Camelcase'))
        self.assertTrue(is_camel_case('Case'))

        self.assertTrue(is_camel_case('_camelCase-'))
        self.assertTrue(is_camel_case('-camelCase_'))

        self.assertFalse(is_camel_case('-camelcase_'))
        self.assertFalse(is_camel_case('-CAMELCASE_'))

        self.assertFalse(is_camel_case('camel'))
        self.assertFalse(is_camel_case('CAMELCASE'))
        self.assertFalse(is_camel_case('camelcase'))
        self.assertFalse(is_camel_case('camel_case'))
        self.assertFalse(is_camel_case('camel-Case'))


if __name__ == '__main__':
    unittest.main()
