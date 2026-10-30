import time

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, close_old_connections

from chores.recurrence import reconcile_all


class Command(BaseCommand):
    help = "Generate due recurring work independently of browsers."

    def add_arguments(self, parser):
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument("--once", action="store_true")
        mode.add_argument("--loop", action="store_true")
        parser.add_argument("--interval", type=int, default=60)

    def handle(self, *args, **options):
        if options["interval"] < 1:
            raise CommandError("Interval must be at least one second.")
        try:
            while True:
                close_old_connections()
                try:
                    count = reconcile_all()
                except DatabaseError:
                    if options["once"]:
                        raise CommandError(
                            "Scheduling unavailable; retry safely."
                        ) from None
                    self.stderr.write("Scheduling unavailable; retrying next interval.")
                else:
                    self.stdout.write(f"Reconciled: {count} occurrence(s) created.")
                    self.stdout.flush()
                if options["once"]:
                    return
                time.sleep(options["interval"])
        except KeyboardInterrupt:
            self.stdout.write("Scheduler stopped cleanly.")
        finally:
            close_old_connections()
