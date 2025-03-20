from pylatex import (
    Document,
    LongTable,
    Package,
)
from pylatex.utils import (
    bold,
)


class Reporter:
    """
    Построитель отчёта "Список детей, получивших места в дошкольных организациях"
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def report(self, data):
        """
        Создать отчёт по данным
        """
        doc = Document(
            'report',
            fontenc='T2A,T1',
            indent=False,
            geometry_options=[
                'landscape',
                'a4paper',
                'left=20mm',
                'top=20mm',
            ],
        )
        doc.packages.append(Package('DejaVuSerifCondensed'))
        doc.packages.append(Package('babel', options='main=russian'))

        with doc.create(
            LongTable(
                'p{0.2\linewidth} | '
                'p{0.1\linewidth} | '
                'p{0.15\linewidth} | '
                'p{0.1\linewidth} | '
                'p{0.15\linewidth} | '
                'p{0.1\linewidth} | '
                'p{0.2\linewidth}'
            )
        ) as table:
            table.add_hline()
            table.add_row(
                (
                    'Идентификатор заявления',
                    'Дата и время подачи заявления',
                    'Наличие внеочередного, первоочередного или преимущественного права для приема с указанием вида права',
                    'Возрастная категория группы',
                    'Направленность группы с указанием вида для групп компенсирующей и комбинированной направленности и профиля группы для оздоровительных групп',
                    'Режим пребывания ребенка в группе',
                    'Наименование и направленность образовательной программы (при наличии) или данные об осуществлении только присмотра и ухода, язык обучения',
                ),
                mapper=[bold],
            )
            table.add_hline()
            table.end_table_header()
            for row in data:
                table.add_row(tuple(d if d is not None else '' for d in row))
                table.add_hline()

        doc.generate_pdf(filepath=self.file_path, clean_tex=True, clean=True)
