%if 0%{?fedora} > 12 || 0%{?rhel} > 5
%global with_python3 1
%endif

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-lxml
Version:        2.2.8
Release:        1%{?dist}
Summary:        ElementTree-like Python bindings for libxml2 and libxslt

Group:          Development/Libraries
License:        BSD
URL:            http://codespeak.net/lxml/
Source0:        http://cheeseshop.python.org/packages/source/l/lxml/lxml-%{version}.tar.gz
Source1:        http://cheeseshop.python.org/packages/source/l/lxml/lxml-%{version}.tar.gz.asc

# Workaround for bug 600036: 2to3 chokes on certain lines
# Reported upstream against 2to3 as listed in that bug
Patch0:         python-lxml-2.2.6-fix-2to3.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxslt-devel

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  Cython >= 0.12

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools
%endif

%description
lxml provides a Python binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
%description docs
This package provides the documentation for %{name}, e.g. the API as html.


%if 0%{?with_python3}
%package -n python3-lxml
Summary:        ElementTree-like Python 3 bindings for libxml2 and libxslt
Group:          Development/Libraries

%description -n python3-lxml
lxml provides a Python 3 binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python 3 Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.
%endif

%prep
%setup -q -n lxml-%{version}

%patch0 -p1

# remove the C extension so that it will be rebuild using the latest Cython
rm -f src/lxml/lxml.etree.c
rm -f src/lxml/lxml.etree_api.h
rm -f src/lxml/lxml.objectify.c

chmod a-x doc/rest2html.py
%{__sed} -i 's/\r//' doc/s5/ui/default/print.css \
    doc/s5/ep2008/atom.rng \
    doc/s5/ui/default/iepngfix.htc

# FIXME: this is fixed in upstreams issue:
# http://bugs.python.org/issue7313
# Don't know when this is in a released python version.
# Always try to delete that part,
# when a new python version is released!!!
#
# src/lxml/tests/test_errors.py has a 3-byte Byte Order Marker, which seems to
# break both 2to3 and python3-2to3;
# However, it doesn't contain any non-ASCII characters, so for now, simply
# strip it from the top of the file:
pushd src/lxml/tests
    tail --bytes=+4 test_errors.py > test_errors.py.new
    mv test_errors.py.new test_errors.py
popd

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -r . %{py3dir}
2to3 --write --nobackup %{py3dir}
%endif

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
cp src/lxml/lxml.etree.c %{py3dir}/src/lxml
cp src/lxml/lxml.etree_api.h %{py3dir}/src/lxml
cp src/lxml/lxml.objectify.c %{py3dir}/src/lxml

pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --no-compile --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --no-compile --root %{buildroot}
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt
%{python_sitearch}/lxml
%{python_sitearch}/lxml-*.egg-info

