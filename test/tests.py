import unittest


def get_script_name(project_name: str) -> str:
    g = (i for i in project_name)
    shift = 0
    for i in range(len(project_name)):
        char = next(g)

        if char.isupper() and i > 0:
            start_ = project_name[:i + shift]
            end_ = project_name[i + shift:]

            project_name = start_ + '-' + end_
            shift += 1

    return project_name.lower()


def is_project_name_camelcase(project_name: str) -> bool:

    if project_name[0].islower():
        return False

    if project_name.islower():
        return False

    for i in ['-', '_']:
        if i in project_name:
            return False
    return True


class MyTestCase(unittest.TestCase):
    def test_get_script_name(self):
        self.assertEqual(get_script_name('ImageCrypt'), 'image-crypt')
        self.assertEqual(get_script_name('Imagecrypt'), 'imagecrypt')
        self.assertEqual(get_script_name('ImageCrypt'), 'image-crypt')
        self.assertEqual(get_script_name('imagecrypt'), 'imagecrypt')
        self.assertEqual(get_script_name('imagecryptT'), 'imagecrypt-t')
        self.assertEqual(get_script_name('ImageCryptTEST'), 'image-crypt-t-e-s-t')

        self.assertEqual(get_script_name('ImageCryptSave'), 'image-crypt-save')
        self.assertEqual(get_script_name('ImageCryptSave'), 'image-crypt-save')
        self.assertEqual(get_script_name('ImageCryptSave'), 'image-crypt-save')

        self.assertEqual(get_script_name('ImageCryptSaveSegaMegaDriveUltraSuper'),
                         'image-crypt-save-sega-mega-drive-ultra-super')

    def test_is_project_name_camelcase(self):
        self.assertEqual(is_project_name_camelcase('ImageCrypt'), True)
        self.assertEqual(is_project_name_camelcase('Imagecrypt'), True)

        self.assertEqual(is_project_name_camelcase('image-crypt'), False)
        self.assertEqual(is_project_name_camelcase('image_crypt'), False)
        self.assertEqual(is_project_name_camelcase('image_Crypt'), False)
        self.assertEqual(is_project_name_camelcase('imageCrypt'), False)


if __name__ == '__main__':
    unittest.main()
