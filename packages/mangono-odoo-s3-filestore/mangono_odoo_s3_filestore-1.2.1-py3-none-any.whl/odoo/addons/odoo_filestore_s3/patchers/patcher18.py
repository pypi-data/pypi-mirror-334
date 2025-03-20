import logging

import odoo

from ..adapter import OdooIrAttachmentModel, StorageAdapter
from . import patcher14
from .method_patcher import MethodPatcher

_logger = logging.getLogger("odoo_filestore_s3")


def _to_http_stream(self: OdooIrAttachmentModel):
    return StorageAdapter.to_http_stream(self)


IrAttachment = odoo.addons.base.models.ir_attachment.IrAttachment


PATCHED_METHOD = patcher14.PATCHED_METHOD + [
    MethodPatcher(IrAttachment, "_to_http_stream", _to_http_stream),
]
