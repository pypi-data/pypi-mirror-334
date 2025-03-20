import os
from unittest.mock import patch

import odoo
from odoo.tests import TransactionCase

from odoo.addons.odoo_filestore_s3.adapter import StorageAdapter
from odoo.addons.odoo_filestore_s3.odoo_s3_fs import S3Odoo


class OdooFilestoreS3TestPatcher(TransactionCase):
    def setUp(self):
        super().setUp()
        self.attachmentModel = self.env["ir.attachment"]
        self.s3 = S3Odoo.from_env(self.env.cr.dbname)

    # region: Helper method

    def check_has_method(self, inst, method):
        to_call = getattr(inst, method)
        callable(to_call)

    # endregion

    # region : Tests methods
    def test_01_params(self):
        self.assertTrue(
            "odoo_filestore_s3" in odoo.conf.server_wide_modules,
            "'odoo_filestore_s3' should be in load to run this tests",
        )

    def test_10_file_write_file_read(self):
        """
        Test file write, and check de file is in the local storage and in the s3 storage
        """
        value = b"My binary content"
        fname = StorageAdapter.file_write(self.attachmentModel, value, "checksum")
        self.assertEqual("ch/checksum", fname)
        default_value = StorageAdapter.file_read(self.attachmentModel, fname)
        self.assertEqual(default_value, value)
        local_value = self.attachmentModel._file_read.origin(self.attachmentModel, fname)
        self.assertEqual(local_value, value)
        s3_value = self.s3.file_read(fname)
        self.assertEqual(s3_value, value)
        gc_path = f"checklist/{fname}"
        s3_gc_value = self.s3.file_read(gc_path)
        self.assertEqual(s3_gc_value, b"")

    #
    def test_11_mask_for_gc(self):
        bin_value = b"contenu du fichier"
        checksum = self.attachmentModel._compute_checksum(bin_data=bin_value)
        fname = StorageAdapter.file_write(self.attachmentModel, bin_value, checksum)
        StorageAdapter.mark_for_gc(self.attachmentModel, fname=fname)
        res = list(self.s3.conn.s3_session.list_objects(self.s3.bucket.name, recursive=True))
        self.assertTrue(len(res), 1)
        self.assertFalse(res[0].is_dir)
        checklist_fname = f"checklist/{fname}"
        self.assertEqual(checklist_fname, self.s3.bucket.get_key("checklist", fname))
        obj = self.s3.conn.s3_session.get_object(
            self.s3.bucket.name,
            self.s3.bucket.get_key("checklist", fname),
        )
        # Size should be 0 byte
        self.assertEqual(len(obj.data), 0)
        local_value = self.attachmentModel._file_read.origin(self.attachmentModel, checklist_fname)
        self.assertEqual(len(local_value), 0)
        # StorageAdapter._gc_file_store(self.attachmentModel)
        # full_path = self.attachmentModel._full_path(fname)
        # self.assertFalse(os.path.exists(full_path))
        # self.assertRaises(FileNotFoundError, self.s3.file_read(fname))

    def test_12_orm_attachment(self):
        file_data = b"R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs="
        attachment = self.attachmentModel.create(
            {
                "datas": file_data,
                "name": "testEtag.gif",
                "mimetype": "image/gif",
            }
        )
        store_fname = attachment.store_fname
        full_path = self.attachmentModel._full_path(store_fname)
        self.assertTrue(os.path.exists(full_path))
        res = StorageAdapter.file_read(self.attachmentModel, store_fname)
        self.assertEqual(attachment.raw, res)
        res_local = self.attachmentModel._file_read.origin(self.attachmentModel, store_fname)
        self.assertEqual(attachment.raw, res_local)
        res_s3 = self.s3.file_read(store_fname)
        self.assertEqual(attachment.raw, res_s3)
        attachment.unlink()
        checklist_fname = f"checklist/{store_fname}"
        full_path = self.attachmentModel._full_path(checklist_fname)
        self.assertTrue(os.path.exists(full_path))
        self.assertEqual(checklist_fname, self.s3.bucket.get_key("checklist", store_fname))
        obj = self.s3.conn.s3_session.get_object(
            self.s3.bucket.name,
            self.s3.bucket.get_key("checklist", store_fname),
        )
        # Size should be 0 byte
        self.assertEqual(len(obj.data), 0)
        # StorageAdapter._gc_file_store(self.attachmentModel)
        # full_path = self.attachmentModel._full_path(store_fname)
        # self.assertFalse(os.path.exists(full_path))
        # self.assertRaises(FileNotFoundError, self.s3.file_read(store_fname))

    def test_13_record_field_attachment(self):
        """Test store in cache, no add to gc"""
        partner_demo = self.env.ref("base.partner_demo")
        attach = self.env["ir.attachment"].search(
            [("res_id", "=", partner_demo.id), ("res_field", "=", "image_1920"), ("res_model", "=", "res.partner")],
            limit=1,
        )
        attach_path_local = attach._full_path(attach.store_fname)
        if os.path.exists(attach_path_local):
            os.remove(attach_path_local)
        with patch.object(S3Odoo, "file_write") as mock:
            self.env["res.partner"].search_read([("id", "=", partner_demo.id)], fields=["id", "name", "image_1920"])
            assert not mock.called
