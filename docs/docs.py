#!/usr/bin/env python

import darmbits
import darmtbl
import darmtblthumb
import darmtblthumb2
import darmtblvfp

def html_styles():
    s = '<style type="text/css">\n'
    tdform = 'padding-left: %dpx; background-color: rgb(224, 224, 224); text-align: %s; color: rgb(0, 0, 0); font-size: 13px; font-weight: 900; font-family: monospace; word-wrap: break-word; border-top-left-radius: 1px; border-top-right-radius: 1px; border-bottom-right-radius: 1px; border-bottom-left-radius: 1px;'
    thform = 'padding-left: %dpx; width: 24px; background-color: rgb(85, 136, 187); text-align: %s; color: rgb(256, 256, 256); font-size: 13px; font-weight: 900; font-family: monospace; border-top-left-radius: 2px; border-top-right-radius: 2px; border-bottom-right-radius: 2px; border-bottom-left-radius: 2px;'
    for n in 'td', 'th':
        t = eval(n + 'form')
        s += '%s.%s { %s }\n' % (n, 'bits', t % (0, 'center'))
        s += '%s.%s { %s }\n' % (n, 'form', t % (8, 'left'))

    s += 'tr:hover td { background: #aaa; }'
    s += '</style>'
    return s

def html_esc(token):
    t = token
    esc = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    for r in esc.keys():
        t = t.replace(r, esc[r])
    return t

def html_doc(content):
    s = '<html><body>'
    s += html_styles()
    s += content
    s += '</body></html>'
    return s

def html_table(size, elements):
    s = '<table>'
    s += html_row(['Instruction Format'] + range(size), True)
    for e in elements:
        s += e
    s += '</table>\n'
    return s

def html_row(insn, head = False):
    h = 'd'
    if head:
        h = 'h'

    s = '<tr>'
    for i in insn:
        t = None
        l = None
        c = None
        if isinstance(i, int):
            t = str(i)
            l = 1
            c = 'bits'
        elif isinstance(i, darmbits.Bitsize) or isinstance(i, darmtbl.Operand):
            t = i.name
            l = i.bitsize
            c = 'bits'
        else:
            t = html_esc(str(i))
            l = 1
            c = 'form'
        assert(t != None and l != None and c != None)
        s += '<t%s colspan="%d" class="%s">%s</t%s>' % (h, l, c, t, h)

    return s + '</tr>\n'


def make_doc(desc, size, insns, fname):
    f = open(fname, 'w')
    f.write(html_doc('<h1>%s</h1>' % desc + html_table(size, [html_row(i) for i in insns])))
    f.close()

def main():
    make_doc('Thumb Instruction Encodings (16-bit)', 16, darmtblthumb.thumbs, 'thumb.html')
    make_doc('Thumb2 Instruction Encodings (16-bit)', 16, darmtblthumb2.thumb16, 'thumb2_16.html')
    make_doc('Thumb2 Instruction Encodings (32-bit)', 32, darmtblthumb2.thumb32 + darmtblvfp.thumbvfp, 'thumb2.html')
    make_doc('ARMv7 Instruction Encodings (32-bit)', 32, darmtbl.ARMv7 + darmtblvfp.armvfp, 'armv7.html')

if __name__ == '__main__':
    main()
