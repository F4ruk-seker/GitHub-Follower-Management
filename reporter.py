from jinja2 import Template
import os
import tempfile


def write_html_report(context: dict) -> str | None:
    new_temp_dir = tempfile.mkdtemp()
    template_file_name = 'report_template.html'
    with open(template_file_name, encoding='utf-8') as template_file:
        template = Template(template_file.read())
    output = template.render(context)
    output_path = os.path.join(new_temp_dir, 'github-report-f4.html')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(output)
    return output_path
