#! /usr/bin/env python

# replace reference id in tex file to conform zotero refid style
##@article{crutzen_n2o_2008,
##        title = {N$_{\textrm{2}}${O} release from agro-biofuel production negates global warming reduction by replacing fossil fuels},
##        author = {Crutzen, P. J. and Mosier, A. R. and Smith, K. A. and Winiwarter, W.},
##}

import sys
import os

Ignore_st = set(['a', 'the'])

def parse_bib(f):
    d = {}
    with open(f) as fp:
        trigger = False
        refid = None
        title_key = None
        author_key = None
        year = None
        cnt = 0
        for line in fp:
            line = line.strip()
            if not line:
                continue

            if line.startswith('@'):
                trigger = True
                refid = line.split('{',1)[1].rstrip(',').rstrip() #@article{parrish_biology_2005,
            if trigger:
                #title = {The {Biology} and {Agronomy} of {Switchgrass} for {Biofuels}},

                line = line.lower()
                if line.startswith('title'):
                    title = line.split('{',1)[1].rsplit('}',1)[0].strip()
                    for word in title.split():
                        #N$_{\textrm{2}}${O}
                        if word.count('$') == 2: # find math mode
                            fisrt, second, third = word.split('$')
                            second = second.replace('{', ' ').replace('}', ' ')
                            t_lis = []
                            for item in second.split():
                                if item.startswith('\\'):
                                    continue
                                t_lis.append(item)
                            second = ''.join(t_lis)
                            second = ''.join([c for c in second if c.isalnum()])
                            word = first+second+third

                        word = word.replace('{', '').replace('}', '').rstrip(',')
                        
                        if word in Ignore_st:
                            continue
                        title_key = word
                        break
                        
                if line.startswith('author'):
                    author = line.split('=',1)[1].strip().strip('"').lstrip('{')
                    author_key = author.split(',',1)[0]

                if line.startswith('year'):
                    year = ''.join([c for c in line.split('=',1)[1] if c.isdigit()])

                if line == '}':
                    refid_new = '_'.join([author_key,title_key,year])
                    d[refid] = refid_new
                    print >> sys.stderr, '{} -- {}'.format(refid, refid_new)
                    cnt += 1
                    trigger = False
                    refid = None
                    title_key = None
                    author_key = None
                    year = None

    print >> sys.stderr, '*** records process: {}'.format(cnt)
    return d

def findall_iter(sub, string):
    """
    >>> text = "Allowed Hello Hollow"
    >>> tuple(findall_iter('ll', text))
    (1, 10, 16)
    """
    def next_index(length):
        index = 0 - length
        while True:
            index = string.find(sub, index + length)
            yield index
    return iter(next_index(len(sub)).next, -1)

def main():
    if len(sys.argv) != 4:
        mes = '*** python {} <file.bib> <file.tex> <out.tex>'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    bib = sys.argv[1]
    tex = sys.argv[2]
    outfile = sys.argv[3]
    d = parse_bib(bib)
    key = '\cite'
    with open(tex) as fp, open(outfile, 'wb') as fw:
        for line in fp:
            idx = 0
            while idx < len(line):
                idx = line.find(key, idx)
                if idx == -1:
                    break

                idx += len(key)
                left = line.find('{', idx)
                right = line.find('}', left)
                ref_str = line[left+1:right]
                ref_lis = [ref.strip() for ref in ref_str.split(',')]
                ref_len_lis = [len(item.split('_')) for item in ref_lis]
                if min(ref_len_lis) >= 3:
                    print >> sys.stderr, 'These refids match zotero style: {}, skipping'.format(ref_str)
                    continue
                    
                ref_lis_new = [d[ref] for ref in ref_lis]
                ref_str_new = ','.join(ref_lis_new)
                line = line[:left+1] + ref_str_new + line[right:]

            fw.write(line)


if __name__ == '__main__':
    main()
