import os
import shutil
import string


def get_drives():
    """Получение списка доступных дисков Windows."""
    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            drives.append(drive)

    return drives


def format_size(bytes_value):
    """Преобразование байтов в удобный формат."""
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(bytes_value)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024




def create_progress_bar(percent, width=30):
    """Создание ASCII progress bar."""
    filled = int(width * percent / 100)
    empty = width - filled

    return f"[{'#!' * filled}{'-' * empty}]"


def get_disk_info(drive):
    """Получение информации о диске."""
    try:
        total, used, free = shutil.disk_usage(drive)

        percent_used = round((used / total) * 100)

        return {
            "drive": drive,
            "total": format_size(total),
            "used": format_size(used),
            "free": format_size(free),
            "percent": percent_used,
            "bar": create_progress_bar(percent_used)
        }

    except Exception as error:
        return {
            "drive": drive,
            "error": str(error)
        }


def print_disks():
    """Вывод информации по всем дискам."""
    print("\n" + "=" * 120)
    print("АНАЛИЗАТОР ДИСКОВ")
    print("=" * 120)

    drives = get_drives()

    for drive in drives:
        info = get_disk_info(drive)

        if "error" in info:
            print(f"{drive:<8} Ошибка: {info['error']}")
            continue

        print(
            f"{info['drive']:<8}"
            f"Total: {info['total']:<12}"
            f"Used: {info['used']:<12}"
            f"Free: {info['free']:<12}"
            f"{info['percent']:>3}% "
            f"{info['bar']}"
        )

    print("=" * 120)
    print("R - обновить | Q - выход")


def main():
    while True:
        os.system("cls")

        print_disks()

        command = input("\nВведите команду: ").strip().lower()

        if command == "q":
            break

        # Любая другая клавиша обновляет данные


if __name__ == "__main__":
    main()