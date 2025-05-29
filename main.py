import flet as ft
from db import main_db

def main(page: ft.Page):
    print('downloading')
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True

    # отсупы между элементами
    buy_list = ft.Column(spacing=10)
    # показывает все, без фильтра
    filter_type = 'all'
    total_count_text = ft.Text("")


    def load_buy():
        buy_list.controls.clear()
        buys = list(main_db.get_buys(filter_type))
        total_count = len(buys)

        for purchase_id, purchase, bought in buys:
            buy_list.controls.append(create_buys_row(purchase_id, purchase, bought))

        total_count_text.value = f"Всего товаров: {total_count}"
        page.update()



    def create_buys_row(purchase_id, purchase, bought):
        purchase_field = ft.TextField(value=purchase, expand=True, read_only=True)

        buy_checkbox= ft.Checkbox(
            value=bool(bought),
            on_change=lambda e: toggle_buy(purchase_id, e.control.value)
        )

        return ft.Row([
            buy_checkbox,
            ft.Column([purchase_field], expand=True),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e: delete_purchases(purchase_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # добавление новой покупки
    def add_purchase(e):
        if buy_input.value:
            main_db.add_buy_db(buy_input.value)
            buy_input.value = ""
            load_buy()
            page.update()


    def toggle_buy(purchase_id, is_bought):
        main_db.update_buy_db(purchase_id, is_bought=int(is_bought))
        load_buy()


    def delete_purchases(purchase_id):
        main_db.delete_buy_id(purchase_id)
        load_buy()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_buy()

    filter_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("Купленные", on_click=lambda e: set_filter('bought')),
            ft.ElevatedButton("Не купленные", on_click=lambda e: set_filter('not_bought'))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    buy_input = ft.TextField(hint_text="Добавьте покупку: ", expand=True, dense=True, on_submit=add_purchase)

    add_button = ft.ElevatedButton("Добавить", on_click=add_purchase, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[buy_input, add_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                filter_buttons,
                total_count_text,
                buy_list
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=20,
        alignment=ft.alignment.center
    )


    background_image = ft.Image(
        src="958080.jpg",
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )   

    background = ft.Stack(controls=[background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        background.update()

    page.add(background)
    page.on_resize = on_resize



if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)