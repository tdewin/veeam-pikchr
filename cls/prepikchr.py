#!/usr/bin/env python3
import argparse
import sys
import re

# Define the Veeam preamble content
veeam_preamble = """//VEEAM PREAMBLE
//https://www.veeam.com/company/brand-resource-center.html
$viridis = 0x00d15f
$lime = 0x9cffa3
$mint = 0x32f26f
$pine = 0x007f49
$darkmineral = 0x505861
$frenchgrey = 0xADACAF
$fog = 0xf0f0f0
$sol = 0xffd839
$suma = 0xfe8a25
$casia = 0x8e71f4
$electricazure = 0x3700ff
$sky = 0x57e0ff
$ignis = 0xed2b3d

$grey = $darkmineral
$green = $viridis
$policy = $casia


//https://github.com/drhsqlite/pikchr/blob/2c46091ee5548d4fa3fedaea2fc8c0a05c5a89eb/pikchr.y#L975
thickness = 0.015*2

charwid = 0.06
charht = 0.10
linerad = 0.1
arrowht = 0.1
arrowwid = 0.12

$remove = 0xee00a0

fontscale = 1.7

//below icon label
define blbl {
  text with .n at $1.s $3 color $2
}
//above icon label
define albl {
  text with .s at $1.n $3 color $2
}

define netdot {
  dot at $1 vertex of NET color $grey
}
define conn {
  line from previous box $1 to previous dot.n color $grey
}

boxwid = 1
boxht = 1

$offset = boxht/1.5
$o = boxht/8
$oh = $o/2
$o2 = $o*2
$o3 = $o*3
$o4 = $o*4
$o5 = $o*5
$o6 = $o*6


//END VEEAM PREAMBLE

//DIAGRAM
//EDIT inside the DIAgram
DIA:[
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
]

//END DIAGRAM
C: dot at DIA.n+(0,boxht/2) invis
T: box with .c at previous.c color $grey "#TITLE#" big big big big bold fit invis

$mg = 0.3
DIABOX:line from T.w left until even with DIA.nw -($mg,0) then\
 down until even with DIA.sw -(0,$mg) then\
 right until even with DIA.se +($mg,0) then\
 up until even with T.e then \
 left until even with T.e then to T.e rad 0.2 color $frenchgrey thickness 200% 

"""




def strip_trailing_digit(s):
    return re.sub(r'\d+$', '', s)


def main():
    parser = argparse.ArgumentParser(description="Create a file with the Veeam preamble content.")
    parser.add_argument("--filename", help="The name of the file to create",default=None)
    parser.add_argument("--title", help="Title",default="")
    parser.add_argument("--icons","-i", help="Classes",default=["proxy0","repo0"],nargs='+')
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
    for conn in args.conns:
        s = conn.split(",")
        if len(s)>1:
            clns.append("{:10}  arrow -> from {} down boxht then down $o*{} then right until even with {} then to {} chop".format("",s[0].upper(),totalconns,s[1].upper(),s[1].upper()))
            clns.append("{:10}  text \"{}\" with .nw at 1st vertex of previous arrow +($o,-$o)".format("",conn))
        totalconns -= 1 
    icons = '\n'.join(lns)
    texts = '\n'.join(tlns)
    conns = '\n'.join(clns)
    outtext = veeam_preamble
    outtext = outtext.replace("#TITLE#",args.title).replace("#CLS#",icons).replace("#TEXTS#",texts).replace("#CONNS#",conns)

    if args.filename:
        with open(args.filename, 'w') as f:
            f.write(outtext)

        print(f"File '{args.filename}' created with Veeam preamble content.")
    else:
        print(outtext,file=sys.stdout)

if __name__ == "__main__":
    main()
