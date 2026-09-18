# Old Windows games on Linux: first setup

For the Windows 3.1 edition of **Cosmology of Kyoto**, start by trying DOSBox-X with Windows 3.1 installed inside it. **Eastern Mind: The Lost Souls of Tong-Nou** also has a 16-bit Windows edition. A game marked “Windows” is not necessarily aimed at modern Windows.

DOSBox-X is the emulator, Windows 3.1 is the guest environment, and the game runs inside Windows. The emulator does not include the operating system or game. Use your own installation media. These are suggested routes, not a claim that the supplied game files have been tested here.

## Choose a route

| Target | Suggested starting point |
| --- | --- |
| Windows 3.1-era CD-ROM game | DOSBox-X + Windows 3.1 |
| Broader retro Windows machine / Windows 95–98 | 86Box with period hardware and drivers |
| General-purpose VM experiment | QEMU; select legacy hardware deliberately |
| LSD: Dream Emulator | DuckStation, because this is a PlayStation game |

GNOME Boxes uses QEMU through virtualization infrastructure. Boxes is convenient for conventional VMs, but its streamlined interface is less suited to tuning old video cards, sound cards, and other period hardware. QEMU is possible; DOSBox-X is my first choice for this particular Windows 3.1 task. 86Box is a good alternative if you want to build a virtual vintage PC.

## Suggested first milestone

Get one reusable Windows 3.1 environment displaying correctly and playing sound, before trying several games.

1. Install the Linux build of DOSBox-X using the project's instructions for your distribution.
2. Follow its Windows 3.1x installation guide using a dedicated host folder, not your home directory as a whole.
3. Install the appropriate display and sound drivers. The official guide recommends its S3 display path; begin with basic VGA during Windows installation.
4. Mount the game CD image before starting Windows. DOSBox-X documents limitations when adding a CD drive after Windows has started.
5. Run the game's installer inside Windows. Install the runtime version it asks for if required (some games use period multimedia components).
6. Verify music, speech, saving, and loading. Shut down the emulator and back up the working folder/configuration.
7. Record a short session and check the captured audio before making a long recording.

Keep the original image files separate from writable Windows files and saves. Exact configuration depends on whether your copy is an original ISO, a folder of installed files, a Macintosh release, or a repack already carrying an emulator. An exact launch command should be based on those files.

If a package contains `dosbox.exe` and a `.conf` file, that executable is the Windows build of the emulator. Linux can use its native emulator and an adapted configuration; Windows drive paths in the configuration need attention. A Macintosh-only disc requires a Macintosh environment, not Windows merely because both versions of the game exist.

## References

- [DOSBox-X Windows 3.1x installation guide](https://dosbox-x.com/wiki/Guide:Installing-Windows-3.1x)
- [86Box overview and downloads](https://86box.net/)
- [GNOME Boxes technology](https://help.gnome.org/gnome-boxes/supported-protocols.html)
- [QEMU x86 system emulation](https://www.qemu.org/docs/master/system/target-i386.html)
- [DuckStation project and Linux instructions](https://github.com/stenzek/duckstation)
- [Osamu Sato's site](https://www.osamusato.net/)

This guide is outside the public notes directory and is not included in the generated website.
