jekyll build
find _site -type d -exec chmod 775 {} +
find _site -type f -exec chmod 664 {} +
rsync -vrze ssh --delete _site/* root@tomato.immstudios.org:/var/www/sitigrema.cz/site/
