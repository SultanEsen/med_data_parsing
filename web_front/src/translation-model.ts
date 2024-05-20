import { atom } from "@reatom/framework";
import { withLocalStorage } from "@reatom/persist-web-storage";

export type Language = "en" | "ru";
export const languageAtom = atom<Language>("en", "languageAtom").pipe(withLocalStorage("language"));

const dictionary = new Map<Language, { [key: string]: string }>(
  [
    ["ru", { 
      "Translate": "Перевод",
      "Select columns": "Выбор столбцов",
      "Search": "Поиск",
      "Select columns for": "Выбор столбцов для страны:",
      "prev": "пред",
      "next": "след",
      "go": "Перейти",
      "Raw Data": "Исходные данные",
      "Prepared": "Готовые",
      "Uzbekistan": "Узбекистан",
      "Kazakhstan": "Казахстан",
      "Russia": "Россия",
      "Belarus": "Беларусь",
      "Ukraine": "Украина",
      "Turkey": "Турция",
      "Moldova": "Молдавия",
      "id": "ID",
      "package_id": "ID упаковки",
      "trade_mark_name": "Торговое название",
      "mnn": "МНН",
      "producer": "Производитель",
      "package": "Упаковка",
      "registration_name": "Номер регистрации",
      "registration_number": "Номер регистрации",
      "currency": "Валюта",
      "limit_price": "Предельная цена",
      "current_retail_price": "Текущая розничная цена",
      "current_wholesale_price": "Текущая оптовая цена",
      "dosage_form": "Лекарственная форма",

    }],
    ["en", {
      "Translate": "Translate",
      "Select columns": "Select columns",
      "Search": "Search",
      "Select columns for": "Select columns for",
      "prev": "prev",
      "next": "next",
      "go": "Go",
      "Uzbekistan": "Uzbekistan",
      "Kazakhstan": "Kazakhstan",
      "Russia": "Russia",
      "Belarus": "Belarus",
      "Ukraine": "Ukraine",
      "Turkey": "Turkey",
      "Moldova": "Moldova",
      "Raw Data": "Raw Data",
      "Prepared": "Prepared",
      "id": "ID",
      "package_id": "Package ID",
      "trade_mark_name": "Trade mark name",
      "mnn": "MNN",
      "producer": "Producer",
      "package": "Package",
      "registration_name": "Registration name",
      "registration_number": "Registration number",
      "currency": "Currency",
      "limit_price": "Limit price",
      "current_retail_price": "Current retail price",
      "current_wholesale_price": "Current wholesale price",
      "dosage_form": "Dosage form",
    }]
  ]
);

export const dictionaryAtom = atom((ctx) => {
  const lang = ctx.spy(languageAtom);
  if (dictionary.has(lang)) {
    return dictionary.get(lang);
  }
  return dictionary.get("en");
})

