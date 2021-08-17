import unittest


def get_script_name(project_name: str) -> str:
    project_name = project_name.strip()
    g = (i for i in project_name)
    shift = 0
    flag = False
    for i in range(len(project_name)):
        char = next(g)

        if char.isupper():
            start_ = project_name[:i + shift]
            end_ = project_name[i + shift:]
            try:
                if end_[1].isupper():
                    if not flag:
                        flag = True
                    else:
                        continue
                else:
                    flag = False
            except IndexError:
                continue
            project_name = start_ + '-' + end_
            shift += 1

    return project_name.lower().strip('-').strip()


def is_camel_case(string):
    return string != string.lower() and string != string.upper() and "_" not in string and "-" not in string


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
        self.assertEqual(get_script_name('ImageCryptSave'), 'image-crypt-save')

        self.assertEqual(get_script_name('ImageCryptSaveSegaMegaDriveUltraSuper'),
                         'image-crypt-save-sega-mega-drive-ultra-super')

    def test_is_project_name_camelcase(self):
        self.assertTrue(is_camel_case('camelCase'))
        self.assertTrue(is_camel_case('CamelCase'))
        self.assertTrue(is_camel_case('Camelcase'))
        self.assertTrue(is_camel_case('Case'))

        self.assertFalse(is_camel_case('camel'))
        self.assertFalse(is_camel_case('CAMELCASE'))
        self.assertFalse(is_camel_case('camelcase'))
        self.assertFalse(is_camel_case('camel_case'))
        self.assertFalse(is_camel_case('camel-Case'))


if __name__ == '__main__':
    unittest.main()
