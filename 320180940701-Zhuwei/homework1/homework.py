__author__ = "ZhuWei"
__address__ = 'Lanzhou University'
__studentID__ = "320180940701"
__date__ = "3/20/2020"
__email__ = "zhuw2018@lzu.edu.cn"

import  re,argparse
import prettytable as pt
from subprocess import Popen,PIPE, DEVNULL




class Commit():
    def __init__(self,rev):
        self.rev=rev
    def get_commit_cnt(self,next_rev):
     tagrange = self.rev + ".." + next_rev
     gitcnt = "git rev-list --pretty=format:\"%ai\" " + tagrange
     git_list = Popen(gitcnt, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
     if git_list is not None:
         pass
     else:
         ex=Exception('The data does not exist')
         raise ex
     raw_counts = git_list.communicate()[0]
     cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
     return len(cnt)
    def get_tag_days(self):
        gittag = "git log -1 --pretty=format:\"%ct\" " + self.rev
        git_date = Popen(gittag, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds =int(git_date()[0])
        return (seconds)//(3600*24)
    def _print(self):
        tb = pt.PrettyTable()
        tb.field_names = ["version", "days", "commits"]
        for sl in range(1, self.revrange+1):
            print(".")
            rev2 = self.rev + "." + str(sl)
            days, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                tb.add_row([rev2, days, commit_cnt])
            else:
                break
        with open('result', 'a') as f:
            f.write(str(tb))
        print(tb)
        print('The result has been written into "result" file')

# get dates of all commits - unsorted 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("revision", help="the version tag you want to start checking, example: v4.1")
    parser.add_argument("range", type=int, help="the range of revision you want to check")
    args = parser.parse_args()
    rev_in = args.revision
    range_in = args.range
    rev = Commit(rev_in, int(range_in))
    rev.log_print()
if __name__=='__main__':
    main()
