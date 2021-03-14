import re
import docx
import os
import zipfile
import tempfile
import shutil
import io

# pre, ext = os.path.splitext("test2.docx")  # actually.. not needed
# os.rename("test2.docx", "result.zip")  # renaming is not very good idea
# shutil.copyfile("test.docx", "result.zip")
#
#
# # another black box to DELETE file in .zip
# def remove_from_zip(zip_fname, *filenames):
#     tempdir = tempfile.mkdtemp()
#     try:
#         temp_name = os.path.join(tempdir, 'new.zip')
#         with zipfile.ZipFile(zip_fname, 'r') as zip_read:
#             with zipfile.ZipFile(temp_name, 'w') as zip_write:
#                 for item in zip_read.infolist():
#                     if item.filename not in filenames:
#                         data = zip_read.read(item.filename)
#                         zip_write.writestr(item, data)
#         shutil.move(temp_name, zip_fname)
#     finally:
#         shutil.rmtree(tempdir)
#
#
# zipfile_name = "result.zip"
# with zipfile.ZipFile(zipfile_name, 'r') as z:
#     # printing all the contents of the zip file
#     z.printdir()
#     # extracting one file
#     print('\nExtracting word/document.xml file now...')
#     z.extract('word/document.xml')
#     print('Done!')
#     z.close()

# fin = open('word/document.xml', "rt")
# lines = fin.readlines()
# fin.close()
with io.open('word/document.xml', encoding='utf-8') as file:
    print(len(file.readlines()))
    file.close()

# needs_to_be_replaced = ["18234454", "14114836", "5660041", "6278869", "14114836", "5660041", "6278869"]
# needs_to_be_replaced = list(dict.fromkeys(needs_to_be_replaced))  # delete repeats
#
# fout = open("word/document.xml", "wt")
#
# print("\nReplacing...")
# for i, elem in enumerate(needs_to_be_replaced):
#     print("[" + str(i + 1) + "] instead of (" + str(elem) + ")")
#     lines[1] = lines[1].replace(elem, '[' + str(i) + ']')
#     # print(lines[1])
#
# print("Replacing completed!\n\nWriting to file...")
#
# for line in lines:
#     fout.write(line)
#     # print(line)
#
# fout.close()
#
# print("Writing done successfully!\n\nPacking word/document.xml back...")
#
# remove_from_zip(zipfile_name, "word/document.xml")
# with zipfile.ZipFile("result.zip", "a") as z:
#     # writing file
#     z.write("word/document.xml")
#     z.close()
#
# print("document.xml packed successfully!")
#
# os.rename("result.zip", "result.docx")
