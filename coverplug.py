"""Coverage plugin to add exclude lines based on the Python version."""

from coverage import CoveragePlugin


class MyConfigPlugin(CoveragePlugin):
    def configure(self, config):
        opt_name = 'report:exclude_lines'
        exclude_lines = config.get_option(opt_name)
        config.set_option(opt_name, exclude_lines)


def coverage_init(reg, options):
    reg.add_configurer(MyConfigPlugin())
