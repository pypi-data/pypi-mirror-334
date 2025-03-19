# To run without installing, relative imports must match the module imports,
# which is satisfied when in 'src' directory: python3 -m upp.upp --help

import click
import tempfile
from upp import decode
import importlib.metadata
import os.path
import sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
REG_CTRL_CLASS = 'Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}'
REG_KEY = 'ControlSet001\\' + REG_CTRL_CLASS
REG_KEY_VAL = 'PP_PhmSoftPowerPlayTable'
REG_HEADER = 'Windows Registry Editor Version 5.00' + 2 * '\r\n' + \
             '[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\' + \
             REG_CTRL_CLASS + '\\0000]\r\n'


def _normalize_var_path(var_path_str):
    var_path_list = var_path_str.strip('/').split('/')
    normalized_var_path_list = [
      int(item) if item.isdigit() else item for item in var_path_list]
    return normalized_var_path_list


def _is_int_or_float(value):
    if value.isdigit():
        return True
    try:
        float(value)
        return True
    except ValueError:
        pass
    return False


def _validate_set_pair(set_pair):
    valid = False
    if '=' in set_pair and _is_int_or_float(set_pair.split('=')[-1]):
        return set_pair.split('=')
    else:
        print("ERROR: Invalid variable assignment '{}'. ".format(set_pair),
              "Assignment must be specified in <variable-path>=<value> ",
              "format. For example: /PowerTuneTable/TDP=75")
        return None, None


def _get_pp_data_from_registry(reg_file_path):
    reg_path = 'HKLM\\SYSTEM\\' + REG_KEY + ':' + REG_KEY_VAL
    try:
        from Registry import Registry
    except ImportError as e:
        print('ERROR: -f/--from-registry option requires python-registry',
              'package, consider installing it with PIP.')
        sys.exit(-2)
    try:
        reg = Registry.Registry(reg_file_path)
        keys = reg.open(REG_KEY)
    except Exception as e:
        print('ERROR: Can not access', REG_KEY, 'in', reg_file_path)
        print(e)
        return None
    found_data = False
    for key in keys.subkeys():
        index = key.name()
        key_path = REG_KEY + '\\' + index
        if index.startswith('0'):
            try:
                data_type = key.value(REG_KEY_VAL).value_type_str()
                registry_data = key.value(REG_KEY_VAL).raw_data()
                print('Found', data_type, 'type value', REG_KEY_VAL,
                      'in', key_path)
                if found_data:
                    print('WARNING: Multiple PP tables found in the registry,',
                          'only using data from last table found!')
                found_data = True
                tmpf_prefix = 'registry_device_' + index + '_pp_table_'
                tmp_pp_file = tempfile.NamedTemporaryFile(prefix=tmpf_prefix,
                                                          delete=False)
                decode._write_binary_file(tmp_pp_file.name, registry_data)
                print('Saved registry PP table', 'data to', tmp_pp_file.name)
                tmp_pp_file.close()
            except Registry.RegistryValueNotFoundException:
                print("Can't find needed value", REG_KEY_VAL, 'in', key_path)

    return tmp_pp_file.name


def _get_pp_data_from_mpt(mpt_filename):

    try:
        mpt_bytes = decode._read_binary_file(mpt_filename)
    except Exception as e:
        print('ERROR: Can not access', mpt_filename)
        print(e)
        sys.exit(-2)
    mpt_table_filename = mpt_filename + '.pp_table'
    print('Saving MPT PP table data to', mpt_table_filename)
    decode._write_binary_file(mpt_table_filename, mpt_bytes[0x100:])

    return mpt_table_filename


def _check_file_writeable(filename):
    if os.path.exists(filename):
        if os.path.isfile(filename):
            return os.access(filename, os.W_OK)
        else:
            return False
    pdir = os.path.dirname(filename)
    if not pdir:
        pdir = '.'
    return os.access(pdir, os.W_OK)


