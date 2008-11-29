%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define alpha 1

Name:           python-lxml
Version:        2.2
Release:        0.3.alpha%{alpha}%{?dist}
Summary:        ElementTree-like Python bindings for libxml2 and libxslt

Group:          Development/Libraries
License:        BSD
URL:            http://codespeak.net/lxml/
Source0:        http://cheeseshop.python.org/packages/source/l/lxml/lxml-%{version}alpha%{alpha}.tar.gz
#Source0:        http://codespeak.net/lxml/lxml-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxslt-devel

%if 0%{?fedora} >= 8
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

%description
lxml provides a Python binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.

%prep
%setup -q -n lxml-%{version}alpha%{alpha}

chmod a-x doc/rest2html.py

%build
CFLAGS="%{optflags}" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
rm -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt doc/
%{python_sitearch}/*

%changelog
* Fri Nov 28 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.3.alpha1
- Rebuild for Python 2.6

* Mon Nov 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.2.alpha1
- Don't forget to upload the sources!

* Mon Nov 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.1.alpha1
- 2.2alpha1 (2008-11-23)
- Features added
- 
-    * Support for XSLT result tree fragments in XPath/XSLT extension
-      functions.
-    * QName objects have new properties namespace and localname.
-    * New options for exclusive C14N and C14N without comments.
-    * Instantiating a custom Element classes creates a new Element.
- 
- Bugs fixed
- 
-    * XSLT didn't inherit the parse options of the input document.
-    * 0-bytes could slip through the API when used inside of Unicode
-      strings.
-    * With lxml.html.clean.autolink, links with balanced parenthesis, that
-      end in a parenthesis, will be linked in their entirety (typical with
-      Wikipedia links).

* Mon Nov 17 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.3-1
- 2.1.3 (2008-11-17)
- Bugs fixed
- 
-    * Ref-count leaks when lxml enters a try-except statement while an
-      outside exception lives in sys.exc_*(). This was due to a problem
-      in Cython, not lxml itself.
-    * Parser Unicode decoding errors could get swallowed by other
-      exceptions.
-    * Name/import errors in some Python modules.
-    * Internal DTD subsets that did not specify a system or public ID
-      were not serialised and did not appear in the docinfo property
-      of ElementTrees.
-    * Fix a pre-Py3k warning when parsing from a gzip file in Py2.6.
-    * Test suite fixes for libxml2 2.7.
-    * Resolver.resolve_string() did not work for non-ASCII byte strings.
-    * Resolver.resolve_file() was broken.
-    * Overriding the parser encoding didn't work for many encodings.

* Fri Sep  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.2-1
- 2.1.2 (2008-09-05)
- Features added
- 
-    * lxml.etree now tries to find the absolute path name of files when
-      parsing from a file-like object. This helps custom resolvers when
-      resolving relative URLs, as lixbml2 can prepend them with the path of
-      the source document.
- 
- Bugs fixed
- 
-    * Memory problem when passing documents between threads.
-    * Target parser did not honour the recover option and raised an exception
-      instead of calling .close() on the target.

* Fri Jul 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.1-1
- Update to 2.1.1

* Fri Jun 20 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.7-1
- Update to 2.0.7
- Update download URL

* Sat May 31 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.6-1
- Update to 2.0.6

* Thu May  8 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.5-1
- Update to 2.0.5

* Wed Mar 26 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.3-1
- Update to 2.0.3

* Sat Feb 23 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.2-1
- Update to 2.0.2

* Tue Feb 19 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.1-1
- Update to 2.0.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.6-2
- Autorebuild for GCC 4.3

* Mon Nov  4 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.6-1
- Update to 1.3.6.

* Mon Oct 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.5-1
- Update to 1.3.5.

* Thu Aug 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.4-1
- Update to 1.3.4.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.3.3-3
- Rebuild for selinux ppc32 issue.

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.3-2
- BR python-setuptools-devel

* Mon Jul 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.3-1
- Update to 1.3.3

* Fri Jan 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.1.2-1
- Update to 1.1.2

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.3-3
- Rebuild for new Python

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 1.0.3-2
- Rebuild for FC6

* Thu Aug 17 2006 Shahms E. King <shahms@shahms.com> 1.0.3-1
- Update to new upstream version

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 1.0.2-2
- Include, don't ghost .pyo files per new guidelines

* Fri Jul 07 2006 Shahms E. King <shahms@shahms.com> 1.0.2-1
- Update to new upstream release

* Mon Jun 26 2006 Shahms E. King <shahms@shahms.com> 1.0.1-1
- Update to new upstream release

* Fri Jun 02 2006 Shahms E. King <shahms@shahms.com> 1.0-1
- Update to new upstream 1.0 release

* Wed Apr 26 2006 Shahms E. King <shahms@shahms.com> 0.9.1-3
- Add python-setuptools to BuildRequires
- Use dist tag

* Wed Apr 26 2006 Shahms E. King <shahms@shahms.com> 0.9.1-2
- Fix summary and description

* Tue Apr 18 2006 Shahms E. King <shahms@shahms.com> 0.9.1-1
- update the new upstream version
- remove Pyrex build req

* Tue Dec 13 2005 Shahms E. King <shahms@shahms.com> 0.8-1
- Initial package
