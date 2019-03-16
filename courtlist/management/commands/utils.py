import re
from datetime import time
from dateutil.parser import parser


class Scrape:

    fields = {
        'case': {
            'regex': r'^(?P<case_position>\d+)\.? *(?P<case_number>[a-zA-Z]+'
                     r' ?/\d+/\d+) *(?P<plaintiff>Rep||[A-Za-z ]+)\.? *Vs\.? *(?P<defendant>'
                     r'[^\n]+)',
            'multiple': True,
            'cb': 'case_clean'
        },
        'date': {
            'regex': r'(?:(sunday|monday|tuesday|wednesday|thursday|friday|saturday), )?'
                     r'(?P<day>\d+)(?:..)? (?P<month>january|february|march|april|may|june'
                     r'|july|august|september|october|november|december) (?P<year>\d+)',
            'multiple': False,
            'cb': 'make_date'
        },
        'start_time': {
            'regex': '(?P<hour>\d+):(?P<minute>\d+) ?(?P<AMOrPM>[AP]M)?',
            'cb': 'make_time'
        },
        'title': {
            'regex': r'CAUSE LIST',
        },
        'case_type': {
            'regex': r'^(?P<type>MENTION|PART HEARD HEARING|SUBMISSIONS|RULING|FRESH HEARING|JUDGMENT|DEFENSE HEARING|'
                     r'SENTENCING|PRE TRIAL CONFERENCE|PLEA|SUBMISSION|HEARING|HEARING- MAIN SUIT)$'
        },
        'judge': {
            'regex': r'(HON|D).? (?P<name>[ A-Za-z\.]+).*(?:COURT ?)?(?P<court>\d+)?.*?'
        },
        'junk': {
            'regex': 'MILIMANI MAGISTRATE COURT|MAGISTRATE COURT CRIMINAL'
        }
    }

    def __init__(self, content):
        self.content = content
        self.valid = False
        self.line_data = {i: None for i, con in enumerate(content)}
        self.final_data = {}
        self.get_data()
        self.aggregate()

    def case_clean(self, case_match):
        case_dict = case_match.groupdict()
        case_dict['case_position'] = int(case_dict['case_position'])
        if 'plaintiff' not in case_dict:
            case_dict['plaintiff'] = 'Rep'
        return case_dict

    def make_date(self, date_match):
        # print(date_match.string)
        date_dict = date_match.groupdict()
        date = ' '.join(date_dict.values()).title()
        date = parser().parse(date).date()
        return str(date)

    def make_time(self, time_match):
        time_dict = time_match.groupdict()
        if time_dict.get('AMOrPM', 'AM') == 'AM':
            time_dict['hour'] = int(time_dict['hour'])
        else:
            time_dict['hour'] = int(time_dict['hour']) + 12
        del time_dict['AMOrPM']
        time_dict['minute'] = int(time_dict['minute'])
        return str(time(**time_dict))

    def aggregate(self):
        fields = iter(self.line_data.items())
        field = next(fields, None)
        while field:
            field = field[1]
            if field is None:
                field = next(fields, None)
                continue
            elif field['field'] == 'judge':
                if 'name' in field['data']:
                    self.final_data['judge'] = field['data']['name']
                if 'court' in field['data']:
                    self.final_data['court'] = field['data']['court']
                field = next(fields, None)
            elif field['field'] == 'case_type':
                if 'type' in field['data']:
                    case_type = field['data']['type']
                    cases = []
                    field = next(fields, None)
                    if field is None:
                        continue
                    # print(field)
                    f = field[1]
                    while 'field' in f and f['field'] == 'case':
                        cases.append(f['data'])
                        field = next(fields, None)
                        if field is None:
                            break
                        f = field[1]
                    self.final_data.setdefault('cases', {}).update(**{case_type: cases})
            elif field['field'] == 'date':
                self.final_data['date'] = field['data']
                field = next(fields, None)
            elif field['field'] == 'start_time':
                self.final_data['start_time'] = field['data']
                field = next(fields, None)
            else:
                field = next(fields, None)

    def get_data(self):
        for i, line in enumerate(self.content):
            for field, block in self.fields.items():
                regex = block['regex']
                match = re.match(regex, line, re.IGNORECASE)
                if match:
                    if self.line_data[i]:
                        print(line)
                        raise Exception('Double Line Detection!!')
                    self.line_data[i] = {
                        'field': field,
                        'data': match.groupdict() if 'cb' not in block else getattr(self, block['cb'])(match)
                    }
                    break
            else:
                print(line)
                print("line :-(")
