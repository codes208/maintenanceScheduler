import os
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

def choose_from(items, label):
    if not items:
        print(f"\nNo {label}s available")
        return None
    print(f"\n{label.capitalize()}s:")
    for i, item in enumerate(items, 1):
        print(f"\t{i}. {item.name}")
    raw = input(f"\nChoose {label} number (or blank to cancel): ").strip()
    if not raw:
        return None
    try:
        idx = int(raw) - 1
        if idx < 0:
                print("Invalid selection")
                return None
        return items[idx]
    except (ValueError, IndexError):
        print("Invalid selection")
        return None

def view_report(owner):
    print(f"\n============== {owner.name} ==============")
    report = owner.report()

    if not report:
        print("\tNo assets to report on.")
        return False

    for asset_name, componets in report.items():
        print(f"\n{asset_name}")
        if not componets:
            print("\t(no components to report)")
        for component_name, tasks in componets.items():
            print(f"\t{component_name}")
            if not tasks:
                print("\t\t(no tasks to report)")
            for task_name, status in tasks.items():
                print(f"\t\t{task_name}: {status}")
    return False

def add_asset(owner):
    asset = input("\nEnter an Asset name (or blank to cancel): ").strip()
    if not asset:
        print("Cancelled.")
        return False
    try:
        owner.add_asset(Asset(asset))
        print(f"\nAdded asset '{asset}'.")
        return True
    except ValueError as e:
        print(f"\nError: {e}")
        return False


def add_component(owner):
    if not owner.assets:
        print("\nNo assets yet - add an asset first.")
        return False
    asset = choose_from(owner.assets, "asset")
    if asset is None:
        return False
    name = input("\nComponent name (or blank to cancel): ").strip()
    if not name:
        print("\nCancelled.")
        return False
    while True:
        answer = input("\nDoes this component have a meter? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            has_meter = True
            break
        elif answer in ("n", "no"):
            has_meter = False
            break
        else:
            print("\nPlease enter y or n.")
    reading = None
    if has_meter:
        raw = input("\nCurrent meter reading (or blank to set later): ").strip()
        if raw:
            try:
                reading = int(raw)
            except ValueError:
                print("\nReading must be a number.")
                return False
    try:
        asset.add_component(Component(name, has_meter, reading))
        print(f"Added component '{name}' to '{asset.name}'.")
        return True
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return False

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
        choice = input("\nEnter a number: ").strip()
    
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
                print("\nSaved.")
            case "8":
                show_help()
            case "9":
                if dirty:
                    confirm = input("Unsaved changes. Save before quitting? (y/n): ").strip().lower()
                    if confirm == "y":
                        save(owner, DEFAULT_PATH)
                        print("Saved.")
                print("Goodbye.")
                break
            case _:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
                    


    



