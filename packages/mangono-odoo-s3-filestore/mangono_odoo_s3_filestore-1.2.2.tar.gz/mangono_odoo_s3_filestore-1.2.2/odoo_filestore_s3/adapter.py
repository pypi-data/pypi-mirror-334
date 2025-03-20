import base64
import os
from typing import BinaryIO, Union

from typing_extensions import Protocol

from odoo.exceptions import UserError

from .odoo_s3_fs import S3Odoo, _logger


class CallableOrigin(Protocol):
    origin: "CallableOrigin"

    def __call__(self, *args, **kwargs): ...


class OdooAutoVacuumModel(Protocol):
    power_on: CallableOrigin


class OdooIrAttachmentModel(Protocol):
    _file_read: CallableOrigin
    _file_write: CallableOrigin

    def _compute_checksum(self, bin_data: BinaryIO) -> str:
        """file:///workspace/python/odoo/v12/odoo12/odoo/addons/models/ir_attachment.py"""


class OdooS3Error(UserError):
    """S3 error class to filter them from UserError when catching them
    Not just S3Error because Minio already has an error class named like this"""


class StorageAdapter:
    @staticmethod
    def odoo_raise_error(msg: str) -> Exception:
        return OdooS3Error(msg)

    @staticmethod
    def _store_in_cache(odoo_inst: OdooIrAttachmentModel, bin_data: bytes):
        if not bin_data:
            return

        checksum = odoo_inst._compute_checksum(bin_data)
        if not checksum:  # Try to cache file locally
            return

        try:
            odoo_inst._file_write.origin(odoo_inst.with_context(s3_no_gc=True), bin_data, checksum=checksum)
        except Exception as e:
            _logger.error("S3: unable to cache %s file locally: %s", checksum, e)

    @staticmethod
    def file_read(
        odoo_inst: OdooIrAttachmentModel, fname: str, bin_size: bool = False, use_base64: bool = False
    ) -> Union[BinaryIO, str, int]:
        s3 = S3Odoo.from_env(odoo_inst.env.cr.dbname)
        res = StorageAdapter._read_in_cache(odoo_inst, fname)

        if res or not s3.conn.enable:
            if bin_size:
                return res and len(res) or 0
            return res

        res = s3.file_read(fname)
        if not res:
            return ""

        if use_base64:
            res = base64.b64encode(res)

        StorageAdapter._store_in_cache(odoo_inst, res)

        if bin_size:
            return len(res)
        return res

    @staticmethod
    def to_http_stream(odoo_inst: OdooIrAttachmentModel):
        if odoo_inst.store_fname:
            StorageAdapter.file_read(odoo_inst, odoo_inst.store_fname)
        return odoo_inst._to_http_stream.origin()

    @staticmethod
    def _read_in_cache(odoo_inst, fname):
        full_path = odoo_inst._full_path(fname)
        if not os.path.exists(full_path):
            return None

        try:
            return odoo_inst._file_read.origin(odoo_inst, fname=fname)
        except FileNotFoundError:
            _logger.info("File %s not found locally", fname)

    @staticmethod
    def file_write(
        odoo_inst: OdooIrAttachmentModel, content: [bytes, str], checksum: str, use_base64: bool = False
    ) -> str:
        # content is passed as `value` in V11, V12, V13 and as `bin_value` in V14, V15
        s3 = S3Odoo.from_env(odoo_inst.env.cr.dbname)
        fname = odoo_inst._file_write.origin(odoo_inst, content, checksum=checksum)
        if not s3.conn.enable:
            return fname

        if use_base64:
            content = base64.b64decode(content)
        try:
            s3.file_write(fname, content)
        except Exception as e:
            raise StorageAdapter.odoo_raise_error(f"_file_write was not able to write ({fname})") from e
        return fname

    @staticmethod
    def mark_for_gc(odoo_inst: OdooIrAttachmentModel, fname):
        odoo_inst._mark_for_gc.origin(odoo_inst, fname)
        if odoo_inst.env.context.get("s3_no_gc"):
            return
        s3 = S3Odoo.from_env(odoo_inst.env.cr.dbname)
        if not s3.conn.enable:
            _logger.debug("S3: _file_delete bypass to filesystem storage")
        try:
            s3.mark_for_gc(fname)
        except Exception as err:
            _logger.error(err.message)
            raise StorageAdapter.odoo_raise_error(f"Can't mark for Gc the file: {fname}") from err

    @staticmethod
    def _gc_file_store(odoo_inst: OdooIrAttachmentModel):
        """
        User in Odoo version between 14 and more
        :param odoo_inst:
        :return:
        """
        odoo_inst._gc_file_store.origin(odoo_inst.with_context(force_attachment_storage="file"))
        # StorageAdapter.remove_files_s3(odoo_inst) # No unlink for now on the S3, we keep every file uploaded

    @staticmethod
    def _file_gc(odoo_inst: OdooIrAttachmentModel):
        """
        User in Odoo version between 11 and 13
        :param odoo_inst:
        :return:
        """
        odoo_inst._file_gc.origin(odoo_inst.with_context(force_attachment_storage="file"))
        # StorageAdapter.remove_files_s3(odoo_inst) # No unlink for now on the S3, we keep every file uploaded

    @staticmethod
    def remove_files_s3(odoo_inst: OdooIrAttachmentModel):
        # Continue in a new transaction. The LOCK statement below must be the
        # first one in the current transaction, otherwise the database snapshot
        # used by it may not contain the most recent changes made to the table
        # ir_attachment! Indeed, if concurrent transactions create attachments,
        # the LOCK statement will wait until those concurrent transactions end.
        # But this transaction will not see the new attachements if it has done
        # other requests before the LOCK (like the method _storage() above).
        # odoo_inst.env.cr.commit()
        # prevent all concurrent updates on ir_attachment while collecting!
        # odoo_inst.env.cr.execute("LOCK ir_attachment IN SHARE MODE")
        # determine which files to keep among the checklist
        s3 = S3Odoo.from_env(odoo_inst.env.cr.dbname)
        checklist = s3.get_checklist_objects()
        whitelist = set()
        for names in odoo_inst.env.cr.split_for_in_conditions(checklist):
            odoo_inst.env.cr.execute("SELECT store_fname FROM ir_attachment WHERE store_fname IN %s", [names])
            whitelist.update(row[0] for row in odoo_inst.env.cr.fetchall())
        removed = s3.file_delete_multi(checklist, whitelist)
        # commit to release the lock
        # odoo_inst.env.cr.commit()
        _logger.info("S3: filestore gc %d checked, %d removed", len(checklist), removed)
