from django.conf import (
    settings,
)
from django.test.runner import (
    DiscoverRunner,
)


# configure(default_settings=settings,
settings.DEBUG = True
settings.TEMPLATE_DEBUG = True


class KeepDatabaseTestRunner(DiscoverRunner):
    """Пропускаем создание тестовой БД, и запускаем тесты на дефолтной.
    ВНимание! не использовать при обычных тестах, только для проверок,
    иначе можно добавить тестовые невалидные данные
    """

    def __init__(
        self,
        pattern=None,
        top_level=None,
        verbosity=1,
        interactive=True,
        failfast=False,
        keepdb=False,
        reverse=False,
        debug_mode=False,
        debug_sql=False,
        parallel=0,
        tags=None,
        exclude_tags=None,
        **kwargs,
    ):
        """Выставлен keepdb = True, чтобы раннер не спрашивал
        надо ли пересоздать дейсвующую БД"""
        self.pattern = pattern
        self.top_level = top_level
        self.verbosity = verbosity
        self.interactive = interactive
        self.failfast = failfast
        self.keepdb = True
        self.reverse = reverse
        self.debug_mode = debug_mode
        self.debug_sql = debug_sql
        self.parallel = parallel
        self.tags = set(tags or [])
        self.exclude_tags = set(exclude_tags or [])

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        # old_config = self.setup_databases()
        result = self.run_suite(suite)
        # self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)
