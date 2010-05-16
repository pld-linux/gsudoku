Summary:	A sudoku solver and generator
Summary(pl.UTF-8):	Program do tworzenia i rozwiązywania sudoku
Name:		gsudoku
Version:	02
Release:	1
License:	GPL v2
Group:		X11/Applications/Games
Source0:	http://www.yzonesoft.com/gsudoku/files/%{name}_%{version}_source.zip
# Source0-md5:	d0f2ef4ec3089c0dcb435ee1cb31bd3a
Source1:	%{name}.desktop
Patch0:		%{name}-paths.patch
URL:		http://www.yzonesoft.com/gsudoku/gsudoku.html
BuildRequires:	gtk+2-devel >= 2.4
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A sudoku solver and generator.

%description -l pl.UTF-8
Program do tworzenia i rozwiązywania sudoku.

%prep
%setup -q -n %{name}_%{version}_source
%patch0 -p1

find . -name '*~' -print0 | xargs -0 -r -l512 rm -f
cd manual
mv FONT_TAB.GIF font_tab.gif
mv GAME_TAB.GIF game_tab.gif
mv GEN_TAB.GIF gen_tab.gif
mv LINE.PNG line.png
mv MAIN.CSS main.css
mv PREF_TAB.GIF pref_tab.gif
mv SIZE_TAB.GIF size_tab.gif
mv SOL_TAB.GIF sol_tab.gif
mv XWING.GIF xwing.gif
cd ..

# i know its ugly, but may be easier to upgrade then patch
sed -i "s#icons/#%{_datadir}/%{name}/icons/#g" gsudoku.c
sed -i "s#icons/#%{_datadir}/%{name}/icons/#g" menu.c
sed -i "s#icons/#%{_datadir}/%{name}/icons/#g" settings.c
sed -i "s#images/#%{_datadir}/%{name}/images/#g" gsudoku.c
sed -i "s#images/#%{_datadir}/%{name}/images/#g" help_about.c
sed -i "s#manual/#%{_docdir}/%{name}-%{version}/manual/#g" help_about.c
sed -i "s#manual/#%{_docdir}/%{name}-%{version}/manual/#g" settings.c
# comment all chdir() calls, those dirs does not exist anyway
# and only ("..") calls takes effect
sed -i "s#chdir(#//chdir(#g" gsignal.c
sed -i "s#chdir(#//chdir(#g" gsudoku.c
sed -i "s#chdir(#//chdir(#g" other.c
# dont add path to any help call
sed -i "s#strcat(str,path)#//strcat(str,path)#g" help_about.c

%build
# not my fault, there is no Makefile
%{__cc} -DLINUX gsudoku.c generator_solver.c menu.c settings.c gsignal.c \
	da_interactive.c da_drawing.c other.c help_about.c -o gsudoku \
	`pkg-config --cflags --libs gtk+-2.0 gthread-2.0` %{rpmcflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{icons,images}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install gsudoku $RPM_BUILD_ROOT%{_bindir}
install icons/*.png $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
install images/* $RPM_BUILD_ROOT%{_datadir}/%{name}/images

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install icons/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/gsudoku.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.TXT Release_notes.txt manual
%attr(755,root,root) %{_bindir}/gsudoku
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