def _write_pp_to_reg_file(filename, data, debug=False):
    if _check_file_writeable(filename):
        reg_string = REG_KEY_VAL[3:] + '"=hex:' + data.hex(',')
        reg_lines = [reg_string[i:i+75] for i in range(0, len(reg_string), 75)]
        reg_lines[0] = '"' + REG_KEY_VAL[:3] + reg_lines[0]
        formatted_reg_string = '\\\r\n  '.join(reg_lines)
        reg_pp_data = REG_HEADER + formatted_reg_string + 2 * '\r\n'
        if debug:
            print(reg_pp_data)
        decode._write_binary_file(filename, reg_pp_data.encode('utf-16'))
        print('Written {} Soft PowerPlay bytes to {}'.format(len(data),
                                                             filename))
    else:
        print('Can not write to {}'.format(filename))
    return 0


def _load_variable_set(dump_filename):
    variable_set = []
    with open(dump_filename, 'r') as file:
        keys = []
        indent = 0
        prev_indent = 0
        lines = file.readlines()
        for line in lines:
            prev_indent = indent
            indent = (len(line) - len(line.lstrip()))//2
            if line.strip() == '':
                continue
            if indent == 0:
                keys.clear()
            elif indent <= prev_indent:
                keys = keys[0:indent]

            key, value = line.split(':')
            key = key.strip()
            value = value.strip()
            if len(value) > 0:
                value = value.split()[0]
            if key.find('Unused') == 0 or value.find('UNUSED') == 0:
                continue
            if len(keys) > 0 and key.find(keys[-1]) == 0:
                key = key.split(' ')[1]
            keys.append(key)
            if value != '':
                variable_set.append('{}={}'.format('/'.join(keys), value))
    return variable_set


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-p', '--pp-file', help='Input/output PP table binary file.',
              metavar='<filename>',
              default='/sys/class/drm/card0/device/pp_table')
@click.option('-f', '--from-registry',
              help='Import PP_PhmSoftPowerPlayTable from Windows registry ' +
                   '(overrides -p / --pp-file option).',
              metavar='<filename>')
@click.option('-m', '--from-mpt',
              help='Import PowerPlay Table from More Power Tool ' +
                   '(overrides --pp-file and --from-registry optios).',
              metavar='<filename>')
@click.option('--debug/--no-debug', '-d/ ', default='False',
              help='Debug mode.')
@click.pass_context
def cli(ctx, debug, pp_file, from_registry, from_mpt):
    """UPP: Uplift Power Play

    A tool for parsing, dumping and modifying data in Radeon PowerPlay tables.

    UPP is able to parse and modify binary data structures of PowerPlay
    tables commonly found on certain AMD Radeon GPUs. Drivers on recent
    AMD GPUs allow PowerPlay tables to be dynamically modified on runtime,
    which may be known as "soft PowerPlay tables". On Linux, the PowerPlay
    table is by default found at:

    \b
       /sys/class/drm/card0/device/pp_table

    There are also two alternative ways of getting PowerPlay data that this
    tool supports:

    \b
     - By extracting PowerPlay table from Video ROM image (see extract command)
     - Import "Soft PowerPlay" table from Windows registry, directly from
       offline Windows/System32/config/SYSTEM file on disk, so it would work
       from Linux distro that has acces to mounted Windows partition
       (path to SYSTEM registry file is specified with --from-registry option)
     - Import "Soft PowerPlay" table from "More Powe Tool" MPT file
       (path to MPT file is specified with --from-mpt option)

    This tool currently supports parsing and modifying PowerPlay tables
    found on the following AMD GPU families:

    \b
      - Polaris
      - Vega
      - Radeon VII
      - Navi 10, 12, 14
      - Navi 21, 22, 23
      - Navi 3x (experimental)

    Note: iGPUs found in many recent AMD APUs are using completely different
    PowerPlay control methods, this tool does not support them.

    If you have bugs to report or features to request please check:

      github.com/sibradzic/upp
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['PPBINARY'] = pp_file
    ctx.obj['FROMREGISTRY'] = from_registry
    ctx.obj['FROMMPT'] = from_mpt


@click.command(short_help='Show UPP version.')
def version():
    """Shows UPP version."""
    version = importlib.metadata.version('upp')
    click.echo(version)


@click.command(short_help='Dumps all PowerPlay parameters to console.')
@click.option('--raw/--no-raw', '-r/ ', help='Show raw binary data.',
              default='False')
@click.pass_context
def dump(ctx, raw):
    """Dumps all PowerPlay data to console

    De-serializes PowerPlay binary data into a human-readable text output.
    For example:

    \b
        upp --pp-file=radeon.pp_table dump

    In standard mode all data will be dumped to console, where
    data tree hierarchy is indicated by indentation.

    In raw mode a table showing all hex and binary data, as well
    as variable names and values, will be dumped.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']
    from_registry = ctx.obj['FROMREGISTRY']
    from_mpt = ctx.obj['FROMMPT']
    if from_registry:
        pp_file = _get_pp_data_from_registry(from_registry)
    if from_mpt:
        pp_file = _get_pp_data_from_mpt(from_mpt)
    decode.dump_pp_table(pp_file, rawdump=raw, debug=debug)
    return 0


