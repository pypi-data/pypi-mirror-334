# ElonaPlusCustom-GX Installer script for Windows

  
A Installer to download and setup ElonaPlusCustom-GX on Windows.


New Repo: **[JianmengYu](https://github.com/JianmengYu/ElonaPlusCustom-GX)** Current Repo based. <br>

Please visit **[Ruin0x11](https://github.com/Ruin0x11/ElonaPlusCustom-GX)**'s Previous Archived Repo


### Learn about the game:

**[Ylvania](https://ylvania.org/elona_e.html)**: Official Site.
**[Fandom Wiki](https://elona.fandom.com/wiki/Elona_Wiki)**: Game Wiki 

### Need to Know:
You may receive a false positive from Windows Defender
Please review the github issue: **[here](https://github.com/Ruin0x11/ElonaPlusCustom-GX/issues/103)** for more information.


 - In this case just disable __Windows Defender__ or other Anti-Virus prior to installing and re-enable after its finished installing.

# Version:

Current Installer Version: **v0.1.20**<br>

Current Game Version: **Elona+ 2.26**<br>

Current Custom-GX Version: **2.26.1.0**<br>



# Result:

  ##### Installation is placed in your %APPDATA% folder.

- Package will install Elona+ along with Custom-GX Mod

- Create a Desktop Shortcut for Quick Access.

- Create a Start Menu Option (Allows app to be searchable in Windows Search)



# Installation:

```
pip install elonadl

python elonadl
```



# Updates:

If you see a newer release to a newer version of Elona+ just rerun `python elona` it'll automatically create a new install for the latest version and not touch your older install.



## Install stragiht from .whl or tar.gz packages

```
pip install elonadl-<VERSION>-py3-none-any.whl
```
or <br>
```
py -m pip install elonadl-<VERSION>.tar.gz
```

To run the module just run the following command. _**Whenever there is a new update for Custom-GX simply rerun this command and it'll update your installation.**_


```
py -m elonadl
```

The game will be setup in your current user's **%APPDATA%** folder. (If run normally)

The game will be setup in the system's **%APPDATA%** folder. (if run as admin)

The script will inform you of the steps in the command line.



# How to Remove Package.

This won't impact the Elona+CGX setup, just remove the elonadl package from your computer.

```
pip uninstall elonadl
```
or <br>
```
py -m pip uninstall elonadl
```