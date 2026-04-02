import os
import streamlit as st
import builder
import parser

st.set_page_config(page_title="Генератор схем DXF", layout="centered")

uploaded_file = st.file_uploader("Загрузите PDF-спецификацию", type="pdf")

if uploaded_file is not None:
    if st.button("Распознать и сгенерировать DXF", type="primary"):
        with st.spinner("Нейросеть читает спецификацию и чертит схему..."):
            try:
                # 1. Сохраняем загруженный файл
                with open("temp_spec.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 2. Вытаскиваем данные через Gemini
                extracted_data = parser.extract_data("temp_spec.pdf")

                # Показываем сырые данные в интерфейсе для контроля
                with st.expander("Посмотреть распознанное оборудование"):
                    st.json(extracted_data)

                # 3. Передаем данные в сборщик и получаем имя готового файла
                output_dxf = builder.generate_scheme(extracted_data)

                st.success("Чертеж успешно сгенерирован!")

                # 4. Выводим кнопку для скачивания DXF
                with open(output_dxf, "rb") as file:
                    st.download_button(
                        label="Скачать готовый чертеж (DXF)",
                        data=file,
                        file_name=f"scheme_{uploaded_file.name}.dxf",
                        mime="application/dxf",
                    )

            except Exception as e:
                st.error(f"Ошибка в процессе работы: {e}")
