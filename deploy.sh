#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

find $DIR/ -type d -exec chmod 775 {} +
find $DIR/ -type f -exec chmod 664 {} +
chmod 775 $DIR/deploy.sh
chmod 775 $DIR/__data/mk_products.py

