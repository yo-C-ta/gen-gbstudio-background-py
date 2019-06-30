from behave import given, when, then
import subprocess
import hashlib
import os


def run_command(command):
    proc = subprocess.run(command,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.decode('utf8')
    return output


def get_hash(filename):
    m = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()


@given('we have a "{grid}" file in CSV')
def we_have_a_grid_file_in_csv(context, grid):
    context.subprocess_cmd = ['python', 'csv2background.py', grid]


@given('we have a "{config}" file in JSON')
def we_have_a_config_file_in_json(context, config):
    context.subprocess_cmd.append(config)


@when('we run the composer')
def we_run_the_composer(context):
    output_filename = 'test.png'
    context.subprocess_cmd.extend(['--output', output_filename])
    subprocess.run(context.subprocess_cmd)
    context.got_hash = get_hash(output_filename)
    os.remove(output_filename)


@then('we get an output file in PNG like this "{image}"')
def we_get_an_output_file_in_png_like_this_image(context, image):
    hash = context.got_hash
    expected = get_hash(image)
    assert hash == expected, 'got "%s" but expected "%s"' % (hash, expected)
