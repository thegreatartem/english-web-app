import streamlit as st
from PIL import Image
#from streamlit_tags import st_tags, st_tags_sidebar
#from streamlit_jina import jina
import pandas as pd
from english import EnglishEx
from io import StringIO
tasks = [{'sentences': 'The good grandmother , who was in bed , because she was albeit somewhat ill , cried out , " Pull the bobbin , and the latch will go up . "',
          'object': 'somewhat',
          'options': [['---', 'Pull', 'was', 'albeit']],
          'answer': 'albeit',
          'describe': 'Выбери лишние слово',
          'result': [''],
          'total': 0,
          'type': 'delete_word'},
         {'sentences': 'And , insisted saying these words , this wicked wolf fell upon Little Red Riding Hood , and ate her all up .',
          'object': 'saying',
          'options': [['---', 'up', 'and', 'insisted']],
          'answer': 'insisted',
          'describe': 'Выбери лишние слово',
          'result': [''],
          'total': 0,
          'type': 'delete_word'},
         {'sentences': '" Your grandchild , Little Red Riding Hood , " replied the wolf , counterfeiting her voice ; " who has brought you a cake and a ___ pot of butter sent you by mother . "',
          'object': 'little',
          'options': [['---', 'little', 'good', 'even']],
          'answer': 'little',
          'describe': 'Выберите слово',
          'result': [''],
          'total': 0,
          'type': 'select_word'},
         {'sentences': '" Well , " said the wolf , " and I \'ll going go and see her too .',
          'object': 'go',
          'options': [['---', 'and', 'her', 'going']],
          'answer': 'going',
          'describe': 'Выбери лишние слово',
          'result': [''],
          'total': 0,
          'type': 'delete_word'},
         {'sentences': "He then shut the door and got into the grandmother 's ___ , expecting Little Red Riding Hood , who came some time afterwards and knocked at the door : tap , tap .",
          'object': 'bed',
          'options': [['---', 'bed', 'slept', 'couch']],
          'answer': 'bed',
          'describe': 'Выберите слово',
          'result': [''],
          'total': 0,
          'type': 'select_word'},
         {'sentences': '" Grandmother , what big ___ you have ! "',
          'object': 'eyes',
          'options': [['']],
          'answer': 'eyes',
          'describe': 'Заполните пропуск',
          'result': [''],
          'total': 0,
          'type': 'missing_word'},
         {'sentences': '',
          'object': "She was greatly amazed to see how her grandmother looked in her nightclothes, and said to her, Grandmother, what big arms you have!",
          'options': [['---',
               'She was greatly amazed to see how her grandmother looked in her nightclothes, and said to her, "Grandmother, what big arms you have!"',
               'She was substantially astonished to you how her mother seemed in her bearskins, and asked to her, "Grandmother, what like armed you are!"',
               'She was considerably astounded to turn how her niece suddenly in her capitivity, and warned to her, "Grandmother, what biggest hands you had!"']],
              'answer': 'She was greatly amazed to see how her grandmother looked in her nightclothes, and said to her, "Grandmother, what big arms you have!"',
              'describe': 'Выбери правильное предложение',
              'result': [''],
              'total': 0,
              'type': 'select_sent'},
             {'sentences': 'william Charles Perrault',
              'object': 'Charles',
              'options': [['---', 'Perrault', 'Perrault', 'william']],
              'answer': 'william',
              'describe': 'Выбери лишние слово',
              'result': [['']],
              'total': 0,
              'type': 'delete_word'},
             {'sentences': 'One day her mother , having made some cakes , ___ to her , " Go , my dear , and see how your grandmother is doing , for I hear she has been very ill .',
              'object': 'said',
              'options': [['---', 'said', 'but', 'adding']],
              'answer': 'said',
              'describe': 'Выберите слово',
              'result': [''],
              'total': 0,
              'type': 'select_word'},
             {'sentences': 'I say " wolf , " but there are various types kinds of wolves .',
              'object': 'kinds',
              'options': [['---', '"', 'I', 'types']],
              'answer': 'types',
              'describe': 'Выбери лишние слово',
              'result': [''],
              'total': 0,
              'type': 'delete_word'}]




st.write('''
# Янди - веб-приложение для изучения английского языка 

''')

image = Image.open('/home/thegreatartem/Yandex.disk/ds-projects/english-test/Frame 1.png')

st.image(image)



st.write("Outside the form")


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
    options=range(0, 11))
st.write('Количество упражнений', count)

if count == 0:
    st.stop()

'---'
tasks = tasks[:count]
st.header('Выберите правильные варианты:')

# with st.form('forms'):
for task in tasks:
    st.subheader(task['describe'])
    col1, col2 = st.columns(2)
    with col1:
        st.write('')
        if task['type'] == 'select_sent':
            for i in task['options']:
                for x in range(1, len(i)):
                    st.write(i[x])


        else:
            st.write(str(task['sentences']))

    with col2:
        for i in range(len(task['options'])):
            option = task['options'][i]
            #st.write(option)
            if task['type'] == 'missing_word':
                text_input = st.text_input("Enter some text 👇")
                # st.write(task['result'][i])
                # st.write(task['answer'])
                if text_input == task['answer']:
                    st.success('', icon="✅")
                else:
                    st.error('', icon="😟")
            else:
                task['result'][i] = st.selectbox('nolabel', option, label_visibility="hidden")
                #st.write(task['result'][i])
                #st.write(task['answer'])
                if task['result'][i] == '–––':
                    pass
                elif task['result'][i] == task['answer']:
                    st.success('', icon="✅")
                else:
                    st.error('', icon="😟")
    task['total'] = task['result'] == task['answer']
    '---'

total_sum = sum(task['total'] for task in tasks)
if total_sum == len(tasks):
    st.success('Успех!')
    st.balloons()

    # submitted = st.form_submit_button('Отправить ответ')
    # if submitted:
    #     if total_sum == len(tasks):
    #         st.success('Успех!')
    #         st.balloons()
