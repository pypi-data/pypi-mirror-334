# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['backup_to_harddrive']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0.2']

entry_points = \
{'console_scripts': ['backup_to_harddrive = backup_to_harddrive.main:main']}

setup_kwargs = {
    'name': 'backup-to-harddrive',
    'version': '0.0.1',
    'description': 'Backup home files to Harddrive on Linux',
    'long_description': '# backup_to_harddrive\n\nThis script can typically be trigger when you want to backup files from your\nhome folder to one or more backup path (e.g harddrives.)\n\n## Targeted platform\n\n| Platform       | Implemented |\n|----------------|--------------------|\n| Linux          | [ x ]  |\n| Windows        | [ ] |\n| macOS          | []  |\n\n## Features included\n\n- Exclude folders by list\n- CLI switch on and off function (useful if you want to quickly reboot\nthe computer without triggering a long backup)\n- CLI retrieval of last date of backup\n- Creation of quick restore shell script. This is useful to quickly restore\npart of a backup (for instance, only document, or music etc.) on another machine.\n\n## Configuration file\n\nCreate a config file in `~/.config/backup_to_harddrive/config.yaml`.\nFollow this example\n\n```yaml\nbackup_configurations:\n  my_backup:\n    source: /home/foo\n    list_of_harddrive:\n      - /media/foo/hd1\n      - /media/foo/hd2\n    list_of_excluded_folders:\n     - .cache\n     - /home/foo/excluded\n  backup_two:\n    source: /home/bar\n    list_of_harddrive:\n      - /mnt/bar\n    list_of_excluded_folders:\n     - .config\n     - .cache\n```\n\n## Use cases\n\nSee [USECASES.md](USECASES.md)\n\n## Contributing\n\nSee [CONTRIBUTING.md](../CONTRIBUTING.md)\n',
    'author': 'Maxime Haselbauer',
    'author_email': 'maxime.haselbauer@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
