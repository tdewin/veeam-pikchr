#!/usr/bin/env python3
import argparse
import sys
import re

# Sample Content
sample = """
            //
            //replacements
            
            color = $remove
#CLS#

            //texts
            color = $grey

#TEXTS#


            //connections

#CONNS#

            //
"""




def strip_trailing_digit(s):
    return re.sub(r'\d+$', '', s)


def main():
    parser = argparse.ArgumentParser(description="Create a file with some pre content.")
    parser.add_argument("--filename", help="The name of the file to create",default=None)
    parser.add_argument("--title", help="Title",default="")
    parser.add_argument("icons", help="Classes",default=["proxy0","repo0"],nargs='+')
    parser.add_argument("--conns","-c", help="Connections",default=["proxy0,repo0"],nargs='+')
    args = parser.parse_args()

    lns =[]
    tlns = []
    for icon in args.icons:
        nodigit = strip_trailing_digit(icon)
        lns.append("{:10}: box \"{}\" color $remove".format(icon.upper(),nodigit))
        lns.append("{:10}  {}".format("","move"))
        tlns.append("{:10}  albl({},$grey,\"{}\")".format("",icon.upper(),nodigit.title()))

    clns = []
    totalconns = len(args.conns)
    hconns =  int(len(args.conns)/2)
    for conn in args.conns:
        s = conn.split(",")
        sid = conn.upper().replace(",","")
        if len(s)>1:
            clns.append("{:10}: arrow -> from {} down boxht then down $o*{} then right until even with {}.s+($o*{},0) then to {}.s + ($o*{},0) chop".format(sid,s[0].upper(),totalconns,s[1].upper(),totalconns-hconns,s[1].upper(),totalconns-hconns))
            clns.append("{:10}  text \"{}\" with .nw at 1st vertex of {} +($o,-$o)".format("",conn,sid))
        totalconns -= 1 
    icons = '\n'.join(lns)
    texts = '\n'.join(tlns)
    conns = '\n'.join(clns)
    outtext = sample
    outtext = outtext.replace("#TITLE#",args.title).replace("#CLS#",icons).replace("#TEXTS#",texts).replace("#CONNS#",conns)

    if args.filename:
        with open(args.filename, 'w') as f:
            f.write(outtext)

        print(f"File '{args.filename}' created (prepic).")
    else:
        print(outtext,file=sys.stdout)

if __name__ == "__main__":
    main()
