# pylint: disable=W0703

import logging

import odoo
from odoo import release
from odoo.modules import module

from .odoo_s3_fs import S3Odoo

_logger = logging.getLogger("odoo_filestore_s3")


def can_be_activate(odoo_version):
    try:
        s3 = S3Odoo.connect_from_env()
    except AssertionError:
        _logger.info("Not loaded : No bucket !")
        return False
    if not s3 or not s3.conn.enable or not s3.conn.s3_session:
        _logger.warning("Not loaded : S3 connection is not enabled")
        return False
    s3.create_bucket_if_not_exist()
    if odoo_version < 11:
        _logger.warning("Not loaded : Odoo version [%s] not supported", odoo_version)
        return False
    return True


def _patch_method_odoo(cls, name, method):
    """
    Copy of the odoo 16 models.py#_patch_method
    Monkey-patch a method for all instances of this model. This replaces
        the method called ``name`` by ``method`` in the given class.
        The original method is then accessible via ``method.origin``, and it
        can be restored with :meth:`~._revert_method`.

        Example::

            def do_write(self, values):
                # do stuff, and call the original method
                return do_write.origin(self, values)


            # patch method write of model
            model._patch_method("write", do_write)

            # this will call do_write
            records = model.search([...])
            records.write(...)

            # restore the original method
            model._revert_method("write")
    """
    origin = getattr(cls, name)
    method.origin = origin
    # propagate decorators from origin to method, and apply api decorator
    wrapped = odoo.api.propagate(origin, method)
    wrapped.origin = origin
    setattr(cls, name, wrapped)


def apply_patch(patcher):
    for method_patcher in patcher.PATCHED_METHOD:
        if method_patcher.callable_method and hasattr(method_patcher.odoo_class, method_patcher.name_method):
            _logger.info("Patch %s", method_patcher.name_method)
            if not hasattr(method_patcher.odoo_class, "_patch_method"):
                _patch_method_odoo(
                    method_patcher.odoo_class, method_patcher.name_method, method_patcher.callable_method
                )
            else:
                method_patcher.odoo_class._patch_method(method_patcher.name_method, method_patcher.callable_method)
    _logger.info("Enabled")


def _post_load_module():
    if "odoo_filestore_s3" not in odoo.conf.server_wide_modules:
        _logger.info("No module in server wide modules")
        return False

    _logger.info("import odoo")
    module.load_openerp_module("base")
    # Pour être sur que base soit chargé avant nous (Car chargé depuis un set)
    _logger.info("Base loaded")
    odoo_version = release.version_info[0]
    if can_be_activate(odoo_version):
        patcher = False
        if 11 <= odoo_version <= 13:
            _logger.info("Load patcher 11 to 13")
            from .patchers import patcher11 as patcher
        elif 14 <= odoo_version < 18:
            _logger.info("Load patcher 14 to 17")
            from .patchers import patcher14 as patcher
        elif odoo_version <= 18:
            _logger.info("Load patcher 18 and more")
            from .patchers import patcher18 as patcher
        if not patcher:
            raise ValueError(f"Not patcher Found for odoo version : {odoo_version}")
        apply_patch(patcher)
