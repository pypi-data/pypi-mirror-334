from base64 import b64decode, b64encode

from odoo import release
from odoo.tests import TransactionCase

from odoo.addons.odoo_filestore_s3 import ir_attachment
from odoo.addons.odoo_filestore_s3.odoo_s3_fs import S3Odoo


class OdooFilestoreS3TestPatcher(TransactionCase):
    def setUp(self):
        super().setUp()
        self.attachmentModel = self.env["ir.attachment"]

    # region: Helper method

    # endregion

    # region : Tests methods
    def test_01_params(self):
        self.assertFalse(ir_attachment.can_be_activate(release.version_info[0]))
        with self.assertRaises(AssertionError):
            self.s3 = S3Odoo.from_env(self.env.cr.dbname)

    def test_10_file_write_file_read(self):
        """
        Test file write, and check de file is in the local storage and in the s3 storage
        """
        content = b"My binary content"
        value = b64encode(content)
        fname = self.attachmentModel._file_write(value, "checksum")
        self.assertEqual("ch/checksum", fname)
        local_value = self.attachmentModel._file_read(fname)
        self.assertEqual(local_value, value)
        self.assertEqual(content, b64decode(value))
