#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from slugify import slugify
from PIL import Image

CATS = ["Koníci", "Pejsci a kočičky", "Jiná zvířátka", "Ostatní"]


class BaseObject:
    def __init__(self, title):
        self.title = title

    @property
    def slug(self):
        return slugify(self.title)


class Product(BaseObject):
   pass


class Group(BaseObject):
    def __init__(self, title):
        BaseObject.__init__(self, title)
        self.products = []

    def append(self, ptitle):
        self.products.append(Product(ptitle))


used_products = []

result = ""

for id_cat, cat_title in enumerate(CATS):
    cat_file = "source_data{}".format(id_cat)
    cat_slug = slugify(cat_title)
    result += "- id    : {}\n".format(id_cat)
    result += "  title : {}\n".format(cat_title)
    result += "  slug  : {}\n".format(cat_slug)


    if not os.path.exists(cat_file):
        continue

    result += "  groups :\n"

    groups = []
    current_group = None

    data_feed = open(cat_file)
    for line in data_feed.readlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("::"):
            group_title = line.lstrip("::")
            groups.append(Group(group_title))
            continue

        if not groups:
            continue

        groups[-1].append(line)


    for id_group, group in enumerate(groups):
        id_group += 1
        result += "    - id    : {}\n".format(id_group)
        result += "      title : {}\n".format(group.title)
        result += "      slug  : {}\n".format(group.slug)

        if group.products:
            result += "      products :\n"

        cpath = "../{}/{}/".format(cat_slug, group.slug)
        if not os.path.exists(cpath):
            os.makedirs(cpath)
        f = open(cpath + "index.html", "w")
        f.write("---\n")
        f.write("layout: product_group\n")
        f.write("title: {}\n".format(group.title))
        f.write("cat_slug : {}\n".format(cat_slug))
        f.write("group_slug: {}\n".format(group.slug))

        
        #
        # Group thumbnail (barevne sady)
        #

        ifile = os.path.join("products", group.slug+".jpg")
        if os.path.exists(ifile):
            itgt = group.slug+".jpg"
            itgt_tn = group.slug+"_tn.jpg"
            f.write("group_image: {}\n".format(itgt))
            im_orig = Image.open(ifile)
            
            im = im_orig.resize((640,400), Image.ANTIALIAS)
            im.save(itgt)

            im = im_orig.resize((261,163), Image.ANTIALIAS)
            im.save(itgt_tn)

        #
        # Products
        #


        if group.products:
            f.write("products:\n")
        
        for id_product, product in enumerate(group.products):
            id_product += 1000*id_group
            result += "        - id   : {}\n".format(id_product)
            result += "          title: {}\n".format(product.title)
            result += "          slug : {}\n".format(product.slug)

            f.write("  - id   : {}\n".format(id_product))
            f.write("    title: {}\n".format(product.title))
            f.write("    slug : {}\n".format(product.slug))


            pfile = os.path.join("products", product.slug+".txt")
            ifile = os.path.join("products", product.slug+".jpg")
            ptext = ""
            pprices = []
            if os.path.exists(pfile):
                for pline in open(pfile).readlines():
                    r = pline.split(":")
                    if len(r) == 2 and r[1].strip().isdigit():
                        pprices.append(r)
                        continue
                    ptext += pline
            else:
                print (pfile, "does not exist")

            ptfile = cpath + product.slug + ".md"
            pt = open(ptfile, "w")
            pt.write("---\n")
            pt.write("layout: product\n")
            pt.write("title: {}\n".format(product.title))
            pt.write("cat_slug : {}\n".format(cat_slug))
            pt.write("group_slug: {}\n".format(group.slug))
            pt.write("slug: {}\n".format(product.slug))
            if pprices:
                pt.write("pricing:\n")
                for v, c in pprices:
                    pt.write("  - variant : {}\n".format(v.strip()))
                    pt.write("    price   : {}\n".format(c.strip()))
            pt.write("---\n")
            pt.write("\n{}\n\n".format(ptext.strip()))
            pt.close()



            if not os.path.exists(ifile):
                ifile = "default.jpg"

            iffile = cpath + product.slug + ".jpg"    
            itfile = cpath + product.slug + "_tn.jpg"

            im_orig = Image.open(ifile)
            
            im = im_orig.resize((640,400), Image.ANTIALIAS)
            im.save(iffile)

            im = im_orig.resize((261,163), Image.ANTIALIAS)
            im.save(itfile)

            used_products.append(product.slug)
           

        f.write("---\n")

        #
        # Group description
        #

        pfile = os.path.join("products", group.slug+".txt")
        if os.path.exists(pfile):
            pf = open(pfile).read()
            f.write(pf)
            f.close()


        result += "\n"



for p in os.listdir("products"):
    p = os.path.splitext(p)[0]
    if not p in used_products:
        print ("Unused", p)


f = open("../_data/products.yml","w")
f.write(result)
f.close()

