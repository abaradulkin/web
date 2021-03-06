# _*_ coding: utf-8 _*_

__copyright__ = 'Copyright 2012 maizy.ru'
__author__ = 'Nikita Kovaliov <nikita@maizy.ru>'
__license__ = 'MIT'
__doc__ = 'init or update python venv (python 3.3+)'

import os.path as path
import subprocess
import sys
import urllib.error
import urllib.request
import venv


def download_file_if_not_exist(res_path, url):
    """Download file if not exist and put it to provisions_path"""
    if not path.exists(res_path):
        try:
            res = urllib.request.urlopen(url)
            output = open(res_path, 'wb')
            output.write(res.read())
            output.close()
        except (urllib.error.URLError, OSError):
            return False
    return True


class BuilderUtilsMixin(object):

    def run_in_venv(self, context, command, args=None, shell=False):
        """Run command in venv (emulate PATH=env_dir:PATH behavior)"""
        print(command, args)
        venv_command_path = path.join(context.bin_path, command)
        call_args = [venv_command_path]
        if args is not None:
            call_args.extend(args)
        try:
            return subprocess.call(call_args, shell=shell) == 0
        except (subprocess.SubprocessError, OSError) as err:
            print(err)
            return False

    def install_pip_requirements(self, context, requirements_path):
        self.run_in_venv(context, 'pip', ['install', '-r', requirements_path])


class ImprovedEnvBuilder(venv.EnvBuilder, BuilderUtilsMixin):
    """Improved EnvBuilder
    Additional hooks:
     - post_upgrade(context)
    """

    def create(self, env_dir, command):
        """Overwrite create method (add more hooks)"""
        env_dir = path.abspath(env_dir)
        context = self.ensure_directories(env_dir)
        self.create_configuration(context)
        subprocess.call(['python', '-m', 'venv', env_dir])
        #self.setup_python(context)
        if not self.upgrade:
            self.setup_scripts(context)
            self.post_setup(context)
        else:
            self.post_upgrade(context)
        if command:
            self.run_in_venv(context, command[0], command[1:])

    def post_upgrade(self, context):
        pass


class EnvBuilder(ImprovedEnvBuilder):

    def __init__(self, system_site_packages=False, clear=False,
                 symlinks=False, upgrade=False):
        super().__init__(system_site_packages, clear, symlinks, upgrade)
        self.provisions_path = path.dirname(__file__)

    def post_setup(self, context):
        self.post_upgrade(context)
        scripts_path = path.join(self.provisions_path, 'scripts')
        self.install_scripts(context, scripts_path)

    def post_upgrade(self, context):
        print('[*] Install requirements')
        requirements_path = path.join(self.provisions_path, 'requirements.txt')
        self.install_pip_requirements(context, requirements_path)

    def install_distribute(self, context):
        print('[*] Installing distribute ... ', flush=True)
        res_path = path.join(self.provisions_path, 'distribute_setup.py')
        print(res_path)
        downloaded = download_file_if_not_exist(
            res_path,
            #'http://python-distribute.org/distribute_setup.py')
            'http://nightly.ziade.org/distribute_setup.py')
        if not downloaded:
            sys.stdout.write(
                '[!] Error: unable to download distribute install script\n')
            return False
        if not self.run_in_venv(context, context.python_exe, [res_path]):
            sys.stdout.write(
                '[!] Error: when runnig distribute install script\n')
            return False
        return True

    def install_pip(self, context):
        print('[*] Installing pip ... ', flush=True)
        res = self.run_in_venv(context, 'easy_install', ['pip'])
        if not res:
            print('[!] Error', flush=True)
        return res


def main(args):
    root_dir = path.join(path.dirname(__file__), 'my_venv')
    root_dir = path.abspath(root_dir)
    upgrade = path.exists(path.join(root_dir, 'pyvenv.cfg'))
    if not upgrade:
        print('[*] Installing venv on {}'.format(root_dir), flush=True)
    else:
        print('[*] Upgrating venv on {}'.format(root_dir), flush=True)

    builder = EnvBuilder(upgrade=upgrade)
    builder.create(root_dir, args)
    print('[*] Done', flush=True)