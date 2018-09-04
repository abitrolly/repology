# Copyright (C) 2016-2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import re

from repology.logger import Logger
from repology.package import Package
from repology.parsers import Parser


class PyPiHTMLParser(Parser):
    def iter_parse(self, path, logger):
        packages = {}

        with open(path, 'r', encoding='utf-8') as htmlfile:
            for match in re.findall('<td><a href="/pypi/([^"]+)/([^"]+)">[^<>]*</a></td>[ \n]*<td>([^<>]*)</td>', htmlfile.read(), flags=re.MULTILINE):
                pkg = Package()
                pkg.name = match[0]
                pkg.version = match[1]

                comment = match[2].strip()
                if comment == '':
                    logger.log('{}: summary is empty'.format(pkg.name), severity=Logger.ERROR)
                elif '\n' in comment:
                    logger.log('{}: summary is multiline'.format(pkg.name), severity=Logger.ERROR)
                else:
                    pkg.comment = comment

                pkg.homepage = 'https://pypi.python.org/pypi/{}/{}'.format(match[0], match[1])

                packages[pkg.name] = pkg

        yield from packages.values()
