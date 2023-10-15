
from datetime import datetime
import re, sys, os, configparser
import click
import pickle
from ics import Calendar, Event, DisplayAlarm, alarm, component
from datetime import datetime, timedelta
from rich import print
import pretty_errors
current_script_path = os.path.abspath(__file__)
git_root = os.path.dirname(current_script_path)
global config_file_path
config_file_path = os.path.join(git_root, 'lib', 'config.ini')
global config
config = configparser.ConfigParser()
config.read(os.path.abspath(config_file_path))
repoconfig = os.path.join(git_root, 'lib', 'gingerbeer.db')
class EventManager:
    def __init__(self, picklefile):
        self.picklefile = picklefile
        self.events = []
        self.alarms = []
        self.manager = {
                'events': self.events,
                'alarms': self.alarms
                }
    def save_to_pickle(self, event_dict):
        """
        saves entire completed dictionary events to the dictiioanry storage medium 'manager'.
        all dicitionaries should be complete before adding them to this list of event dictionaries.
        """
        try:
            self.manager['events'].append(event_dict)
            print("Appending done, here is new dictionary:", self.manager)
        except Exception as e:
            print("Something went wrong appending event dictionary to self.manager['events']", str(e)) 

        with open(self.picklefile, 'wb') as f:
            pickle.dump(self.manager, f)

    def load_from_pickle(self, debug=True):
        """
        loads from pickle
        """
        try:
            with open(self.picklefile, 'rb') as f:
                self.manager = pickle.load(f)
                if debug:
                    print("[blue]Loaded manager dictionary from the pickle: [/blue]", self.manager)
                return self.manager
        except Exception as e:
            print("Something went wrong, ", str(e))

    def save_to_calendar(self, filename):
        """
        save_to_calendar creates a calendar, opens the dictionary containing dictionaries of events,
        and adds those dictionaries to the calendar. All said and done, it saves it to a file.
        """
        c = Calendar()
        for event_dict in self.manager['events']:
            event = Event(
                name=event_dict.get('name'),
                begin=event_dict.get('begin'),
                end=event_dict.get('end'),
                duration=event_dict.get('duration'),
                uid=event_dict.get('uid'),
                description=event_dict.get('description'),
                created=event_dict.get('created'),
                last_modified=event_dict.get('last_modified'),
                location=event_dict.get('location'),
                url=event_dict.get('url'),
                transparent=event_dict.get('transparent'),
                alarms=event_dict.get('alarms'),
                attendees=event_dict.get('attendees'),
                categories=event_dict.get('categories'),
                status=event_dict.get('status'),
                organizer=event_dict.get('organizer'),
                geo=event_dict.get('geo'),
                classification=event_dict.get('classification')
            )
            c.events.add(event)

        with open(filename, 'w') as f:
            f.writelines(c)

    def validate_datetime_string(self, datetime_str):
        try:
            datetime_obj = datetime.fromisoformat(datetime_str)
            if datetime_obj.tzinfo is None:
                print("Warning: No timezone stamp found in the datetime string.")
        except ValueError:
            print("Error: Invalid datetime string.")



    def add_alarm(self, alarm):
        self.alarms.append(alarm)


    def parse_alarms(self, click_option, debug=False, dry_run=False):
        """
        parse_alarms will take a string written in format "alarm=value, trigger=<neg-number><[hmds]>, summary=value"
        and convert it into alarms that ics module will take. The string can include as many alarms as you like.
        each alarm will need a header "alarm=value" to initalize the alarm.
        the alarms are returned in a dictionary and will need to be extracted from that diciotnary when you go
        to add them to the event itself.
        """
        print(click_option)
        alarms = []
        alarm_pattern = r"alarm=(.*?)((?=, alarm=)|$)"
        alarm_matches = re.findall(alarm_pattern, click_option)
        alrmd = {}
        print("The length of the matching patterns is:", len(alarm_matches))
        for x in alarm_matches:
            print("x = ", x)
            alarm_string = x[0]
            print("alarm string:", alarm_string)
            parts = alarm_string.strip().split(", ")
            header = str(parts[0]).replace(" ", "_")
            alrmd[header] = DisplayAlarm()
            print("alarm_instance:", str(parts[0]).replace(" ", "_"))
            trigger = None
            summary = None
            
            for part in parts:
                if part.startswith("trigger="):
                    trigger = part.replace("trigger=", "").strip()
                elif part.startswith("summary="):
                    summary = part.replace("summary=", "").strip()
            
            if trigger and summary:
                print('trigger: ', trigger)
                print('summary: ', summary)
                trigger_value, trigger_unit = self.extract_trigger_value_unit(trigger)
                
                if trigger_unit == 'h':
                    timedelta_value = timedelta(hours=trigger_value)
                elif trigger_unit == 'm':
                    timedelta_value = timedelta(minutes=trigger_value)
                elif trigger_unit == 'd':
                    timedelta_value = timedelta(days=trigger_value)
                elif trigger_unit == 's':
                    timedelta_value = timedelta(seconds=trigger_value)
                else:
                    raise ValueError("Invalid trigger unit")
                
                alarm_time = datetime.utcnow() - timedelta_value
                alrmd[header].trigger = timedelta_value
                alrmd[header].summary = summary
                print("[blue]attributes:[/blue] \n", (timedelta_value, summary))
                print("[blue]alarm dictionary: [/blue]\n\n", alrmd[header])
            print("now the complete dictionary looks as such :\n", alrmd)
        if not dry_run:
            return alrmd
        else:
            sys.exit()

    def extract_trigger_value_unit(self, trigger):
        if trigger.endswith("h"):
            trigger_unit = 'h'
            trigger_value = int(trigger[:-1])
        elif trigger.endswith("m"):
            trigger_unit = 'm'
            trigger_value = int(trigger[:-1])
        elif trigger.endswith("d"):
            trigger_unit = 'd'
            trigger_value = int(trigger[:-1])
        elif trigger.endswith("s"):
            trigger_unit = 's'
            trigger_value = int(trigger[:-1])
        else:
            raise ValueError("Invalid trigger format")
        return trigger_value, trigger_unit

    def check_pickle_file(self, picklefile, debug=True):
        """TODO: Docstring for check_pickle_file.

        :picklefile: TODO
        :returns: TODO

        """
        if not os.path.exists(picklefile):
            # Prompt the user to create the pickle file
            create_file = input("Pickle file doesn't exist. Do you want to create it? (yes/no): ")
            if create_file.lower() == 'yes':
                # Create the pickle file or perform any desired actions
                with open(picklefile, 'wb') as f:
                    # Perform any necessary operations on the file
                    pass
            else:
                # Handle the case where the user doesn't want to create the pickle file
                pass
        else:
            if debug:
                print("[blue]Pickle file exists[/blue]")


