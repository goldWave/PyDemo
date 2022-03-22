import os,sys
from git import Repo, Commit

_files = ('.cpp','.h','.hpp','.c')
_repo_path = r'C:\Users\Administrator\Documents\source\PRISMLiveStudio'

 # python /c/Users/Administrator/Documents/source/PyDemo/clang_commit_self.py 10



def conrData():
    maxCount = 5
    print(sys.argv)
    if len(sys.argv) == 2:
        maxCount = sys.argv[1]

    repo = Repo(_repo_path)
    branch = repo.active_branch
    commits = list(repo.iter_commits(branch.name,author='jimbo', max_count=maxCount))

    _allList = set()
    for c in commits:
        print(c.summary) #commit message
        for x in c.stats.files:
           if os.path.splitext(x)[-1] in _files:
            _allList.add(x)
    os.chdir(_repo_path)
    _cmdStr = 'clang-format -i %s' % (" ".join(_allList))
    os.system(_cmdStr)

    # for x in _allList:
    #     print(x)

    print("\n\n\nchanged files:\n")
    print(repo.git.status()) #change files

def test():
    maxCount = 4
    print(sys.argv)
    if len(sys.argv) == 2:
        maxCount = sys.argv[1]

    repo = Repo(_repo_path)
    branch = repo.active_branch
    commits = list(repo.iter_commits(branch.name,author='jimbo', max_count=maxCount))

    _allList = set()
    for c in commits:
        print(c) #commit message
        
        with open(r'C:\Users\Administrator\Desktop\response.txt', 'a') as f:
            f.writelines(repo.git.show(c))

        # for x in c.stats.files:
        #    if os.path.splitext(x)[-1] in _files:
        #     _allList.add(x)
    # os.chdir(_repo_path)
    # _cmdStr = 'clang-format -i %s' % (" ".join(_allList))
    # os.system(_cmdStr)

    # # for x in _allList:
    # #     print(x)

    # print("\n\n\nchanged files:\n")
    # print(repo.git.status()) #change files

if __name__ == '__main__':
    conrData()