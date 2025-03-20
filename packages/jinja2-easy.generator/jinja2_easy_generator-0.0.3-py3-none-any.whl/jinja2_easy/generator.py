from os import path, listdir
import jinja2
import platformdirs
import re

class Generator:
    def __init__(self, name, dir=path.dirname(path.abspath(__file__)), extra_dirs=[]):
        self.name = name
        self.dir = dir
        self.extra_dirs = extra_dirs
        self.template_dirs = [
            path.join(i, "templates")
            for i in (
                # user dir
                path.join(path.expanduser("~"), f".{name}"),
                platformdirs.user_data_dir(appname=name),
                platformdirs.user_config_dir(appname=name),
                # usually inside the site-packages dir
                dir,
                # system wide dir
                *platformdirs.site_data_dir(appname=name, multipath=True).split(":"),
            )
        ] + extra_dirs

    def default_file_template(self):
        return self.file_template_list()[0]

    @staticmethod
    def default_file_output(name, template):
        a = template.rsplit(".")
        if (len(a)) > 1:
            return name + "." + a[1]
        else:
            return name

    def write_template(self, data, template, filename):
        #   if not filename:
        #       filename = "python-" + name + '.' + template.rsplit('.', 1)[1]   # take template file ending
        result = self.render(data, template)
        outfile = open(filename, "wb")
        try:
            outfile.write(result)
        finally:
            outfile.close()

    def render(self, data, template):
        #     if not template:
        #         template = self.file_template_list()[0]
        env = self.prepare_template_env()
        template = env.get_template(template)
        return template.render(data).encode("utf-8")

    def get_template_dirs(self):
        """existing directories where to search for jinja2 templates. The order
        is important. The first found template from the first found dir wins!"""
        return filter(lambda x: path.exists(x), self.template_dirs)

    def prepare_template_env(self):
        # setup jinja2 environment with custom filters
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.get_template_dirs())
        )
        env.filters["parenthesize_version"] = lambda s: re.sub(
            "([=<>]+)(.+)", r" (\1 \2)", s
        )
        env.filters["basename"] = lambda s: s[s.rfind("/") + 1 :]
        return env

    def file_template_list(self):
        template_files = []
        for d in self.get_template_dirs():
            template_files += [f for f in listdir(d) if not f.startswith(".")]
        return template_files
