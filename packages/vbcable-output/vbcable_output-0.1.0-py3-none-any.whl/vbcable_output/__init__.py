# vbcable_output/__init__.py

from .vbcable_output import vbcable_output

play = vbcable_output.play
wait = vbcable_output.wait
is_vbcable_installed = vbcable_output.is_vbcable_installed

__version__ = "0.1.0"
__all__ = ['play', 'wait', 'is_vbcable_installed']