#! /bin/sh

# Install /usr/bin wrapper for SCLized executable.
# Copyright (C) 2017 Red Hat, Inc.
# Written by Pavel Raiskup <praiskup@redhat.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

die() { echo >&1 "$*" ; exit 1 ; }

test -n "$BUILDROOT" \
    || die "this script can not be used directly, use macros from @MACROS@ in your package"

set -e

ARGS=$(getopt -o "n:m:" -l "" -n "getopt" -- "$@") || exit 1
eval set -- "$ARGS"

while true; do
    case $1 in
    -n|-m)
        opt=${1##--}
        opt=${opt##-}
        opt=${opt//-/_}
        eval "opt_$opt=\$2"
        shift 2
        ;;
    --) shift ; break ;; # end
    *) echo "programmer mistake ($1)" >&2; exit 1 ;;
    esac
done

src="$1"          ; shift
dst="$1"          ; shift

executable="$(basename "$dst")"
wrapper="$BUILDROOT$dst"

mkdir -p "$(dirname "$wrapper")"

case $opt_m in
script)
    cat <<EOF > "$wrapper"
#! /bin/sh

# Just a convenience script for running '$executable' from '$SCL'
# collection, without the need to call 'scl enable $SCL'.  Note that
# it is not a bug when this script causes RPM collision with some
# '$dst' executable installed from different package.
#
# Generated by @GENERATOR@.

source scl_source enable $SCL
exec "$src" "\$@"
EOF
    chmod 755 "$wrapper"
    ;;

link)
    ln -s "$src" "$wrapper"
esac

echo "$dst" >> "$BUILD/$opt_n".lst
