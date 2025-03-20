import odoo

from odoo_env_config.entry import env_to_section
from odoo_env_config.section import S3Section


odoo_version = odoo.release.version_info[0]
s3section = env_to_section(S3Section)
if not s3section.bucket_name:
    from . import test_nopatcher  # noqa
elif 11 <= odoo_version < 14:
    from . import test_patcher11  # noqa
elif 14 <= odoo_version:
    from . import test_patcher14  # noqa