@click.group()
def cli():
    pass

@cli.command()
@click.argument('name', type=str)
@click.argument('begin', type=str)
@click.argument('end', type=str)
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--duration', type=str, default=None)
@click.option('--uid', type=str, default=None)
@click.option('--description', type=str, default=None)
@click.option('--created', type=str, default=None)
@click.option('--last_modified', type=str, default=None)
@click.option('--location', type=str, default=None)
@click.option('--url', type=str, default=None)
@click.option('--transparent', type=bool, default=None)
@click.option('--alarms', type=str, default=None, help="Read docstring")
@click.option('--attendees', type=list, default=None)
@click.option('--categories', type=list, default=None)
@click.option('--status', type=str, default=None)
@click.option('--organizer', type=str, default=None)
@click.option('--geo', type=tuple, default=None)
@click.option('--classification', type=str, default=None)
def add(picklefile, name, begin, end, duration, uid, description, created, last_modified, location,
        url, transparent, alarms, attendees, categories, status, organizer, geo, classification):
    manager = EventManager(picklefile)
    manager.check_pickle_file(picklefile)
    manager.validate_datetime_string(begin)
    manager.validate_datetime_string(end)
    try:
        manager.load_from_pickle(debug=False)
    except Exception as e:
        print("raised exception")
        print("An error occured, ", str(e))
    event_dict = {
        'name': name,
        'begin': begin,
        'end': end,
        'duration': duration,
        'uid': uid,
        'description': description,
        'created': created,
        'last_modified': last_modified,
        'location': location,
        'url': url,
        'transparent': transparent,
        'alarms': alarms,
        'attendees': attendees,
        'categories': categories,
        'status': status,
        'organizer': organizer,
        'geo': geo,
        'classification': classification
    }
    if alarms:
        event_dict['alarms'] = []
        alarmpress = manager.parse_alarms(alarms, debug=False, dry_run=False)
        for key, value in alarmpress.items():
            print(f"adding {value} to event, {event_dict['name']}.")
            event_dict['alarms'].append(value)

    manager.save_to_pickle(event_dict)

@cli.command()
@click.option('--picklefile', type=str, default=repoconfig)
def list(picklefile):
    """
    list the contents of pickle file
    """
    manager = EventManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    for event_dict in manager.events:
        print("Name:", event_dict.get('name'))
        print("Begin:", event_dict.get('begin'))
        print("End:", event_dict.get('end'))
    print(container)

@cli.command(context_settings={"ignore_unknown_options": True})
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--debug', is_flag=True)
@click.option('--verbose', is_flag=True)
@click.option('--dry', is_flag=True)
@click.argument('pointer', nargs=-1)
def rm(pointer, debug, verbose, dry, picklefile):
    """
    remove events from pickle
    """
    manager = EventManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    if verbose:
        print(container['events'][0])
    if debug:
        print("[blue]pointer is [/blue]", type(pointer))
        print(len(pointer))

    for tg in pointer:
        print("[blue]string in iteration is:[/blue] ", str(tg))

        if ':' in tg:
            start, end = tg.split(':')
            start = int(start) if start else None
            end = int(end) if end else None
            receiver = container['events'][start:end]
        else:
            receiver = container['events'][int(tg)]


    print(receiver)
    if dry:
        sys.exit()
    else:
        container['events'] = receiver
        manager.save_to_pickle(container)

@cli.command()
@click.argument('picklefile', type=str)
@click.argument('calendarfile', type=str)
def create_ics(picklefile, calendarfile):
    """
    save events to ics file
    """
    manager = EventManager(picklefile)
    manager.load_from_pickle()
    manager.save_to_calendar(calendarfile)
