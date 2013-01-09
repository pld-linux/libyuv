#!/bin/sh
# Make snapshot of libyuv
# Author: Elan Ruusamäe <glen@pld-linux.org>
set -e

package=libyuv
specfile=$package.spec
baseurl=http://$package.googlecode.com/svn
svnurl=$baseurl/trunk
ext=xz
tarball=$package-$(date +%Y%m%d).tar.$ext

# get depot tools
# http://www.chromium.org/developers/how-tos/install-depot-tools
test -d depot_tools || {
	# could also checkout:
	# svn co http://src.chromium.org/svn/trunk/tools/depot_tools
	wget -c https://src.chromium.org/svn/trunk/tools/depot_tools.zip
	unzip -qq depot_tools.zip
	chmod a+x depot_tools/gclient depot_tools/update_depot_tools
}

topdir=${PWD:-($pwd)}
gclient=$topdir/gclient.conf
install -d $package
cd $package

if [ ! -f $gclient ]; then
	# create initial config that can be later modified
	../depot_tools/gclient config $svnurl --gclientfile=$gclient
fi

cp -p $gclient .gclient

# emulate gclient config, preserving our deps
sed -i -re '/"url"/ s,"http[^"]+","'$svnurl'",' .gclient

../depot_tools/gclient sync --nohooks -v

cd ..

XZ_OPT=-e9 tar -cf $tarball --$ext  --exclude-vcs $package
../md5 $specfile
../dropin $tarball &
