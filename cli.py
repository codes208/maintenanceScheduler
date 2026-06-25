import os
from os.path import exists
from owner import Owner
from asset import Asset
from component import Component
from task import MeteringTask, CalendarTask
from persistence import save, load

DATA_DIR = os.path.expanduser("~/.maintenance_scheduler")
DEFAULT_PATH = os.path.join(DATA_DIR, "schedule.maint")

def load_or_create():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DEFAULT_PATH):
        owner = load(DEFAULT_PATH)
        print(f"Loaded schedule for {owner.name}")
        return owner
    print("No existing schedule found. Starting fresh.")
    print("An 'Owner' is whoever the equipment belongs to - a person, a shop, facility, etc...")
    name = input("Owner name: ").strip()
    return Owner(name)

def show_menu():
    print("\n***** Maintenance Scheduler *****")
    print("1. View Report")
    print("2. Add Asset")
    print("3. Add Component")
    print("4. Add task")
    print("5. Mark task serviced")
    print("6. Update meter reading")
    print("7. Save")
    print("8. Help")
    print("9. Quit")

def show_help():
    print("\n-------- Help --------")
    print("This program tracks maintenance for your equipment.\n")
    print("Structure:")
    print("\tOwner\t- you (or whoever the equipment belongs to)")
    print("\tAsset\t- a major piece of equipment (car, refrigeration system, hyster, computer, etc).")
    print("\tComponent\t- a part of an asset (engine, compressor, mast, keyboard, bearing, etc).")
    print("\tTask\t- a maintenance job on a component (oil change, inspection, cleaning, etc).")
    print("Tasks come in two kinds:")
    print("\tMetering\t- due based on the meter reading (miles, hours, etc).")
    print("\tCalendar\t- due based on time (daily, weekly, monthly, yearly, etc).")
    print("Components with a meter track a reading: tasks become due as the meter climbs.")
    print("Status: ok / due_soon / overdue / unknown (meter not yet set).")

def view_report(owner):
    pass

def add_asset(owner):
    pass

def add_component(owner):
    pass

def add_task(owner):
    pass

def mark_serviced(owner):
    pass

def update_meter(owner):
    pass


def main():
    owner = load_or_create()
    dirty = False

    while True:
        show_menu()
        choice = input("> ").strip()
    
        match choice:
            case "1":
                view_report(owner)
            case "2":
                dirty = add_asset(owner) or dirty
            case "3":
                dirty = add_component(owner) or dirty
            case "4":
                dirty = add_task(owner) or dirty
            case "5":
                dirty = mark_serviced(owner) or dirty
            case "6":
                dirty = update_meter(owner) or dirty
            case "7":
                save(owner, DEFAULT_PATH)
                dirty = False
                print("Saved.")
            case "8":
                show_help()
            case "9":
                if dirty:
                    confirm = input("Unsaved changes. Save before quitting? (y/n): ").strip().lower()
                    if confirm == "y":
                        save(owner, DEFAULT_PATH)
                        print("Saved.")
                print("Goodbye.")
                break;
            case _:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
                    


    



