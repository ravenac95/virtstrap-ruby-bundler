from virtstrap import hooks
from virtstrap.log import logger
from virtstrap.utils import call_subprocess
from virtstrap.testing.directory import in_directory

@hooks.create('install', ['after'])
def install_ruby_bundler_requirements(event, options, project=None, **kwargs):
    with in_directory(project.path()): # ensure we're in the project's directory
        try:
            call_subprocess(['command', '-v', 'bundle'], show_stdout=False)
        except OSError:
            logger.warning('Skipping Ruby Requirements. '
                    'Bundler must be installed in your system')
            return
        call_subprocess(['bundle', 'install',
            '--binstubs=%s' % project.bin_path()])
