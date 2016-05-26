#!/usr/bin/env python3

import os
import shutil
import json

import yaml

from PIL import Image
from nxtools import *

class GremaProduct():
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.slug = slugify(title)

    @property
    def data_dir(self):
        return self.parent.data_dir

    @property
    def site_dir(self):
        return self.parent.site_dir

    @property
    def data_path(self):
        return os.path.join(self.data_dir, self.parent.parent.slug, self.parent.slug, self.slug + ".txt")

    @property
    def image_path(self):
        return os.path.join(self.data_dir, self.parent.parent.slug, self.parent.slug, self.slug + ".jpg")

    @property
    def has_image(self):
        return os.path.exists(self.image_path)

    @property
    def meta(self):
        group_slug = self.parent.slug
        cat_slug = self.parent.parent.slug
        return {
            "slug" : self.slug,
            "title" : self.title,
            "group_slug" : group_slug,
            "group_title" : self.parent.title,
            "cat_slug" :  cat_slug,
            "cat_title" : self.parent.parent.title,
            "has_image" : self.has_image,
            "image" : os.path.join("/products", cat_slug, group_slug,  "{}.jpg".format(self.slug)) if self.has_image else "false"
        }

    def build(self, root_dir):
        #output_dir = os.path.join(self.site_dir, "products", self.meta["cat_slug"], self.meta["group_slug"])
        if not os.path.exists(self.data_path):
            logging.warning("{} data file does not exist".format(self.data_path))
            return

        # read description and pricelist

        product_text = ""
        pricelist = []
        for pline in open(self.data_path).readlines():
            r = pline.split(":")
            if len(r) == 2 and r[1].strip().isdigit():
                pricelist.append(r)
                continue
            product_text += pline

	# write file

        with open(os.path.join(root_dir, self.meta["slug"] + ".md"), "w") as f:
            f.write("---\nlayout: product\n")
            for key in self.meta:
                f.write("{} : {}\n".format(key, self.meta[key]))
            if pricelist:
                f.write("pricing:\n")
                for v, c in pricelist:
                    f.write("  - variant : {}\n".format(v.strip()))
                    f.write("    price   : {}\n".format(c.strip()))
            f.write("---\n")
            f.write("\n{}\n\n".format(product_text.strip()))

        # create images
        if self.has_image:
            original_image = Image.open(self.image_path)
            image_full_path = os.path.join(root_dir, "{}.jpg".format(self.slug))
            image_thumb_path = os.path.join(root_dir, "{}_tn.jpg".format(self.slug))

            if os.path.exists(image_full_path):
                image_full = original_image.resize((800, 500), Image.ANTIALIAS)
                image_full.save(image_full_path)

            if not os.path.exists(image_thumb_path):
                image_thumb = original_image.resize((261, 163), Image.ANTIALIAS)
                image_thumb.save(image_thumb_path)


class GremaProductGroup():
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.slug = slugify(title)
        self.products = []

    def get_product(self, query):
        for product in self.products:
            if product.title == query or product.slug == query:
                return product

    @property
    def description(self):
        return "TODO: group description"

    @property
    def data_dir(self):
        return self.parent.data_dir

    @property
    def group_dir(self):
        return os.path.join(self.data_dir, self.parent.slug, self.slug)

    @property
    def site_dir(self):
        return self.parent.site_dir

    @property
    def meta(self):
        return {
            "title" : self.title,
            "slug" : self.slug,
            "group_slug" : self.slug, # kvuli zvyraznovani v sidebaru
            "cat_slug" : self.parent.slug,
            "has_index" : os.path.exists(os.path.join(self.group_dir, "index.txt")),
            "has_image" : os.path.exists(os.path.join(self.group_dir, "index.jpg"))
        }

    @property
    def map(self):
        result = {key : self.meta[key] for key in self.meta}
        result["products"] = [product.meta for product in self.products]
        return result

    def build(self, root_dir):
        group_dir = os.path.join(root_dir, self.slug)
        if not os.path.exists(group_dir):
            os.makedirs(group_dir)

        # Create group index page

        with open(os.path.join(group_dir, "index.md"), "w") as f:
            f.write("---\nlayout: product_group\n")
            for key in self.meta:
                f.write("{} : {}\n".format(key, self.meta[key]))
            f.write("products:\n")
            for product in self.products:
                f.write("  - slug: {}\n".format(product.slug))
                f.write("    title: {}\n".format(product.title))
                f.write("    has_image: {}\n".format(product.has_image))
            f.write("---\n\n")

            index_path = os.path.join(self.data_dir, self.parent.slug, self.slug, "index.txt")
            if os.path.exists(index_path):
                f.write(open(index_path).read())

        # Convert index image

        index_image_path = os.path.join(self.data_dir, self.parent.slug, self.slug, "index.jpg")
        if os.path.exists(index_image_path):
            original_image = Image.open(index_image_path)
            image_full_path = os.path.join(group_dir, "index.jpg")
            image_thumb_path = os.path.join(group_dir, "index_tn.jpg")

            image_full = original_image.resize((800, 500), Image.ANTIALIAS)
            image_full.save(image_full_path)
            image_thumb = original_image.resize((261, 163), Image.ANTIALIAS)
            image_thumb.save(image_thumb_path)


        # Build products

        for product in self.products:
            product.build(group_dir)






