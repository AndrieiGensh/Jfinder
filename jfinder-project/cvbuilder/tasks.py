from celery import shared_task
from pathlib import Path
import os
from jinja2 import Environment, FileSystemLoader

@shared_task
def generate_cv(template = "template.tex", data = {}):
    base_path = os.path.join(Path(__file__).resolve().parent.parent, 'templates/cvbuilder/cv_templates')
    dist_dir = 'dist'
    dist_path = os.path.join(base_path, dist_dir)

    jinja_env = Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(searchpath = base_path),
    )

    template = jinja_env.get_template(template)
    template_out_path = os.path.join(dist_path, template)

    with open(template_out_path, 'w') as fout:
        fout.write(template.render(data = {
            'name' : 'Andras',
            'contact': {
                'phone': 1234567,
                'email': 'test@gmail.com',
                'linkedin': 'https://something/here'
            },
            'summary': {
                "one": 'one',
                'two': 'two',
                'three': 'three',
            }
        }))

    os.system('pdflatex -interaction=nonstopmode -output-directory={} {}'.format(dist_path, template_out_path))