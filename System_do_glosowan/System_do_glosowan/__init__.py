"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import System_do_glosowan.views
import System_do_glosowan.fun_base
import System_do_glosowan.fun
import System_do_glosowan.fun_mail
import System_do_glosowan.message

app.secret_key = fun.pass_decoder('0110001001001010011110000100001101110000011010010010101001001001011010000011000101001010010100100111011000101011010010110101010001000011001010110110010101110001')