from dataclasses import dataclass


@dataclass
class MethodPatcher:
    odoo_class: object
    name_method: str
    callable_method: callable
