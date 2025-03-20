import damv1manipulation as mpl
from .mytime7 import currentTime7 as cT7
from .mylogger import logger

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


def printlf_dump_v1(_writeOnFile, _fullfilename='', _file=None, *_messaagePrintlf, **kwargs):
    f = _file
    text_message = ''
    if len(_messaagePrintlf) != 0:
        text_message = ' '.join(_messaagePrintlf)
        text_message = str(text_message).rstrip()  # Menghapus spasi di akhir

        # Log pesan ke console menggunakan logger
        logger(cT7(), text_message)

        # Jika _writeOnFile adalah True, tulis pesan ke file
        if _writeOnFile:
            if f is None:
                try:
                    f = open(_fullfilename, 'w')  # Buka file dalam mode write
                    f.write(cT7() + '\n')  # Tulis timestamp ke file
                except Exception as e:
                    print(f"Error opening file: {e}")
                    return None
            try:
                f.write(cT7() + ' ' + text_message + '\n')  # Tulis pesan ke file
            except Exception as e:
                print(f"Error writing to file: {e}")
                return None
            finally:
                if f is not None:
                    f.close()  # Pastikan file ditutup setelah selesai
                    return _fullfilename  # Kembalikan path file sebagai indikasi keberhasilan
    return None