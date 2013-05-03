from __future__ import with_statement
import os
from contextlib import contextmanager
from virtstrap import hooks
from virtstrap.log import logger
from virtstrap.utils import call_subprocess, in_directory


# FIXME this needs to be added to virtstrap properly
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


@hooks.create('install', ['after'])
def install_ruby_bundler_requirements(event, options, project=None, **kwargs):
    # ensure we're in the project's root directory
    with in_directory(project.path()):
        # Check that bundler is installed on the system
        bundler_path = which('bundle')
        if not bundler_path:
            logger.warning('Skipping Ruby Requirements. '
                    'Bundler must be installed in your system')
            return
        # Installs the bundle requirements and the bins for each
        # requirement in the project's bin path
        call_subprocess([bundler_path, 'install',
            '--binstubs=%s' % project.bin_path()])
