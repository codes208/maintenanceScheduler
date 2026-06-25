# TODO CLI: warn when service_update value is below current last_serviced (legal but unusual — likely a typo)
# CalendarTask(name, interval, last_serviced, warning_buffer):
# MeteringTask(name, interval, last_serviced, unit, warning_buffer=0)

from cli import main

if __name__ == "__main__":
    main()

