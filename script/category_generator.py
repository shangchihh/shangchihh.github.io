#!/usr/bin/env python

import glob
import os

post_dir = '_posts/'
draft_dir = '_drafts/'
category_dir = 'category/'

filenames = glob.glob(post_dir + '*md')
filenames = filenames + glob.glob(draft_dir + '*md')

total_categories = []
for filename in filenames:
    f = open(filename, 'r')
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split()
            if current_tags[0] == 'categories:' or current_tags[0] == 'category:':
                total_categories.extend(current_tags[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_categories = set(total_categories)

old_categories = glob.glob(category_dir + '*.md')
for category in old_categories:
    os.remove(category)

if not os.path.exists(category_dir):
    os.makedirs(category_dir)

for category in total_categories:
    category_filename = category_dir + category + '.md'
    f = open(category_filename, 'a')
    write_str = '---\nlayout: categorypage\ntitle: \"Category: ' + category + '\"\ncategory: ' + category + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Categories generated, count", total_categories.__len__())