from django.core.management.base import BaseCommand
from .scrape import scrape
from courtlist.models import Cases, CourtHearings, HearingCases, Courts


class Command(BaseCommand):
    help = 'Import data by scraping the kenya law website'
    link = 'http://www.kenyalaw.org/kl/index.php?id=1648'

    def handle(self, *args, **kwargs):
        sessions = scrape(self.link)
        self.stdout.write(
            self.style.SUCCESS('Data pulled from website.\nStarting DB writes')
        )
        courts_added = 0
        court_hearing_added = 0
        cases_added = 0
        hearing_added = 0

        for session in sessions:
            # create court
            court_number = session['court']

            if session['court'] is not None and court_number.isdecimal():
                court_number = int(court_number)
                court, court_created = Courts.objects.get_or_create(
                    name='Court %s' % court_number,
                    number=court_number
                )
                court_id = court.id
                courts_added += 1 if court_created else 0
            else:
                court_id = None

            # create court hearing
            judge = (session['judge'] or '').strip()
            court_hearing, court_hearing_created = CourtHearings.objects.get_or_create(
                judge=judge,
                court_id=court_id,
                date=session['date'],
                start_time=session['start_time'],
            )
            court_hearing_added += 1 if court_hearing_created else 0

            for case_type, cases in session['cases'].items():
                for case in cases:
                    # create case
                    saved_case, case_created = Cases.objects.get_or_create(
                        case_id=case['case_number'],
                        plaintiff=case['plaintiff'],
                        defendant=case['defendant']
                    )
                    # create case hearing
                    _, hear_created = HearingCases.objects.get_or_create(
                        position=case['case_position'],
                        hearing_type=case_type,
                        hearing=court_hearing,
                        case=saved_case
                    )
                    cases_added += 1 if case_created else 0
                    hearing_added += 1 if case_created else 0
        self.stdout.write(
            self.style.SUCCESS('%s Cases Added\n%s Case Hearings Added' % (cases_added, hearing_added))
        )
        self.stdout.write(
            self.style.SUCCESS('%s Courts Added\n%s Court Hearings Added' % (courts_added, court_hearing_added))
        )
