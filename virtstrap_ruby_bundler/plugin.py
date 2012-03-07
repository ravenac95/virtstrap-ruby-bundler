from __future__ import with_statement
import os
from contextlib import contextmanager
from virtstrap import hooks
from virtstrap.log import logger
from virtstrap.utils import call_subprocess, in_directory

@hooks.create('install', ['after'])
def install_ruby_bundler_requirements(event, options, project=None, **kwargs):
    # ensure we're in the project's root directory
    with in_directory(project.path()): 
        try:
            call_subprocess(['command', '-v', 'bundle'], show_stdout=False)
        except OSError:
            logger.warning('Skipping Ruby Requirements. '
                    'Bundler must be installed in your system')
            return
        # Installs the bundle requirements and the bins for each 
        # requirement in the project's bin path
        call_subprocess(['bundle', 'install',
            '--binstubs=%s' % project.bin_path()])
