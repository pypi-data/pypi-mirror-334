-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (quilt)
Source: abseil
Binary: libabsl-dev, libabsl20220623t64
Architecture: any
Version: 20220623.1-3.1ubuntu3
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Homepage: https://abseil.io/
Description: extensions to the C++ standard library
 Abseil is an open-source collection of C++ library code designed to augment the
 C++ standard library. The Abseil library code is collected from Google's C++
 codebase and has been extensively tested and used in production. In some cases,
 Abseil provides pieces missing from the C++ standard; in others, Abseil
 provides alternatives to the standard for special needs.
Standards-Version: 4.6.1
Vcs-Browser: https://salsa.debian.org/debian/abseil
Vcs-Git: https://salsa.debian.org/debian/abseil.git
Testsuite: autopkgtest
Testsuite-Triggers: cmake, g++, libgtest-dev, make, pkg-config
Build-Depends: dpkg-dev (>= 1.22.5), cmake (>= 3.5), debhelper-compat (= 12), g++-12, googletest (>= 1.12) [!mipsel !ppc64] <!nocheck>
Package-List:
 libabsl-dev deb libdevel optional arch=any
 libabsl20220623t64 deb libs optional arch=any
Checksums-Sha1:
 60f52f4d90cebd82fc77dae1119590ef96e01ed5 1957272 abseil_20220623.1.orig.tar.gz
 fd95bd8e6fa7168f7f82f4a1a367243666045b49 8412 abseil_20220623.1-3.1ubuntu3.debian.tar.xz
Checksums-Sha256:
 abfe2897f3a30edaa74bc34365afe3c2a3cd012091a97dc7e008f7016adcd5fe 1957272 abseil_20220623.1.orig.tar.gz
 9d427fae687587f47ff6b3e9d83d396300463572e0af342129a9498a1ed82284 8412 abseil_20220623.1-3.1ubuntu3.debian.tar.xz
Files:
 3c40838276f6e5f67acf9a3e5a5e0bd1 1957272 abseil_20220623.1.orig.tar.gz
 1a5a4d628664aea1355429fc76e683e9 8412 abseil_20220623.1-3.1ubuntu3.debian.tar.xz
Original-Maintainer: Benjamin Barenblat <bbaren@debian.org>

-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEEVovyKmYzfL/Jprm3LIPbyOm9DjcFAmYMcKQACgkQLIPbyOm9
DjcSzw/8Dmo8fsi7UNXQjVMGUr4fgB8un5mM0OT7T5osgWU1X7OdUP1Clk4xExXy
9SAA5W1urG9ETAjJ1yULw3GhyAodOsRdByGRu0Wz7zLmWGiDMVCdnw+Q7KJ6T3Jb
zIV/SsW9/uavL3bj2279tkZWH82HVl4ZanmKunaVQKsRVVajvlrCjazEpSBSLUUn
YCfzWfKf7JddLdXOSfBia2BVay05acxIT6ushkjWSqC6QxKlv34snTFZp30dPTrJ
xiTIGSxFqpOGsgVThCFFT2hFDF4ZbaUjyZN8dbHAENYh9hYm1+isKfO83ZsUzKfE
K6jQ+UAGdBrIlcRG9G5j2wQ51lV9J0N2QuVZXpTbEV8LJjFnKkcJDx+hBsw4O0Aq
ovD8Ow5BQ9ZxA+1ng04SXuK13VLS7v4B0vxUjoIEgegbbVB5OA4rd7AEykHeuJ7g
nCqcaSQYdPliwUroHZY5jsq0EL3s0uAMxRrOUeEneBSi3tB3eXiOCoRd7vlik9tN
KcmcNW/pPxJuuwCa6Uptg19I9s3eESRV+hpbovuWGS34T/IPkXdmod4QHXdJ1Tti
VU31c4Vs0koPWVZKPfR9KNmE2jLJ7n2ZH92FZ/UmzATvMcLXw1reaBG2k9E9DvFG
25IVXRfjvm2whVshXXgdYE6tBSxW9SRzz/SNdDjpxy0ZdXl4D4I=
=hAK6
-----END PGP SIGNATURE-----
