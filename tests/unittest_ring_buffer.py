import unittest
import ctypes
import io

# local for testing c code
import c_test

# file name without .c
FILE_TO_TEST = "ring_buffer"

class TestBuffer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''class fixing all tests in class

        copy file and compile it
        load shared library
        '''

        c_test.compile(FILE_TO_TEST)
        # load shared library
        cls.lib_rb = ctypes.CDLL(f"./{FILE_TO_TEST}.so")

    @classmethod
    def tearDownClass(cls):
        '''removed copied and compiled file
        '''

        c_test.clean_file(FILE_TO_TEST)

    def setUp(self):
        '''fixture every test before start

        setting arguments type
        setting return type
        '''
        # set arguments and return types for functions
        self.lib_rb.buffer_put.argtypes = (ctypes.c_char,)
        self.lib_rb.buffer_put.restype = None

        self.lib_rb.buffer_pop.argtypes = None 
        self.lib_rb.buffer_pop.restype = ctypes.c_char

        self.lib_rb.clear.restype = None
        self.lib_rb.clear.argtypes = None

        # clear buffer
        self.lib_rb.clear()

    def test_hello(self):
        '''check basic put and pop from buffer

        put Hello to a buffer char by char
        pop 5 char from buffer
        check if both string are the same
        '''

        hw = "Hello"
        for char in hw:
            self.lib_rb.buffer_put(char.encode('UTF-8'))
        ans = ""
        for char in hw:
            ans = ans + (self.lib_rb.buffer_pop().decode('utf-8'))
        self.assertEqual(hw, ans)

    def test_clear(self):
        '''test functions for clear buffer

        put some data, check buffer value
        check put_position
        pop some data, check pop_position
        clear buffer, check buffer value,
            put_position, pop_position
        '''

        # put some values in buffer
        some_word = "test"
        for char in some_word:
            self.lib_rb.buffer_put(char.encode('UTF-8'))

        # check buffer value
        buf_dump = check_buffer(self.lib_rb)['buffer']
        self.assertEqual(some_word, buf_dump)

        # check put_position
        buf_dump = check_buffer(self.lib_rb)['put_position']
        self.assertEqual(len(some_word), int(buf_dump))

        # pop value (we don't need return value)
        self.lib_rb.buffer_pop()

        # check pop_position
        buf_dump = check_buffer(self.lib_rb)['pop_position']
        self.assertEqual(1, int(buf_dump))

        # clean buffer 
        self.lib_rb.clear()

        # check if buffer is empty
        buf_dump = check_buffer(self.lib_rb)
        self.assertEqual("", buf_dump['buffer'])
        self.assertEqual("0", buf_dump['put_position'])
        self.assertEqual("0", buf_dump['pop_position'])

def check_buffer(shared_lib: ctypes.CDLL) -> dict:
    '''wrapper for buffer_dump c functions

    this functions return status of ring buffer written in c

    Args:
        shared_lib: c .so file loaded as CDLL

    Returns:
        dictionary with buffer, put_position and pop_position values

    Examples:
        output depends on actual buffer values, but might look
        like this: 

        {'buffer': 'test',
         'put_position': '4',
         'pop_position': '0'}
    '''
    c_out = io.BytesIO()
    with c_test.stdout_redirector(c_out): 
        shared_lib.dump()
    c_str = c_out.getvalue().decode('utf-8')
    return (parse_clear_stdout(c_str))

def parse_clear_stdout(cstr: str) -> dict:
    '''parse c type stdout from clear function

    Args:
        cstr: string from standard output in clear function

    Returns:
        dictionary with buffer, put_position and pop_position values

    Examples:
        >>> parse_clear_stdout("DEBUG: buffer: test
                                DEBUG: put_position: 4
                                DEBUG: pop_position: 0")
                                
        {'buffer': 'test',
         'put_position': '4',
         'pop_position': '0'}

    '''

    # dictionary for return
    buffer_dump = {}
    for line in cstr.splitlines():
        word = line.split(": ", 2)
        # remove empty lines
        if word[0] == "DEBUG":
            buffer_dump[word[1]] = word[2]
    return(buffer_dump)

if __name__ == "__main__":
    unittest.main(verbosity = 2)
