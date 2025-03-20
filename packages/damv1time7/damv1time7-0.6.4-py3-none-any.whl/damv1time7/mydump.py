import traceback
import damv1manipulation as mpl
from .mytime7 import currentTime7 as cT7
from .mylogger import logger


# #Konfigurasi versi 0.5.13
# def printlf_dump_v1(_writeOnFile, _fullfilename = '', _file = None, *_messaagePrintlf, **kwargs):
#     f = _file
#     text_message = ''
#     if len(_messaagePrintlf)!=0:
#         text_message = ' '.join(_messaagePrintlf)
#         text_message = str(text_message.removesuffix('\n')).rstrip()

#         logger(cT7(), text_message)
#         if _writeOnFile == True:
#             if f == None: 
#                 f = open(_fullfilename,'w')
#                 f.write(cT7());f.write('\n')
#             f.write(cT7() + ' ' + text_message + '\n')
#     return f


def printlf_dump_v1(_writeOnFile, _fullfilename='', *_messagePrintlf):
    if not _messagePrintlf:
        return None  # Tidak ada pesan, tidak perlu lanjut

    text_message = ' '.join(_messagePrintlf).rstrip()
    logger(cT7(), text_message)  # Log ke console

    if _writeOnFile:
        if not _fullfilename:
            print("Gagal: Nama file kosong.")
            return None

        try:
            with open(_fullfilename, 'a') as f:
                f.write(f"{cT7()} {text_message}\n")
            return _fullfilename  # Indikasi sukses
        except Exception as e:
            print(f"Gagal menulis ke file: {e}")
            print(traceback.format_exc())  # Detail error
            return None

    return None