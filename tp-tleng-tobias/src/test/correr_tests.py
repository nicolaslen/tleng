import os
import subprocess
import unittest

# Para poder usar los asserts de unittest
tc = unittest.TestCase('__init__')
tc.maxDiff = None

# Podria haberse hecho con las suites de unittest pero por alguna razón misteriosa, no lo hicimos


def print_status_message(filename, status_message):
    MAX_COL_WIDTH = 75
    PADDING = 5

    file_name = "----------- %s -------------- " % filename.upper()
    justfied_message = file_name.ljust(MAX_COL_WIDTH + PADDING, '.') + ' ' + status_message
    print(justfied_message)


def print_OK(filename):
    print_status_message(filename, 'TEST OK')


def print_OK_sin_archivo_de_comparacion(filename):
    print_status_message(filename, 'TEST OK - SIN ARCHIVO DE COMPARACION')


def print_FAIL_mismatch(filename):
    print_status_message(filename, '!!TEST FAIL!! SALIDAS DIFIEREN')


def print_FAIL_archivo_no_generado(filename):
    print_status_message(filename, '!!TEST FAIL!! OUTPUT NO GENERADO')


def print_FAIL_test_debia_fallar(filename):
    print_status_message(filename, '!!TEST FAIL!! NO PRODUJO EXCEPCION')


def assert_la_salida_debe_ser_correcta(filename, out_filename):
    try:
        assert_la_salida_es_igual_a_la_de_la_cateadra(filename, out_filename)
    except FileNotFoundError:
        print_OK_sin_archivo_de_comparacion(filename)


def assert_la_salida_es_igual_a_la_de_la_cateadra(file, out_file):
    with open('archivos/%s' % out_file, 'r') as ideal:
        try:
            with open('salida/%s' % out_file, 'r') as nuestro:
                try:
                    tc.assertEqual(nuestro.read(), ideal.read())
                except AssertionError:
                    print_FAIL_mismatch(file)

                print_OK(file)
        except FileNotFoundError:
            # si existe ideal y no generamos archivo, debería marcar fail
            print_FAIL_archivo_no_generado(file)


def assert_que_debe_fallar_y_el_stderr_debe_tener_algo(file, stderr_output):
    try:
        tc.assertNotEqual(len(stderr_output), 0)
    except AssertionError:
        print_FAIL_test_debia_fallar(file)


def correr_archivo_de_input(filename):
    out_filename = "%so" % filename
    p = subprocess.run(["python", "../SLSParser.py", "-c", "archivos/%s" % filename, "-o", "salida/%s" % out_filename],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_output = p.stdout.decode("utf-8")
    stderr_output = p.stderr.decode("utf-8")
    # print(stdout_output)
    # print(stderr_output)
    verificar_correctitud_del_parseo(filename, out_filename, stderr_output)


def verificar_correctitud_del_parseo(filename, out_file, stderr_output):
    if "FALLA" in filename:
        assert_que_debe_fallar_y_el_stderr_debe_tener_algo(filename, stderr_output)
        print_OK(filename)
    else:
        assert_la_salida_debe_ser_correcta(filename, out_file)


def borrar_salidas():
    directorio_outputs = "./salida"
    for output_file in os.listdir(directorio_outputs):
        os.remove(os.path.join(directorio_outputs, output_file))


def test_todo():
    borrar_salidas()
    archivos_de_input = filter(lambda f: f.endswith(".i"), os.listdir("./archivos"))
    for filename in archivos_de_input:
        correr_archivo_de_input(filename)


test_todo()
