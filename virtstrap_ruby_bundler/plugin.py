from __future__ import with_statement
import os
from contextlib import contextmanager
from virtstrap import hooks
from virtstrap.log import logger
from virtstrap.utils import call_subprocess

# FIXME this should be somewhere else. for now we'll just copy
# this from virtstrap.testing
class ChangedWorkingDirectory(object):
    def __init__(self, directory):
        self._directory = directory
        self._original_directory = os.getcwd()

    def __enter__(self):
        # Change the directory to the new cwd
        directory = self._directory
        # Change to the new directory
        os.chdir(directory)
        # Return the directory
        return directory

    def __exit__(self, ex_type, ex_value, traceback):
        # Return back to normal
        os.chdir(self._original_directory)

@contextmanager
def in_directory(directory):
    """Context manager for changing CWD to a directory

    Don't use this if you plan on writing files to the directory.
    This does not delete anything. It is purely to change the CWD
    """
    with ChangedWorkingDirectory(directory) as directory:
        yield directory


@hooks.create('install', ['after'])
def install_ruby_bundler_requirements(event, options, project=None, **kwargs):
    with in_directory(project.path()): # ensure we're in the project's directory
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
