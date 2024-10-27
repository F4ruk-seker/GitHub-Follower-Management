from jinja2 import Template, Environment
import os
import tempfile


def write_html_report() -> str:
    new_temp_dir = tempfile.mkdtemp()
    template_file = 'report_template.html'
    template = Template(template_file.read())
    output = template.render()
    output_path = os.path.join(new_temp_dir, 'github-report-f4.html')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(output)
    return output_path