class GremaCategory():
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.slug = slugify(title)
        self.load_groups()

    def get_product(self, query):
        for group in self.groups:
            product = group.get_product(query)
            if product:
                return product

    @property
    def data_dir(self):
        return self.parent.data_dir

    @property
    def site_dir(self):
        return self.parent.site_dir

    @property
    def map(self):
        return {
                "title" : self.title,
                "slug" : self.slug,
                "groups" : [group.map for group in self.groups if (group.products or group.meta["has_index"])]
            }

    def load_groups(self):
        self.groups = []
        index_path = os.path.join(self.data_dir, "index-{}.yml".format(self.slug))
        if not os.path.exists(index_path):
            logging.error("{} does not exist".format(index_path))
            return
        data = yaml.safe_load(open(index_path))
        if not data:
            logging.error("No data in {}".format(index_path))
            return
        for group_title in data.keys():
            logging.debug("Creating category {}".format(group_title))
            group = GremaProductGroup(self, group_title)
            if data[group_title]:
                for product_title in data[group_title]:
                    product = GremaProduct(group, product_title)
                    group.products.append(product)
            self.groups.append(group)

    def build(self, root_dir):
        category_dir = os.path.join(root_dir, self.slug)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        for group in self.groups:
            group.build(category_dir)


class GremaSite():
    def __init__(self):
        self.data_dir = "_source"
        self.site_dir = "."
        self.load_categories()

    def get_product(self, query):
        for category in self.categories:
            product = category.get_product(query)
            if product:
                return product

    def load_categories(self):
        self.categories = []
        index_path = os.path.join(self.data_dir, "index.yml")
        if not os.path.exists(index_path):
            return
        for category_title in yaml.safe_load(open(index_path))["categories"]:
            category_title = to_unicode(category_title)
            self.categories.append(GremaCategory(self, category_title))

    def build(self):
        product_map = []
        root_dir = os.path.join(self.site_dir, "products")
        for category in self.categories:
            logging.info("Creating category {}".format(category.title))
            category.build(root_dir)
            cmap = category.map
            if cmap["groups"]:
                product_map.append(cmap)

        product_map_path = os.path.join(self.site_dir, "_data", "products.yml")
        with open(product_map_path, 'w') as outfile:
            outfile.write(
                yaml.dump(product_map)
                )

        with open("data.json","w") as f:
            json.dump(product_map, f)

        # Default thumbnail

        original_image = Image.open(os.path.join(self.data_dir, "default.png"))
        image_full_path = os.path.join(self.site_dir, "static", "default.jpg")
        image_thumb_path = os.path.join(self.site_dir, "static", "default_tn.jpg")

        image_full = original_image.resize((640, 400), Image.ANTIALIAS)
        image_full.save(image_full_path)
        image_thumb = original_image.resize((261, 163), Image.ANTIALIAS)
        image_thumb.save(image_thumb_path)




def import_products(site, data_dir):
    for fname in os.listdir(data_dir):
        if os.path.splitext(fname)[1] != ".txt":
            continue
        product_source_path = os.path.join(data_dir, fname)
        base_name = get_base_name(fname)
        image_source_path = os.path.join(data_dir, base_name + ".jpg")
        product = site.get_product(base_name)
        if not product:
            continue

        product_dir = os.path.dirname(product.data_path)
        if not os.path.exists(product_dir):
            os.makedirs(product_dir)

        shutil.copy2(product_source_path, product.data_path)
        if os.path.exists(image_source_path):
            shutil.copy2(image_source_path, product.image_path)


if __name__ == "__main__":
    grema = GremaSite()
    grema.build()
