# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section   free

Name:           velocity-dvsl
Version:        1.0
Release:        %mkrel 1.0.1
Epoch:          0
Summary:        DVSL Declarative Velocity Style Language

Group:          Development/Java
License:        Apache Software License
URL:            http://velocity.apache.org/dvsl/releases/dvsl-1.0/
Source0:        http://www.apache.org/dist/velocity/dvsl/1.0/velocity-dvsl-1.0-src.tar.gz
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml

Patch0:         %{name}-java2source.patch
Patch1:         %{name}-ant16.patch
Patch2:         %{name}-fix-pom_xml.patch
Patch3:         %{name}-site_xml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  crimson
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-lang
BuildRequires:  dom4j
BuildRequires:  jakarta-oro
BuildRequires:  jaxen >= 0:1.1
BuildRequires:  velocity >= 0:1.5
BuildRequires:  xalan-j2
BuildRequires:  xml-commons-jaxp-1.3-apis
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven-surefire-plugin
#BuildRequires:  mojo-maven2-plugin-taglist
BuildRequires:  maven2-default-skin
%endif

Requires:  ant
Requires:  jakarta-commons-collections
Requires:  jakarta-commons-lang
Requires:  dom4j
Requires:  jakarta-oro
Requires:  jaxen >= 0:1.1
Requires:  velocity >= 0:1.5
Requires:  xalan-j2
Requires:  jaxp_parser_impl
Requires:  xml-commons-jaxp-1.3-apis

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
DVSL (Declarative Velocity Style Language) is a tool modeled 
after XSLT and is intended for general XML transformations 
using the Velocity Template Language as the templating language 
for the transformations. The key differences are that it 
incorporates easy access to Java objects and allows you to use 
the Velocity template language and it's features for expressing 
the transformation templates. 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%if 0
%package        manual
Summary:        Documents for %{name}
Group:          Development/Java

%description    manual
%{summary}.
%endif

%package        demo
Summary:        Examples for %{name}
Group:          Development/Documentation
Requires:       velocity-dvsl = 0:%{version}-%{release}

%description    demo
%{summary}.

%prep
%setup -q -n %{name}-%{version}-src
find . -name "*.jar" -exec rm {} \;
cp %{SOURCE1} settings.xml

%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav
%patch3 -b .sav

%if %{with_maven}
mkdir -p target/classes/org/apache/dvsl/resource/
cp src/java/org/apache/dvsl/resource/defaultroot.dvsl \
         target/classes/org/apache/dvsl/resource/
rm src/test/org/apache/dvsl/GrinderTest.java


%else
mkdir lib
(cd lib
ln -sf $(build-classpath ant)
ln -sf $(build-classpath commons-collections)
ln -sf $(build-classpath commons-lang)
ln -sf $(build-classpath crimson)
ln -sf $(build-classpath dom4j)
ln -sf $(build-classpath jaxen)
ln -sf $(build-classpath junit)
ln -sf $(build-classpath oro)
ln -sf $(build-classpath velocity)
ln -sf $(build-classpath xalan-j2)
#ln -sf $(build-classpath xerces-j2)
ln -sf $(build-classpath xml-commons-jaxp-1.3-apis)
ln -s $(find-jar xml-commons-apis)
#commons-collections-3.2.jar
#commons-lang-2.3.jar
#crimson-1.1.3.jar
#dom4j-1.6.1.jar
#jaxen-1.1.1.jar
#junit-4.3.1.jar
#oro-2.0.8.jar
#velocity-1.5.jar
#xalan-2.7.0.jar
)
%endif

%build
%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc
%else

%ant -Dskip.jar.loading=true \
    -Dcompile.source=1.4 \
    -Dcompile.target=1.4 \
    all

%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
%if %{with_maven}
install -m 644 target/dvsl-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%else
install -m 644 dist/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%endif
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -pr target/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 


# manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%if 0
%if %{with_maven}
rm -rf target/site/apidocs
cp -pr target/site/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%else
cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%endif
%endif
cp LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# demo
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/*.jar
%doc %{_docdir}/%{name}-%{version}/LICENSE
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%if 0
%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%endif

%files demo
%defattr(-,root,root,-)
%doc %{_datadir}/%{name}-%{version}
