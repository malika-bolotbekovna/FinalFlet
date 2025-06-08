import flet as ft
from db import main_db

def main(page: ft.Page):
    print('downloading')
    page.title = "Task Manager"
    page.theme_mode = ft.ThemeMode.SYSTEM

    # отсупы между элементами
    task_list = ft.Column(spacing=10)
    # показывает все, без фильтра
    filter_type = 'all'
    total_count_text = ft.Text("")


    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    def load_task():
        task_list.controls.clear()
        tasks = list(main_db.get_task(filter_type))
        total_count = len(tasks)

        for task_id, task, completed, date in tasks:
            task_list.controls.append(create_tasks_row(task_id, task, completed, date))

        total_count_text.value = f"Всего задач: {total_count}"
        page.update()



    def create_tasks_row(task_id, task, completed, date):
        task_field = ft.TextField(value=task, expand=True, read_only=True)
        added_date_text = ft.Text(f'Дата добавления: {date}')

        task_checkbox= ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        return ft.Row([
            task_checkbox,
            ft.Column([task_field, added_date_text], expand=True),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e: delete_tasks(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # добавление новой покупки
    def add_task(e):
        if task_input.value:
            main_db.add_task_db(task_input.value)
            task_input.value = ""
            load_task()
            page.update()


    def toggle_task(task_id, completed):
        main_db.update_task_db(task_id, completed=int(completed))
        load_task()


    def delete_tasks(task_id):
        main_db.delete_task_id(task_id)
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    theme_button = ft.IconButton(ft.Icons.SUNNY, on_click=change_theme)
    filter_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("Выполненные", on_click=lambda e: set_filter('completed')),
            ft.ElevatedButton("Не выполненные", on_click=lambda e: set_filter('not_completed'))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    task_input = ft.TextField(hint_text="Добавьте задачу: ", expand=True, dense=True, on_submit=add_task)

    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[ft.Text('Task Manager', size=30), theme_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    controls=[task_input, add_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                filter_buttons,
                total_count_text,
                task_list
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(content)



if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)