@click.command(short_help='Undumps all PowerPlay parameters to a binary' +
                          'PP Table file or a Registry')
@click.option('-d', '--dump-filename',
              help='File path of dumped powerplay parameters.')
@click.option('-t', '--to-registry', metavar='<filename>',
              help='Output to Windows registry .reg file.')
@click.option('-w', '--write', is_flag=True,
              help='Write changes to PP binary.', default=False)
@click.pass_context
def undump(ctx, dump_filename, to_registry, write):
    """Undumps all PowerPlay data to pp file or registry

    Serializes previously dumped PowerPlay text to pp file or registry.
    For example:

    \b
        upp --pp-file=radeon.pp_table undump -d pp.dump --write

    """
    variable_set = _load_variable_set(dump_filename)
    ctx.invoke(set, variable_path_set=variable_set,
               to_registry=to_registry, write=write)
    return 0


@click.command(short_help='Extract PowerPlay table from Video BIOS ROM image.')
@click.option('-r', '--video-rom', required=True, metavar='<filename>',
              help='Input Video ROM binary image file.')
@click.pass_context
def extract(ctx, video_rom):
    """Extracts PowerPlay data from full VBIOS ROM image

    The source video ROM binary must be specified with -r/--video-rom
    parameter, and extracted PowerPlay table will be saved into file
    specified with -p/--pp-file. For example:

    \b
        upp --pp-file=extracted.pp_table extract -r VIDEO.rom

    Default output file name will be an original ROM file name with an
    additional .pp_table extension.
    """
    pp_file = ctx.obj['PPBINARY']
    ctx.obj['ROMBINARY'] = video_rom
    # Override default, we don't want to extract any random VBIOS into sysfs
    if pp_file.endswith('device/pp_table'):
        pp_file = video_rom + '.pp_table'
    msg = "Extracting PP table from '{}' ROM image..."
    print(msg.format(video_rom))
    if decode.extract_rom(video_rom, pp_file):
        print('Done')

    return 0


@click.command(short_help='Inject PowerPlay table into Video BIOS ROM image.')
@click.option('-i', '--input-rom', required=True, metavar='<filename>',
              help='Input Video ROM binary image file.')
@click.option('-o', '--output-rom', required=False, metavar='<filename>',
              help='Output Video ROM binary image file.')
@click.pass_context
def inject(ctx, input_rom, output_rom):
    """Injects PowerPlay data from file into VBIOS ROM image

    The input video ROM binary must be specified with -i/--input-rom
    parameter, and the output ROM can be specified with an optional
    -o/--output-rom parameter.

    \b
        upp -p modded.pp_table inject -i original.rom -o modded.rom

    The output filename defaults to <input ROM file name>.modded.

    WARNING: Modified vROM image is probalby not going to work if flashed as
    is to your card, due to ROM signature checks on recent Radeon cards.
    Authors of this tool are in no way responsible for any damage that may
    happen to your expansive graphics card if you choose to flash the modified
    video ROM, you are doing it entierly on your own risk.
    """
    pp_file = ctx.obj['PPBINARY']
    if not output_rom:
        output_rom = input_rom + '.modded'
    msg = "Injecting {} PP table into {} ROM image..."
    print(msg.format(pp_file, input_rom))
    if decode.inject_pp_table(input_rom, output_rom, pp_file):
        print('Saved modified vROM image as {}.'.format(output_rom))

    return 0


