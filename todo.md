# JAGSS - ToDo list

## Add deployment tools via config file

- sFTP could use Paramiko
- s3 could use awscli
- git could use legit

in the config file, there would be fields for deployment type, username and password. Then a call like "jagss --deploy".

## get JAGSS submitted to PyPI

Once this gets to the level of a stable, user-friendly release, of course.

## Add multimedia metadata scanning

If image/audio files are in a directory, add their embedded metadata to the site dictionary

- mutagen for mp3 files
- iptcinfo for image files
