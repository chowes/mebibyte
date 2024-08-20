import argparse
import streamlit as st
import requests

from bs4 import BeautifulSoup

github_link = "https://github.com/chowes/mebibyte"
github_logo_path = "app/static/GitHub_Lockup_Light.png"


class MebibyteApp:
    mebibyte_endpoint: str
    expression: str

    def __init__(self, mebibyte_endpoint: str):
        self.mebibyte_endpoint = mebibyte_endpoint

    def page_config(self):
        st.set_page_config(
            page_title="Mebibyte",
            page_icon=":floppy_disk:",
            layout="centered",
            initial_sidebar_state="auto",
        )

    def expression_input(self):
        st.title("Mebibyte")

        self.expression = st.text_input(
            label="Enter Expression",
            placeholder="2^30 bytes + (2 KiB * 4) in KiB",
            key="expression",
            autocomplete="off",
            help="Enter an expression and (optionally) a unit to display the result in.",
        )

    def send_request(self, expression: str) -> requests.Response:
        response = requests.post(
            self.mebibyte_endpoint,
            json={"expression": expression},
        )
        return response

    def extract_error_message(self, response: requests.Response) -> str:
        if not response.content:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        if not soup.find('h1'):
            return "Invalid expression"
        error_title = soup.find('h1').get_text()

        if not soup.find('p'):
            return error_title
        error_message = soup.find('p').get_text()

        return f"{error_title}: {error_message}"

    def handle_input(self):
        expression = self.expression.strip()

        # Send a request when the user hits enter or presses a button
        if st.button("Evaluate") or expression:
            if not expression:
                return
            try:
                response = self.send_request(expression)
                response.raise_for_status()
                result = response.json().get('result')
                st.success(result)
            except requests.exceptions.HTTPError as e:
                print(e)
                error_message = self.extract_error_message(response)
                if error_message:
                    st.error(error_message)
                else:
                    st.error("An error occurred :(")
            except Exception as e:
                print(e)
                st.error("An error occurred :(")

    def sidebar(self):
        with st.sidebar:
            st.markdown(
                f"""
                ### Examples:
                - `1 MiB in bytes`
                - `2^30 bytes in MiB`
                - `2 MiB / 2 KiB`
                - `100 TiB in TB`
                - `100 MiB in gigabits`
                - `(1 MiB + 512 KiB) * 2 in KiB`

                ### What won't work?
                - Exponents (`2 MiB ^ 2`)
                - Rates (`100 MiB/s`)
                - Higher order units (`2 MiB * 1 KiB`)
                - Reciprocals (`1 / 2 MiB`)
                - Mixed units (`1 KB + 1`)

                ### Supported units:
                - Bit-based units (`gigabits`)
                - Byte-based units (`gigabytes`)
                - Binary prefix units up to `exbibytes`
                - Decimal prefix units up to `exabytes`
                - Shorthand for byte-based units (`GiB`)
                - Units are not case sensitive

                <style>
                .resizable-image {{
                    height: 1.5em;
                    vertical-align: middle;
                }}
                </style>
                <a href="{github_link}" target="_blank" style="color: #ffffff;">
                    <img src="{github_logo_path}" class="resizable-image">
                </a>
                """,
                unsafe_allow_html=True,
            )

    def run(self):
        self.page_config()
        self.sidebar()
        self.expression_input()
        self.handle_input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='mebibyte-frontend',
        description='Mebibyte frontend')

    parser.add_argument(
        "--mebibyte-endpoint",
        type=str,
        required=True
    )

    args = parser.parse_args()

    app = MebibyteApp(args.mebibyte_endpoint)
    app.run()