@click.command(short_help='Get current value of a PowerPlay parameter(s).')
@click.argument('variable-path-set', nargs=-1, required=True)
@click.pass_context
def get(ctx, variable_path_set):
    """Retrieves current value of one or multiple PP parameters

    The parameter variable path must be specified in
    "/<param> notation", for example:

    \b
        upp get /FanTable/TargetTemperature /VddgfxLookupTable/7/Vdd

    The raw value of the parameter will be retrieved,
    decoded and displayed on console.
    Multiple PP parameters can be specified at the same time.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']
    from_registry = ctx.obj['FROMREGISTRY']
    if from_registry:
        pp_file = _get_pp_data_from_registry(from_registry)
    pp_bytes = decode._read_binary_file(pp_file)
    data = decode.select_pp_struct(pp_bytes, debug=debug)

    for set_pair_str in variable_path_set:
        var_path = _normalize_var_path(set_pair_str)
        res = decode.get_value(pp_file, var_path, data, debug=debug)
        if res:
            print('{:n}'.format(res['value']))
        else:
            print('ERROR: Incorrect variable path:', set_pair_str)
            exit(2)

    return 0


@click.command(short_help='Set value to PowerPlay parameter(s).')
@click.argument('variable-path-set', nargs=-1, required=False)
@click.option('-w', '--write', is_flag=True,
              help='Write changes to PP binary.', default=False)
@click.option('-t', '--to-registry', metavar='<filename>',
              help='Output to Windows registry .reg file.')
@click.option('-c', '--from-conf', metavar='<filename>',
              help='Input VARIABLE_PATH_SET from file.')
@click.pass_context
def set(ctx, variable_path_set, to_registry, write, from_conf):
    """Sets value to one or multiple PP parameters

    The parameter path and value must be specified in
    "/<param>=<value> notation", for example:

    \b
        upp set /PowerTuneTable/TDP=75 /SclkDependencyTable/7/Sclk=107000

    Multiple PP parameters can be set at the same time.
    The PP tables will not be changed unless additional
    --write option is set.

    It is possible to set parameters from a configuration file with one
    "/<param>=<value>" per line using -c/--from-conf instead of directly
    passing parameters from command line

    \b
        upp set --from-conf=card0.conf

    Optionally, if -t/--to-registry output is specified, an additional Windows
    registry format file with '.reg' extension will be generated, for example:

    \b
        upp set /PowerTuneTable/TDP=75 --to-registry=test

    will produce the file test.reg in the current working directory.
    """
    debug = ctx.obj['DEBUG']
    pp_file = ctx.obj['PPBINARY']

    if from_conf is not None:
        if (len(variable_path_set) > 0):
            print("ERROR: VARIABLE_PATH_SET found when using -c/--from-conf.")
            exit(2)
        if not os.path.isfile(from_conf):
            print("ERROR: file {} not found.".format(from_conf))
            exit(2)
        with open(from_conf, 'r') as config:
            variable_path_set = list(filter(''.__ne__,
                                            config.read().splitlines()))
    elif (len(variable_path_set) == 0):
        print("ERROR: no parameters given to set to pp table.")
        exit(2)

    set_pairs = []
    for set_pair_str in variable_path_set:
        var, val = _validate_set_pair(set_pair_str)
        if var and val:
            var_path = _normalize_var_path(var)
            res = decode.get_value(pp_file, var_path)
            if res:
                if res["type"] == 'f':
                    set_pairs += [var_path + [float(val)]]
                else:
                    set_pairs += [var_path + [int(val)]]
            else:
                print('ERROR: Incorrect variable path:', var)
                exit(2)
        else:
            exit(2)

    pp_bytes = decode._read_binary_file(pp_file)
    data = decode.select_pp_struct(pp_bytes)

    for set_list in set_pairs:
        decode.set_value(pp_file, pp_bytes, set_list[:-1], set_list[-1],
                         data_dict=data, write=False, debug=debug)
    if write:
        print("Committing changes to '{}'.".format(pp_file))
        decode._write_binary_file(pp_file, pp_bytes)
    else:
        print("WARNING: Nothing was written to '{}'.".format(pp_file),
              "Add --write option to commit the changes for real!")
    if to_registry:
        _write_pp_to_reg_file(to_registry + '.reg', pp_bytes, debug=debug)

    return 0


cli.add_command(extract)
cli.add_command(inject)
cli.add_command(dump)
cli.add_command(undump)
cli.add_command(get)
cli.add_command(set)
cli.add_command(version)


def main():
    cli(obj={})()


if __name__ == "__main__":
    main()
