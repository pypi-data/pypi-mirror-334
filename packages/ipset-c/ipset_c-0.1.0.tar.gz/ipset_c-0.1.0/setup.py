# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipset_c']

package_data = \
{'': ['*']}

install_requires = \
['setuptools']

setup_kwargs = {
    'name': 'ipset_c',
    'version': '0.1.0',
    'description': 'IPSet written in C',
    'long_description': '# ipset_c\n\nIPSet is written in C.\nIt is designed to fast calculating ip/subnet/prefixes intersection, inclusion, joining, subtracting and other operations on IP sets. If you use pytricia or py-radix over netaddr.IPSet because of performance reasons, you should try this library.\nRuns on Windows, Linux, macOS. Wheels are available for supported versions.\nTens of times faster than pure Python netaddr IPSet.\nSupports both IPv4 and IPv6. Picklable. Can be compiled for free-threading usage.\n\n> [!IMPORTANT]\n> Due to the max sequence size in python(sys.maxsize), using len() with a large IPv6 IPSet raising an error. Use the IPSet([]).size attribute instead.\n\n> [!IMPORTANT]\n> Do not mix IPv4 and IPv6 in one IPSet without converting to IPv4-mapped IPv6. For example, instead of "0.0.0.0/32" pass "::ffff:0.0.0.0/128".\n\n## Installation\n\n```\npip install ipset_c\n```\n\n## Usage\n\n```\nfrom ipset_c import IPSet\na = IPSet([\'12.12.12.0/25\', \'12.12.12.128/25\'])\na.getCidrs()  # [\'12.12.12.0/24\']\na.addCidr(\'8.8.8.8/30\')\na.getCidrs()  # [\'8.8.8.8/30\', \'12.12.12.0/24\']\nb = IPSet([\'12.12.12.0/25\'])\na.isSubset(b)  # False\na.isSuperset(b)  # True\na == b  # False\na < b  # False\na <= b  # False\na > b  # True\na >= b  # True\na.isContainsCidr("12.12.0.0/16")  # False\na.isIntersectsCidr("12.12.0.0/16")  # True\nb.addCidr(\'4.4.4.4/32\')\na.getCidrs()  # [\'8.8.8.8/30\', \'12.12.12.0/24\']\nb.getCidrs()  # [\'4.4.4.4/32\', \'12.12.12.0/25\']\nc = a & b\nc.getCidrs()  # [\'12.12.12.0/25\']\nc = a | b\nc.getCidrs()  # [\'4.4.4.4/32\', \'8.8.8.8/30\', \'12.12.12.0/24\']\nc = a ^ b\nc.getCidrs()  # [\'4.4.4.4/32\', \'8.8.8.8/30\', \'12.12.12.128/25\']\nc = a - b\nc.getCidrs()  # [\'8.8.8.8/30\', \'12.12.12.128/25\']\na.removeCidr(\'8.8.8.8/30\')\na.getCidrs()  # [\'12.12.12.0/24\']\nlen(a)  # 256\na.size  # 256\nc = a.copy()\nbool(IPSet([]))  # False\nstr(IPSet([\'8.8.8.8/30\']))  # "IPSet([\'8.8.8.8/30\'])"\n```\n',
    'author': 'glowlex',
    'author_email': 'antonioavocado777@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
