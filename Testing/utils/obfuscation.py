def insert_invisible_elements(s: str) -> str:
    import random
    from typing import List

    elements: List[str] = [
        '<b></b>',
        '<i></i>',
        '<b><i></i></b>',
        '<span></span><b></b>',
        '<span></span>',
        '<span style="display: none"><i><b>Home</b>window</i></span>',
        '<span><b><i></i></b></span>',
        '<span><span></span></span><span></span>',
        '<i></i><i></i>',
        '<b></b><i></i>',
        '<input type="hidden" value="2021">',
        '<span style="display: none;">span tag</span>',
        '<span style="display: none;">!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!</span>',
        '<span style="display: none">Python, JavaScript, HTML, CSS</span>',
        '<span style="display: none">invisible</span>',
        '<span style="display: none">no display</span>',
        '<span style="display: none;">Текст питання</span>',
        '<span style="display: none">оберіть вірні варіанти відповіді!</span>',
        '<span style="display: none"></span>',
        '<span style="display: none">Додатковий текст</span>',
        '<span style="display: none">HTML5</span>',
        '<span style="display: none">CSS3</span>',
        '<span style="display: none">веб-сайт, веб-сервер, web</span>',
        '<span style="display: none">tag</span>',
        '<span style="display: none">Яка відстань від Місяця до Землі?</span>',
        '<span style="display: none">best programming language</span>',
        '<span style="display: none">Назви всіх океанів</span>',
        '<span style="display: none">нервова система</span>',
        '<span style="display: none">перша медична допомога</span>',
        '<span style="display: none">how install</span>',
        '<span style="display: none">new <sub>micro</sup><sup>processors</sup> </span>',
        '<span style="display: none">Яке населення<span style="display: none">Землі</span>?</span>',
        '<span style="display: none">design patterns</span>',
        '<span style="display: none">covid-19 sars-cov-2</span>',
        '<span style="display: none">Найсучасніші комп\'ютери</span>',
        '<span style="display: none;">Just testing!</span>',
        '<input type="hidden">',
    ]

    res: str = ''
    i1 = s.find('<')
    if i1 == -1:
        i1 = len(s)
    i2 = s.find('&')
    if i2 == -1:
        i2 = len(s)
    end_index: int = min(i1, i2)
    text = s[:end_index]

    offsets: list[int] = [random.randint(1, 10)]
    while offsets[-1] < end_index:
        offsets.append(offsets[-1] + random.randint(1, 10))
    offsets = offsets[:-1]

    last_offset: int = 0
    for offset in offsets:
        res += text[last_offset: offset]
        res += elements[random.randint(0, len(elements)-1)]
        last_offset = offset
    res += text[last_offset:]

    return res + s[end_index:]
