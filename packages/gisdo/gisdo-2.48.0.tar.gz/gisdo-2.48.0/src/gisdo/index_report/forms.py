from m3_ext.ui import (
    all_components as ext,
)
from m3_ext.ui.windows import (
    ExtEditWindow,
)

from .constants import (
    INDEXES,
)


class UnloadChildrenByIndexWindow(ExtEditWindow):
    """Окно выбора параметров отчета "Выгрузка детей по показателю/тегу"."""

    def __init__(self, pack, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width, self.height = 450, 150
        self.title = 'Выгрузка детей по показателю/тегу: Параметры'

        self.template_globals = 'ui-js/index-report-edit-window.js'

        self.modal = True
        self.minimizable = True

        self.form = ext.ExtForm()
        self.form.url = pack.unload_by_index_url

        self.unit = ext.ExtDictSelectField(
            anchor='100%',
            label='Организация',
            name='unit_id',
            allow_blank=False,
            hide_edit_trigger=True,
            hide_trigger=False,
            pack='kinder.core.unit.actions.MOReporsAncestorsUnitPack',
        )
        self.unit.editable = False

        self.indexes = ext.ExtMultiSelectField(
            anchor='100%',
            label='Показатель/тег',
            hide_edit_trigger=True,
            hide_trigger=False,
            editable=False,
        )
        self.indexes.set_store(ext.ExtDataStore(data=INDEXES))
        self.indexes.allow_blank = False
        self.indexes.name = 'indexes'

        self.form.items.extend([self.unit, self.indexes])

        self.buttons.extend(
            (
                ext.ExtButton(text='Сформировать', handler='submitForm'),
                ext.ExtButton(text='Отмена', handler='cancelForm'),
            )
        )
