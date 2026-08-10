import flet as ft
import requests

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def get_exchange_rates(base_currency):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data["rates"]
    except Exception as e:
        print(f"Error fetching rates: {e}")
        return None

def main(page: ft.Page):
    page.title = "Currency Converter"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    from_currency = ft.Dropdown(
        label="From",
        options=[ft.dropdown.Option("USD"), ft.dropdown.Option("EUR"), ft.dropdown.Option("GBP"), ft.dropdown.Option("JPY")],
        value="USD",
        width=150,
    )
    to_currency = ft.Dropdown(
        label="To",
        options=[ft.dropdown.Option("USD"), ft.dropdown.Option("EUR"), ft.dropdown.Option("GBP"), ft.dropdown.Option("JPY")],
        value="EUR",
        width=150,
    )
    amount_input = ft.TextField(label="Amount", value="1", width=150)
    result_text = ft.Text("", size=20)

    def convert_clicked(e):
        try:
            amount = float(amount_input.value)
            rates = get_exchange_rates(from_currency.value)
            if rates and to_currency.value in rates:
                if from_currency.value == "USD":
                    converted = amount * rates[to_currency.value]
                else:
                    usd_value = amount / rates[from_currency.value]
                    converted = usd_value * rates[to_currency.value]
                result_text.value = f"{amount} {from_currency.value} = {converted:.2f} {to_currency.value}"
            else:
                result_text.value = "Error fetching rates!"
        except Exception as e:
            result_text.value = f"Error: {str(e)}"
        page.update()

    convert_btn = ft.ElevatedButton("Convert", on_click=convert_clicked)

    page.add(
        ft.Row([from_currency, to_currency], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([amount_input, convert_btn], alignment=ft.MainAxisAlignment.CENTER),
        result_text,
    )

ft.app(target=main)
