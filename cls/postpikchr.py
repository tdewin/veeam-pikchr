#!/usr/bin/env python3

import argparse
import sys
import xml.etree.ElementTree as ET
import re
import subprocess
import platform

from pathlib import Path

def parse_svg_or_xml(tree,magic,verbose,font,searchdir,scale=1,fontscale=1):
    try:

        root = tree.getroot()
        
        # Define the SVG namespace
        ns = {'svg': 'http://www.w3.org/2000/svg'}



        #for autoremove
        #$remove = 0xee00a0
        #stroke: rgb(238,0,160);
        path_elements = root.findall('.//svg:path', namespaces=ns)
        for e in path_elements:
          if "style" in e.attrib:
            if magic in e.attrib["style"]:
                root.remove(e)


	# Find all <text> elements using XPath
        text_elements = root.findall('.//svg:text', namespaces=ns)

        mpct = re.compile(r'([0-9\.]+)[%]')
        if font:
            newstyle = ET.Element('{http://www.w3.org/2000/svg}style',attrib={}) 
            newstyle.text = "text { font-family: \""+font+"\"}"
            root.insert(0,newstyle)
        

        
        
        fblank=searchdir / "{}.svg".format("blank")

        for elem in text_elements:
          escale = scale
          ctxt = ""
          if elem.text:
            ctxt = elem.text
          if ctxt != ""  and "fill" in elem.attrib and elem.attrib["fill"] == magic:
            if verbose:
              print(f"Text content: '{elem.text}' | Attributes: {elem.attrib}",file=sys.stderr)
            x=float(elem.attrib['x'])
            y=float(elem.attrib['y'])
            idn=ctxt.lower().replace(" ","-")

            sq = 100
            wid = sq
            ht = sq

          

            newe = ET.Element('{http://www.w3.org/2000/svg}rect', attrib={'x': '0', 'y': '0', 'width': "{}".format(escale*wid), 'height':"{}".format(escale*ht) , 'fill':'#00ff00'})

            ftest=searchdir / "{}.svg".format(idn)
            if ftest.exists():
               clstree = ET.parse(ftest)
               clsroot = clstree.getroot()
               gs=clsroot.findall('.//svg:g',namespaces=ns)
               if len(gs) > 0:
                 if "viewBox" in clsroot.attrib:
                   vb = clsroot.attrib["viewBox"]
                   flarr = [float(x) for x in vb.split(' ')]
                   if len(flarr) > 3:
                     wid = flarr[2]
                     ht = flarr[3]
                     escale=sq/max(wid,ht)*escale
                     if verbose:
                       print(wid,ht,escale,file=sys.stderr)
                 newe = gs[0]
               else:
                 print("ooops, no g's",file=sys.stderr)
            elif fblank.exists():
               blktree = ET.parse(fblank)
               blkroot = blktree.getroot()
               gs=blkroot.findall('.//svg:g',namespaces=ns)
               if len(gs) > 0:
                 txt=blkroot.findall('.//svg:text',namespaces=ns)
                 if len(txt) > 0:
                   txt[0].text = idn
                 newe = gs[0]
               else:
                 print("ooops, no g's",file=sys.stderr)
            else:
              print("ooops, no blank",file=sys.stderr)

            root.remove(elem)
            newg = ET.Element('{http://www.w3.org/2000/svg}g',attrib={'transform': "translate({},{}) scale({})".format(x-(wid/2*escale),y-(ht/2*escale),escale),'id':idn}) 
            newg.append(newe) 
            root.append(newg)
          else:
            if "font-size" in elem.attrib:
              fs = elem.attrib['font-size']
              pct = mpct.match(fs)
              if pct:
                fpct = float(pct.group(1))
                elem.attrib['font-size'] = "{}%".format(fpct*fontscale)
            else:
             elem.attrib['font-size'] = "{}%".format(100*fontscale)
        return tree

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

def main():
    epilogtxt = "For branding assests such as logo's or fonts, go to https://www.veeam.com/company/brand-resource-center.html"
    parser = argparse.ArgumentParser(description="Parse SVG/XML from stdin.",epilog=epilogtxt)
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--output', '-o', type=str, help='Output file path (default: stdout)')
    parser.add_argument('--magic', type=str, help='Magic code color for replacement (default: rgb(238,0,160))',default="rgb(238,0,160)")
    parser.add_argument('--font', '-f', type=str, help='Font for update (ES Build default, custom Veeam Font request via branding)', default="ES Build") 
    parser.add_argument('--fontscale', '-r', type=float, help='Scale font', default=1.2) 
    parser.add_argument('--dir', '-d', type=Path, help='Search for svgs in this path',default=Path("."))
    parser.add_argument('--scale', '-s', type=float, help='Scale images',default=1.45)
    parser.add_argument('--clipboard','-c',action='store_true',help='Read from clipboard')

    args = parser.parse_args()

    tree = 0
    if args.clipboard:
      if platform.system() == 'Darwin':
        p = subprocess.Popen(['pbpaste', 'r'],stdout=subprocess.PIPE,text=True)
        clipboarddata,stderr = p.communicate()
        root = ET.fromstring(clipboarddata)
        tree = ET.ElementTree(root)
      else:
        print("Only mac support for clipboard, use cat file | ./script or something similar to pipe output to stdin")
        sys.exit()
    else:
      tree = ET.parse(sys.stdin)
      

    ET.register_namespace('', 'http://www.w3.org/2000/svg')


    tree = parse_svg_or_xml(tree,args.magic,args.verbose,args.font,args.dir,args.scale,args.fontscale)


    if args.output:
      tree.write(args.output, encoding='utf-8', xml_declaration=True)
    else:
      tree.write(sys.stdout, encoding='unicode')

if __name__ == "__main__":
    main()

