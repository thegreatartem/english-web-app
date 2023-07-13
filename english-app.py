import streamlit as st
from PIL import Image
from streamlit_tags import st_tags, st_tags_sidebar
from streamlit_jina import jina
import pandas as pd
from english import EnglishEx
from io import StringIO



st.write('''
# Янди - веб-приложение для изучения английского языка 

''')

image = Image.open('/home/thegreatartem/Yandex.disk/ds-projects/english-test/Frame 1.png')

st.image(image)


#st.header('Генератор упражнений по английскому')
st.subheader('Вставьте текст или загрузите файл для создания упражнения')

radio = st.radio('Выбери загрузку файла или поле для вставки текста',
         options=('Загрузка файла', 'Поле для текста'))
if radio == 'Загрузка файла':
    file = st.file_uploader("Загрузка файла", type="txt")

    if file == None:
        st.info('Добавьте текст')
        st.stop()
    else:
        stringio = StringIO(file.getvalue().decode("utf-8"))
        txt = stringio.read()

    if st.checkbox("Показать и скрыть текст"):
        # display the text if the checkbox returns True value
        st.write(txt)

else:
    txt_file = st.text_area('Вставка текста', label_visibility="hidden")
    txt = txt_file.read()



count = st.select_slider(
    'Выбери количество упражнений',
    options=range(1, 13))
st.write('Количество упражнений', count)



#st.write(df)



#st.write(tasks)
if st.button('Создать приложение'):
    with st.form('forms'):

        ex = EnglishEx(count, txt)
        df = ex.df_type
        tasks = df.to_dict('records')


        for task in tasks:
            st.subheader(task['describe'])
            col1, col2 = st.columns(2)

            with col1:

                if task['type'] == 'select_sent':
                    options = task['options']
                    for o in task['options'][1:]:
                        st.write(o)
                else:
                    st.write(task['sentences'])


            with col2:

                for i in range(0, len(task['options'])):
                    option = task['options']
                    #st.write(option)
                    if task['type'] == 'missing_word':
                        text_input = st.text_input(placeholder="Enter some text 👇")
                        #st.write(task['result'][i])
                        #st.write(task['answer'])
                        if text_input == task['answer']:
                            st.success('', icon="✅")
                        else:
                            st.error('', icon="😟")

                    else:
                        task['result'][i] = st.selectbox('nolabel', option, label_visibility="hidden")
                        if task['result'][i] == task['answer']:
                            st.success('', icon="✅")
                        else:
                            st.error('', icon="😟")

        total_sum = sum(task['total'] for task in tasks)
        submitted = st.form_submit_button('Отправить ответ')

if submitted:
    if total_sum == len(tasks):
        st.success('Успех!')
        st.balloons()

st.write("Outside the form")













