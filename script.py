import subprocess as sp
import sys
import json
merged_branches = {}


def fire_command(cmd):
    """Fire the command"""

    return sp.check_output(cmd.split()).decode("utf-8")


def is_branch_in_merged_branches(candidate):
    """Check if canddidate is a branch that is in the merge_branches collection"""

    for x in merged_branches:
        if candidate in x:
            return True
    return False


def main_logic():
    global merged_branches

    # merged branches
    cmd1 = "git branch --merged"
    merged_branches = set([x.split()[-1]
                           for x in fire_command(cmd1).splitlines()])

    # current branch
    cmd2 = "git rev-parse --abbrev-ref HEAD"
    current_branch = fire_command(cmd2).strip()

    # get everything
    cmd3 = "git branch -r --sort=-committerdate --format='|%(HEAD)%(refname:short)|%09%(committerdate)|%09%(subject)|%09%(authorname)'"
    all_branches = fire_command(cmd3)

    count = 0
    data = []
    for line in all_branches.splitlines():
        """ Each line will look something like this: 
        [u"'", u' origin/master', u'\tTue May 18 07:48:33 2021 -0500', u'\tInitial commit', u"\tkermitt PDX'"]
        """
        print(line)
        pieces = line.split("|")
        print(pieces)
        refname = pieces[1].strip()
        comitterdate = pieces[2].strip()
        subject = pieces[3].strip()
        authorname = pieces[4].strip()
        # Boo... authornames have a trailing '
        authorname = authorname.replace("'", "")

        # this replace stuff feels squishy to me
        short_name = refname.replace("refs/remotes/origin/", "")
        short_name = short_name.replace("origin/", "")
        short_name = short_name.replace("\t", "")
        short_name = short_name.replace(" ", "")
        short_name = short_name.strip()

        TF = is_branch_in_merged_branches(short_name)
        merged = "___"
        if TF == True:
            merged = "[M]"
        count += 1

        ##########################################
        # PIPE DELIMITED -
        print("{}|{}|{}|{}|{}|{}".format(count, merged,
                                         refname, comitterdate, subject, authorname))

        ##########################################
        # JSON
    #     obj = {}
    #     obj["count"] = count
    #     obj["merge"] = merged
    #     obj["refname"] = refname
    #     obj["comitterdate"] = comitterdate
    #     obj["subject"] = subject
    #     obj["authorname"] = authorname
    #     data.append(obj)
    # print(json.dumps(data))


if __name__ == "__main__":
    main_logic()
