# Introduction

beadroll is a command line interface created for the purpose of ...

simplification of generation of calendar files.

Currently this is but a dream, however there is evidence that it is materializing.

# Doc files

after tickering with the `setup.py` today, 2023-12-19, I'm including this advice.
If you can't get the command `man beadroll` functioning, use `manpath` to locate the
directories that contain your manpages and copy the `beadroll.1` file into that path.

```
cp -vi docs/man/beadroll.1 /usr/local/share/man/man1
```

the `beadroll.1` file was created using `pod2man` command for rendering markdown, or
semi markdown into toff typesetting language.

 
