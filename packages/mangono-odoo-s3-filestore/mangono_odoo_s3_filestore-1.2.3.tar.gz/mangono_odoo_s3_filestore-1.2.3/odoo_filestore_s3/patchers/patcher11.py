import logging
from typing import BinaryIO, Union

import odoo

from ..adapter import OdooIrAttachmentModel, StorageAdapter
from .method_patcher import MethodPatcher

_logger = logging.getLogger("odoo_filestore_s3")


@odoo.api.model
def _file_read(self: OdooIrAttachmentModel, fname: str, bin_size: bool = False) -> Union[BinaryIO, str, int]:
    return StorageAdapter.file_read(self, fname, bin_size=bin_size, use_base64=True)


@odoo.api.model
def _file_write(self: OdooIrAttachmentModel, value: bytes, checksum: str) -> str:
    return StorageAdapter.file_write(self, content=value, checksum=checksum, use_base64=True)


@odoo.api.model
def _storage(self: OdooIrAttachmentModel) -> str:
    return self.env.context.get("force_attachment_storage") or "s3"


@odoo.api.model
def _mark_for_gc(self: OdooIrAttachmentModel, fname: str):
    return StorageAdapter.mark_for_gc(self, fname)


@odoo.api.model
def _file_gc(self: OdooIrAttachmentModel):
    return StorageAdapter._file_gc(self)


if int(odoo.release.version_info[0]) == 11:
    IrAttachment = odoo.addons.base.ir.ir_attachment.IrAttachment
else:
    IrAttachment = odoo.addons.base.models.ir_attachment.IrAttachment

PATCHED_METHOD = [
    MethodPatcher(IrAttachment, "_file_read", _file_read),
    MethodPatcher(IrAttachment, "_file_write", _file_write),
    MethodPatcher(IrAttachment, "_storage", _storage),
    MethodPatcher(IrAttachment, "_mark_for_gc", _mark_for_gc),
    MethodPatcher(IrAttachment, "_file_gc", _file_gc),
]
