# Introduction

beadroll is a command line interface created for the purpose of ...
I wanna just leave it there. Here you go. Figure it out yourself. lol.

No. beadroll, at least in the webster dictionary is defined as,
<div style="color: teal;">
    Beadroll \Bead"roll\, n. (R. C. Ch.)
     A catalogue of persons, for the rest of whose souls a certain
     number of prayers are to be said or counted off on the beads
     of a chaplet; hence, a catalogue in general.
     [1913 Webster]
</div>.



           On Fame's eternal beadroll worthy to be filed.
                                                    --Spenser.
     [1913 Webster]

---

Beadroll was designed for the simplification of generation of calendar files.

The design itself is quite simple. Using setuptools, click, and pickle I developed a 
command line interface that saves, and manipulates a database using pickle. 
In the database you can store multiple event dictionaries that the module ics uses
to create ics files. This can be done by using the subcommand `create`. 

With that being said there are some general features that I attempted to include.
Inside the python script itself, I attempted to leave room for expansion. 
This can be seen in that the click subcommands have many options that aren't hardcoded
to do anything as of yet. Instead they are left blank and the ics module packages them
as such within each individual event.

# Installation 

Clone the repo, create a venv with `python -m venv rollenv `, source to
activate the environment with `source rollenv/bin/activate ` and use 
`pip install --editable . ` once inside to install the dependencies. 
Voila, you have a working version of the binary inside the enviroment.

Next you can live in the environment or you can create a softlink, by executing
`ln -s rollenv/bin/beadroll /usr/local/bin/beadroll`

Alternatively you can add the `rollenv/bin/` dir to your path by
adding this line to your bashrc file.

```
export PATH="$HOME/path/to/repo/rollenv/bin":$PATH
``` 

now your free to enjoy the command line interface.


# Usage

Using beadroll involves, as of version 0.0.11, a bit of hand wrangling. Here is 
an overview. 

## show, crop, rm

There are 5 major subcommands for usage of beadroll. There are `add`, `create`, `crop`, `rm`,
and `show`. The add subcommand inserts events into the pickle database. As mentioned above
a lot of the subcommands have variables that haven't been developed, or actively developed as 
of yet.

You can use the `show` command dump the contents of the database events in a json format.
With the exception of `crop` and `rm` the other subcommands are standardized in their execution.

With `crop` the idea is that it works in a python splicing manner. That means that ':\<number\>'
will save indices 0 until, and including the number. Likewise the pattern '\<number\>:' will grab 
each number up to and including the final entry in the database of events.

While crop saves what is excluded for its selection, `rm` removes what is selected, while using
the same pattern as above. Technically both subcommands should also support the use of the pattern
'\<number\>:\<number\>' to select a range between and including each number.

## add, create

Although I intend on adding more features, that will be in the distance future, so for the time being
here is catalogue of feature for the `add` subcommand. 

beadroll supports adding alarms to the events to notify you of upcoming events, and since this is 
supported in the ics module I've attached a string interpreter that will allow you to add alarms
to upcoming events. 

Here is an example of the add subcommand:

```
beadroll add --alarms="alarm=last minute, trigger=-1m, summary=get ready, alarm=five minutes, trigger=-5m, summary=steady time, alarm=feeder, trigger=-15m, summary=start preparations, alarm=soul, trigger=-30m, summary=preparations" \
"Chess Club Meeting" \
"2023-10-15T15:45:00-04:00" \
"2023-10-15T16:45:00-04:00"
```

the alarms string is delimited by the ', ' character and supports adding as many alarms as you feel is necessary so that you can get
out of bed for your cousin's wedding, or if it's June 21 1988 in Hinamizawa prepare for the worse!

Each alarm in the string is comprised of three components: alarm, trigger and summary. These will be displayed when the 
events are loaded into whatever calendar application you are using. Naturally because the characters ', ' are used as
a delimiter there is, not as of yet, no other way to input the alarms into each event. 

The string handler has a special function to parse the trigger variable, as such the last character in the string delineates the interpretation
into one of either hours, minutes, days or seconds.

These options are delineated within the function 'parse_alarms' which is in the 'main.py', and are dependent on python datetime module.
In this manner you can specify when the alarm will sound by altering the trigger variable where 0 is the occurance of the event.
Therefore a '-24h' trigger would give you a 24 hours heads up about the dreadfull awful Hinamizawa incidence. Likewise a short notice
alarm would have the trigger set with a smaller nominal, such as '-30m'.

The `add` subcommand then takes three arguments, one for each essential requisite: the event, the beginning of the event, and the end of the 
event. Above I've made the event a simple day at work, with multiple alarms to feed your cat, wash your soul, and make preparations.

It should be noted that the last two args, the beginning and end of the event, are to be made in ISO 8601 date times. As you can see
from above this doesn't allow much flexibility in terms of error. The end cannot be before the beginning of the event,
or it will not be added to the dataset.

finally, the `create` subcommand exports the dataset into a ics file. you will need to give the filname with its appropriate extension.

```
beadroll create school_club_events.ics
```

## Doc files for generating manpages

after tickering with the `setup.py` today, 2023-12-19, I'm including this advice.
If you can't get the command `man beadroll` functioning, use `manpath` to locate the
directories that contain your manpages and copy the `beadroll.1` file into that path.

```
cp -vi docs/man/beadroll.1 /usr/local/share/man/man1
```

the `beadroll.1` file was created using `pod2man` command for rendering markdown, or
semi markdown into toff typesetting language.

 
