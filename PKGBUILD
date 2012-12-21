# Maintainer: Nekolyanich <gmail@nekolyanich.com>
pkgname=python2-psys
pkgver=0.1
pkgrel=1
pkgdesc="A Python module with a set of basic tools for writing system utilities"
arch=("i686" "x86_64")
url="http://github.com/KonishchevDmitry/psys"
license=("GPL3")
depends=("python2")
makedepends=("git")
provides=("python2-psys")
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
source=()
md5sums=()

_gitroot="git://github.com/KonishchevDmitry/psys.git"
_gitname="psys"

build () {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $_gitname ] ; then
    cd $_gitname && git pull origin
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting make..."

  rm -rf "$srcdir/$_gitname-build"
  git clone "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"
  python2 setup.py install --root="$pkgdir/" --optimize=1
}

# vim:set ts=2 sw=2 et:
