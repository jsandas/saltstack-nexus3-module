"""Namespace package for Salt extensions."""

from pkgutil import extend_path

# Enable pkgutil-style namespace package so multiple distributions
# can provide `saltext.*` subpackages in the same environment.
__path__ = extend_path(__path__, __name__)