%files docs
%defattr(-,root,root,-)
%doc doc/*

%if 0%{?with_python3}
%files -n python3-lxml
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt
%{python3_sitearch}/lxml-*.egg-info
%{python3_sitearch}/lxml
%endif

%changelog
* Mon Sep  6 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.8-1
- 2.2.8 (2010-09-02)
- Bugs fixed
-
-     * Crash in newer libxml2 versions when moving elements between
-       documents that had attributes on replaced XInclude nodes.
-     * Import fix for urljoin in Python 3.1+.

* Tue Aug 24 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.7-3
- Don't byte-compile files during install because setup.py doesn't
  properly byte compile for Python version 3.2

* Sun Aug 22 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.7-2
- Rebuild for Python 3.2

* Mon Jul 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.7-1
- 2.2.7 (2010-07-24)
- Bugs fixed
- 
-     * Crash in XSLT when generating text-only result documents with a stylesheet created in a different thread.

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.6-4
- actually add the patch this time

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.6-3
- workaround for 2to3 issue (patch 0; bug 600036)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  2 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.6-1
- 2.2.6 (2010-03-02)
- 
- Bugs fixed
- 
-    * Fixed several Python 3 regressions by building with Cython 0.11.3.

* Mon Mar  1 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.5-1
- 2.2.5 (2010-02-28)
- 
- Features added
- 
-    * Support for running XSLT extension elements on the input root node
-      (e.g. in a template matching on "/").
- 
- Bugs fixed
- 
-    * Crash in XPath evaluation when reading smart strings from a document
-      other than the original context document.
-    * Support recent versions of html5lib by not requiring its XHTMLParser
-      in htmlparser.py anymore.
-    * Manually instantiating the custom element classes in lxml.objectify
-      could crash.
-    * Invalid XML text characters were not rejected by the API when they
-      appeared in unicode strings directly after non-ASCII characters.
-    * lxml.html.open_http_urllib() did not work in Python 3.
-    * The functions strip_tags() and strip_elements() in lxml.etree did
-      not remove all occurrences of a tag in all cases.
-    * Crash in XSLT extension elements when the XSLT context node is not
-      an element.

* Mon Feb 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.2.4-2
- update to current python3 guidelines
- be more explicit in %%files
- use %%global and not %%define
- create docs subpackage
- add stripping 3-byte Byte Order Marker from src/lxml/tests/test_errors.py
  to get 2to3 to work (dmalcolm)
- fixes FTBFS (#564674)

* Thu Jan 14 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.4-1
- Update to 2.2.4
- Enable Python 3 subpackage

* Thu Nov  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-3
- F-13's python build chain must be a little different...

* Thu Nov  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-2
- Add option to build a Python 3 subpackage, original patch by David Malcolm

* Fri Oct 30 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-1
- 2.2.3 (2009-10-30)
- Bugs fixed
- 
-    * The resolve_entities option did not work in the incremental feed
-      parser.
-    * Looking up and deleting attributes without a namespace could hit a
-      namespaced attribute of the same name instead.
-    * Late errors during calls to SubElement() (e.g. attribute related
-      ones) could leave a partially initialised element in the tree.
-    * Modifying trees that contain parsed entity references could result
-      in an infinite loop.
-    * ObjectifiedElement.__setattr__ created an empty-string child element
-      when the attribute value was rejected as a non-unicode/non-ascii
-      string
-    * Syntax errors in lxml.cssselect could result in misleading error
-      messages.
-    * Invalid syntax in CSS expressions could lead to an infinite loop in
-      the parser of lxml.cssselect.
-    * CSS special character escapes were not properly handled in
-      lxml.cssselect.
-    * CSS Unicode escapes were not properly decoded in lxml.cssselect.
-    * Select options in HTML forms that had no explicit value attribute
-      were not handled correctly. The HTML standard dictates that their
-      value is defined by their text content. This is now supported by
-      lxml.html.
-    * XPath raised a TypeError when finding CDATA sections. This is now
-      fully supported.
-    * Calling help(lxml.objectify) didn't work at the prompt.
-    * The ElementMaker in lxml.objectify no longer defines the default
-      namespaces when annotation is disabled.
-    * Feed parser failed to honour the 'recover' option on parse errors.
-    * Diverting the error logging to Python's logging system was broken.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.2-1
- 2.2.2 (2009-06-21)
- Features added
- 
-    * New helper functions strip_attributes(), strip_elements(),
-      strip_tags() in lxml.etree to remove attributes/subtrees/tags
-      from a subtree.
- 
- Bugs fixed
- 
-    * Namespace cleanup on subtree insertions could result in missing
-      namespace declarations (and potentially crashes) if the element
-      defining a namespace was deleted and the namespace was not used
-      by the top element of the inserted subtree but only in deeper
-      subtrees.
-    * Raising an exception from a parser target callback didn't always
-      terminate the parser.
-    * Only {true, false, 1, 0} are accepted as the lexical representation
-      for BoolElement ({True, False, T, F, t, f} not any more), restoring
-      lxml <= 2.0 behaviour.

* Tue Jun  2 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.1-1
- 2.2.1 (2009-06-02)
- Features added
- 
-    * Injecting default attributes into a document during XML Schema
-      validation (also at parse time).
-    * Pass huge_tree parser option to disable parser security restrictions
-      imposed by libxml2 2.7.
- 
- Bugs fixed
- 
-    * The script for statically building libxml2 and libxslt didn't work
-      in Py3.
-    * XMLSchema() also passes invalid schema documents on to libxml2 for
-      parsing (which could lead to a crash before release 2.6.24).

* Tue Mar 24 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-1
- 2.2 (2009-03-21)
- Features added
- 
-    * Support for standalone flag in XML declaration through
-      tree.docinfo.standalone and by passing standalone=True/False on
-      serialisation.
- 
- Bugs fixed
- 
-    * Crash when parsing an XML Schema with external imports from a
-      filename.

* Fri Feb 27 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.8.beta4
- 2.2beta4 (2009-02-27)
- Features added
- 
-    * Support strings and instantiable Element classes as child arguments
-      to the constructor of custom Element classes.
-    * GZip compression support for serialisation to files and file-like
-      objects.
- 
- Bugs fixed
- 
-    * Deep-copying an ElementTree copied neither its sibling PIs and
-      comments nor its internal/external DTD subsets.
-    * Soupparser failed on broken attributes without values.
-    * Crash in XSLT when overwriting an already defined attribute using
-      xsl:attribute.
-    * Crash bug in exception handling code under Python 3. This was due to
-      a problem in Cython, not lxml itself.
-    * lxml.html.FormElement._name() failed for non top-level forms.
-    * TAG special attribute in constructor of custom Element classes was
-      evaluated incorrectly.
- 
- Other changes
- 
-    * Official support for Python 3.0.1.
-    * Element.findtext() now returns an empty string instead of None for
-      Elements without text content.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.7.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.6.beta3
- 2.2beta3 (2009-02-17)
- Features added
- 
-    * XSLT.strparam() class method to wrap quoted string parameters that
-     require escaping.
- 
- Bugs fixed
- 
-    * Memory leak in XPath evaluators.
-    * Crash when parsing indented XML in one thread and merging it with
-      other documents parsed in another thread.
-    * Setting the base attribute in lxml.objectify from a unicode string
-      failed.
-    * Fixes following changes in Python 3.0.1.
-    * Minor fixes for Python 3.
- 
- Other changes
- 
-    * The global error log (which is copied into the exception log) is now
-      local to a thread, which fixes some race conditions.
-    * More robust error handling on serialisation.

* Sun Jan 25 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.5.beta2
- 2.2beta2 (2009-01-25)
- Bugs fixed
- 
-    * Potential memory leak on exception handling. This was due to a
-      problem in Cython, not lxml itself.
-    * iter_links (and related link-rewriting functions) in lxml.html would
-      interpret CSS like url("link") incorrectly (treating the quotation
-      marks as part of the link).
-    * Failing import on systems that have an io module.

* Fri Dec 12 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.4.beta1
- 2.2beta1 (2008-12-12)
- Features added
- 
-    * Allow lxml.html.diff.htmldiff to accept Element objects,
-      not just HTML strings.
- 
- Bugs fixed
- 
-    * Crash when using an XPath evaluator in multiple threads.
-    * Fixed missing whitespace before Link:... in lxml.html.diff.
- 
- Other changes
- 
-    * Export lxml.html.parse.

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
