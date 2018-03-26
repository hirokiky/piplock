import argparse
import configparser
import os
import subprocess
import tempfile


PROJECT_DIR_FILES = ['setup.cfg', 'requirements.txt']


def detect_project_dir():
    """ Detect path to tox.ini
    """
    current_dir = os.getcwd()
    while current_dir != '/':
        if set(PROJECT_DIR_FILES) & set(os.listdir(current_dir)):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise ValueError('Cloud not detect project root.')


def parse_reqs(s):
    return [row.strip() for row in s.strip().splitlines()]


def parse_conf():
    """
    [piplock:common]
    reqs = sqlalchemy

    [piplock:dev]
    reqs =
        testfixtures
        factory-boy

    [piplock:prod]
    reqs = psycopg2
    """
    config = configparser.ConfigParser()
    with open(os.path.join(detect_project_dir(), 'setup.cfg')) as f:
        config.read_file(f)

    return {
        'common': parse_reqs(config['piplock:common']['reqs']),
        'dev': parse_reqs(config['piplock:dev']['reqs']),
        'prod': parse_reqs(config['piplock:prod']['reqs'])
    }


def target_packages(dev=False, prod=False):
    conf = parse_conf()
    packages = conf['common']
    if dev:
        packages.extend(conf['dev'])
    if prod:
        packages.extend(conf['prod'])

    return packages


def remove_packaging_libs(reqs):
    packaging_libs = [
        'pkg-resources',
        'pip',
        'virtualenv',
        'setuptools',
        'distribute',
    ]
    packages = []
    for row in reqs.splitlines():
        for p in packaging_libs:
            if p in row:
                break
        packages.append(row)
    return '\n'.join(packages)


def install(dev=False, prod=False):
    subprocess.run(['pip', 'install', *target_packages(dev, prod)])


def lock(dev=False, prod=False):
    with tempfile.TemporaryDirectory() as td:
        venv_path = os.path.join(td, 'venv')
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        subprocess.run(['python', '-m', 'venv', venv_path])
        subprocess.run([pip_path, 'install', *target_packages(dev, prod)])
        process = subprocess.run([pip_path, 'freeze'], stdout=subprocess.PIPE)

    reqs = remove_packaging_libs(process.stdout.decode())

    with open(os.path.join(detect_project_dir(), 'requirements.txt'),
              mode='w') as f:
        f.write(reqs)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('--dev', action='store_true')
    install_parser.add_argument('--prod', action='store_true')
    install_parser.set_defaults(func=install)

    lock_parser = subparsers.add_parser('lock')
    lock_parser.add_argument('--dev', action='store_true')
    lock_parser.add_argument('--prod', action='store_true')
    lock_parser.set_defaults(func=lock)

    args = parser.parse_args()
    args.func(args.dev, args.prod)


if __name__ == '__main__':
    main()
