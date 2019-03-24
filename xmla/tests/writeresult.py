#! /usr/bin/env python
import olap.xmla.xmla as xmla
import olap.xmla.utils as utils
import pprint
import os.path


def main(mdxfile, location, catalog, username, password, spn, sslverify):
    p = os.path.dirname(os.path.realpath(__file__))
    pyfile = os.path.join(p, os.path.splitext(mdxfile)[0] + os.path.extsep + "py")
    cmd = open(os.path.join(p,mdxfile)).read()

    p = xmla.XMLAProvider()
    c=p.connect(location=location, username=username, 
                password=password, spn=spn, sslverify=sslverify)
    res=c.Execute(cmd, Catalog=catalog)
    x=utils.dictify(res.root)

    erg=pprint.pformat(x)
    print("erg-type",type(erg))
    open(pyfile, "w+").write('"""\n%s\n"""\n\nresult=%s\n' % (cmd, erg))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MDX Resultwriter.")
    parser.add_argument("mdxfile")
    parser.add_argument("--location", dest="location", 
                        help="location von XMLASource", 
                        default="http://localhost:8080/xmondrian/xmla")
    parser.add_argument("--catalog", dest="catalog", 
                        help="catalog to execute the mdx in", 
                        default="FoodMart")
    parser.add_argument("--username", dest="username", help="connect as user", 
                        default=None)
    parser.add_argument("--password", dest="password", help="use password", 
                        default=None)
    parser.add_argument("--spn", dest="spn", 
                        help="spn, defaults to HTTP@host if omitted")
    parser.add_argument("--sslverify", dest="sslverify", default=True,
                        help="sslverify, either False or path of cert file")
    args = parser.parse_args(['--location=http://dwh-bi.kiebackpeter.kup/olap/msmdpump.dll', 
                                '--catalog=Adventure Works DW 2008R2', 'tt.txt'])

    if isinstance(args.sslverify, str):
        if args.sslverify.upper() in ["0", "FALSE", "NO", "NEIN"]:
            args.sslverify = False

    main(args.mdxfile, args.location, args.catalog, 
         args.username, args.password, args.spn, args.sslverify)

else:
    main("tt.txt", "http://dwh-bi.kiebackpeter.kup/ola/msmdpump.dll", "Adventure Works DW 2008R2", 
         None, None, None, False)
