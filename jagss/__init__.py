# -*- coding: utf-8 -*-

import jinja2
import markdown2
import os
import shutil
import subprocess
import yaml
import json


def render_site_ouput(source_dir, output_base, templates_dir, site_data):
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            folder_id = root[len(source_dir):]
            output_dir = output_base + folder_id
            if f[:1] != '.':
                render_site_file(root, f, output_dir, templates_dir, site_data,
                                 folder_id)


def populate_site_data(location):
    site_data = {'/': []}
    for root, dirs, files in os.walk(location):
        folder_id = '/' + root[len(location) + 1:]
        site_data[folder_id] = []
        for f in files:
            if os.path.splitext(f)[1] == '.md':
                md_data = dict_from_markdown(os.path.join(root, f), folder_id)
                site_data[folder_id].append(md_data)
            if os.path.splitext(f)[1] == '.yaml':
                yml_data = dict_from_yaml(os.path.join(root, f), folder_id)
                site_data[folder_id].append(yml_data)
        for folder in dirs:
            yaml_data = {'relativePath': folder_id}
            yaml_data['type'] = 'folder'
            yaml_data['name'] = folder
            site_data[folder_id].append(yaml_data)
    return site_data


def dict_from_markdown(markdown_path, folder_id):
    separator = '-*-*-*-\n'
    raw_file = open(markdown_path).read()
    separator_index = raw_file.find(separator)
    if separator_index > -1:
        yaml_data = yaml.load(raw_file[:separator_index])
        md_data = raw_file[separator_index + len(separator):]
        html_data = markdown2.markdown(md_data)
        yaml_data['html'] = html_data
        yaml_data['type'] = 'yaml+markdown'
    else:
        yaml_data = {'html': markdown2.markdown(raw_file)}
        yaml_data['type'] = 'markdown'
    yaml_data['relativePath'] = folder_id
    yaml_data['url'] = folder_id + '/'
    filename = os.path.basename(markdown_path)
    yaml_data['url'] += os.path.splitext(filename)[0] + '.html'
    return yaml_data


def dict_from_yaml(yaml_path, folder_id):
    yaml_data = yaml.load(open(yaml_path).read())
    yaml_data['relativePath'] = folder_id
    yaml_data['type'] = 'yaml'
    if 'template' in yaml_data:
        yaml_data['url'] = folder_id + '/'
        filename = os.path.basename(yaml_path)
        yaml_data['url'] += os.path.splitext(filename)[0] + '.html'
    return yaml_data


def render_markdown_file(source_dir, filename, new_dir, templates_dir,
                         site_data, folder_id):
    new_filename = os.path.splitext(filename)[0] + '.html'
    new_path = os.path.join(new_dir, new_filename)
    md_data = dict_from_markdown(os.path.join(source_dir, filename), folder_id)
    if 'template' in md_data:
        jinja_loader = jinja2.FileSystemLoader([templates_dir])
        jinja_env = jinja2.Environment(loader=jinja_loader)
        template = jinja_env.get_template(md_data['template'])
        output = template.render(page=md_data, site=site_data)
        with open(new_path, 'w') as f:
            f.write(output.encode('utf-8'))
    else:
        with open(new_path, 'w') as f:
            f.write(md_data['html'].encode('utf-8'))
    return new_path


def render_yaml_file(source_dir, filename, new_dir, templates_dir, site_data,
                     folder_id):
    new_filename = os.path.splitext(filename)[0] + '.html'
    new_path = os.path.join(new_dir, new_filename)
    yaml_data = dict_from_yaml(os.path.join(source_dir, filename), folder_id)
    if 'template' in yaml_data:
        jinja_loader = jinja2.FileSystemLoader([templates_dir])
        jinja_env = jinja2.Environment(loader=jinja_loader)
        template = jinja_env.get_template(yaml_data['template'])
        output = template.render(page=yaml_data, site=site_data)
        with open(new_path, 'w') as f:
            f.write(output.encode('utf-8'))
    else:
        return False
    return new_path


def render_html_file(source_dir, filename, new_dir, templates_dir, site_data,
                     folder_id):
    new_path = os.path.join(new_dir, filename)
    jinja_fls = jinja2.FileSystemLoader([templates_dir, source_dir])
    jinja_env = jinja2.Environment(loader=jinja_fls)
    template = jinja_env.get_template(filename)
    output = template.render(site=site_data)
    with open(new_path, 'w') as f:
        f.write(output.encode('utf-8'))
    return new_path


def render_site_file(source_dir, filename, output_dir,
                     templates_dir, site_data, folder_id):
    extension = os.path.splitext(filename)[1]
    current_path = os.path.join(source_dir, filename)
    source_length = len(source_dir) + 1
    new_dir = os.path.join(output_dir, source_dir[source_length:])
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    if extension == '.html':
        new_path = render_html_file(source_dir, filename, new_dir,
                                    templates_dir, site_data, folder_id)
    elif extension == '.md':
        new_path = render_markdown_file(source_dir, filename, new_dir,
                                        templates_dir, site_data, folder_id)
    elif extension == '.yaml':
        new_path = render_yaml_file(source_dir, filename, new_dir,
                                    templates_dir, site_data, folder_id)
    else:
        new_path = os.path.join(new_dir, filename)
        shutil.copy2(current_path, new_dir)
    return new_path


def render_less_file(less_file, output_dir):
    basename = os.path.basename(less_file)
    css_dir = os.path.join(output_dir, 'css')
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    css_file = os.path.splitext(basename)[0] + '.css'
    output_file = os.path.join(css_dir, css_file)
    sub_call = ['lessc', '-x', less_file, output_file]
    subprocess.call(sub_call)
    return output_file


def render_sass_file(sass_file, output_dir):
    basename = os.path.basename(sass_file)
    css_dir = os.path.join(output_dir, 'css')
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    css_file = os.path.splitext(basename)[0] + '.css'
    output_file = os.path.join(css_dir, css_file)
    sub_call = ['sass', '--style', 'compressed', sass_file, output_file]
    subprocess.call(sub_call)
    return output_file


def delete_folder_contents(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


def build_static_site(source_dir, output_dir, templates_dir=False,
                      less_file=False, sass_file=False,
                      print_site_data=False):
    delete_folder_contents(output_dir)
    site_data = populate_site_data(source_dir)
    if print_site_data:
        print json.dumps(site_data, sort_keys=True, indent=4)
    if not templates_dir:
        templates_dir = os.path.join(os.path.dirname(source_dir), 'templates')
    render_site_ouput(source_dir, output_dir, templates_dir, site_data)
    if less_file:
        render_less_file(less_file, output_dir)
    if sass_file:
        render_sass_file(sass_file, output_dir)
