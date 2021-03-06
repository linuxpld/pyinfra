'''
Manage choco (Chocolatey) packages. (see https://chocolatey.org/ )
'''

from pyinfra.api import operation

from .util.packaging import ensure_packages


@operation
def packages(state, host, packages=None, present=True, latest=False):
    '''
    Add/remove/update choco packages.

    + packages: list of packages to ensure
    + present: whether the packages should be installed
    + latest: whether to upgrade packages without a specified version

    Versions:
        Package versions can be pinned like gem: ``<pkg>:<version>``.

    Example:

    .. code:: python

        # Note: Assumes that 'choco' is installed and
        #       user has Administrator permission.
        choco.packages(
            {'Install Notepad++'},
            'notepadplusplus',
        )
    '''

    yield ensure_packages(
        packages, host.fact.choco_packages, present,
        install_command='choco install -y',
        uninstall_command='choco uninstall -y -x',
        upgrade_command='choco update -y',
        version_join=':',
        latest=latest,
    )


@operation
def install(state, host):
    '''
    Install choco (Chocolatey).
    '''

    yield 'Set-ExecutionPolicy Bypass -Scope Process -Force ;' \
        'iex ((New-Object System.Net.WebClient).DownloadString' \
        '("https://chocolatey.org/install.ps1"))'
