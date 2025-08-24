import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import pandas as pd
from config import ABS_PATH_DATA, URL_AI, URL_PRODUCT

class ProgramPageParser:
    def __init__(self, urls):
        self.urls = urls
        self.data_path = ABS_PATH_DATA

    def parse_all(self):
        for name, page_url in self.urls.items():
            print(f"\nОбрабатываем {name}...")
            soup = self.get_soup(page_url)
            if soup:
                table = self.extract_program_data(soup)
                self.save_excel(table, name)
                pdf_url = self.find_pdf(soup, page_url)
                if pdf_url:
                    self.download_pdf(pdf_url, f"study_plan_{name}.pdf")
                else:
                    print("PDF-файл не найден.")

    def get_soup(self, page_url):
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print("Ошибка при запросе страницы:", e)
            return None

    def find_pdf(self, soup, page_url):
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
        if pdf_links:
            return urljoin(page_url, pdf_links[0])
        return None

    def download_pdf(self, pdf_url, filename):
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()
            file_path = self.data_path / filename
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"PDF успешно скачан: {file_path}")
        except requests.RequestException as e:
            print("Ошибка при скачивании PDF:", e)

    def extract_program_data(self, soup):
        """Извлекаем все нужные поля и формируем pandas DataFrame"""
        data = {}

        # Основные поля
        data['Форма обучения'] = self.get_text(soup, "Information_card__text__txwcx", index=0)
        data['Доп. возможности'] = self.get_text(soup, "Information_card__text_none__cRCxR")
        data['Длительность обучения'] = self.get_text(soup, "Information_card__text__txwcx", index=1)
        data['Язык обучения'] = self.get_text(soup, "Information_card__text__txwcx", index=2)
        data['Стоимость обучения'] = self.get_text(soup, "Information_card__text__txwcx", index=3)
        data['Наличие общежития'] = self.get_text(soup, "Information_card__text__txwcx", index=4)
        data['Гос. аккредитация'] = self.get_text(soup, "Information_card__text__txwcx", index=5)

        # Менеджер программы
        data['ФИО менеджера'] = self.get_text(soup, "Information_manager__name__ecPmn")
        data['Контакты'] = self.get_text(soup, "Information_manager__contact__1fPAH")

         # Даты вступительных
        entry_container = soup.find(class_="Information_entry__container__WYx9j")
        if entry_container:
            dates = [h.get_text(strip=True) for h in entry_container.find_all("h6")]
            data['Даты вступительных'] = ", ".join(dates)
            data['Даты вступительных'] = "Скоро появится"
        else:
            data['Даты вступительных'] = "Скоро появится"


        # Направления и описание
        directions = [d.get_text(strip=True) for d in soup.find_all(class_="Directions_table__name__CklG5")]
        data['Направления'] = ", ".join(directions) if directions else ""

        headers = [h.get_text(strip=True) for h in soup.find_all(class_="Directions_table__header__qV8_J")]
        data['Номер направления'] = ", ".join(headers) if headers else ""

        data['Описание программы'] = self.get_text(soup, "AboutProgram_aboutProgram__description__Bf9LA")

        # Преобразуем в DataFrame с одной строкой
        df = pd.DataFrame([data])
        return df

    def get_text(self, soup, class_name, index=0):
        """Возвращает текст из указанного класса, по умолчанию первый элемент"""
        elements = soup.find_all(class_=class_name)
        if elements and len(elements) > index:
            text = elements[index].get_text(separator="\n", strip=True)
            text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
            return text
        return ""

    def save_excel(self, df, program_name):
        filename = self.data_path / f"{program_name.lower()}.xlsx"
        df.to_excel(filename, index=False)
        print(f"Данные программы '{program_name}' сохранены в {filename}")


URLS = {
    "AI": URL_AI,
    "PRODUCT": URL_PRODUCT
}
