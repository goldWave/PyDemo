from typing import List
import os

import os
from git import Repo, Commit

_files = ('.cpp','.h','.hpp')
_repo_path = r'C:\Users\Administrator\Documents\source\PRISMLiveStudio'

def test():


if __name__ == '__main__':
    maxCount = 10
    if len(sys.argv) == 2:
        maxCount = sys.argv[2]
    repo = Repo(_repo_path)
    branch = repo.active_branch
    commits = list(repo.iter_commits(branch.name,author='jimbo', max_count=maxCount))

    _allList = set()
    for c in commits:
        for x in c.stats.files:
           if os.path.splitext(x)[-1] in _files:
            _allList.add(x)
    os.chdir(_repo_path)
    _cmdStr = 'clang-format -i %s' % (" ".join(_allList))
    os.system(_cmdStr)