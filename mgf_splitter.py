## This tool is developed by Mr. Sandeep Kasargod and Mr. Chinmaya Narayana K.
## If you have any queries please contact chinmaya_k@yenepoya.edu.in or sandeepk@yenepoya.edu.in 
## This tool is licensed under MIT License
## For more information please visit https://github.com/chinmayaNK22/MGF-file-splitter


import argparse
import os

parser = argparse.ArgumentParser(description='''Extract raw file specific spectra from an unassigned spectra file (.mgf) from Proteome Discoverer and generate new mgf file specific to raw files''')

parser.add_argument('infile', metavar='-ip', type=str, nargs='+', help='MGF file path')

args = parser.parse_args()

dicts_mz = {}
dicts_mz_info = {}
def read_mgf(infile):
    for i in open(infile):
        if "BEGIN IONS" in i.rstrip():
            title = ""
            pepmass = ""
            rt = ""
            charge=""
            scans=""
            lst = []
        if "TITLE" in i.rstrip():
            file_name = i.split('\\')[-1].split(';')[0].replace('"', '')
            title = i.rstrip()
        if "PEPMASS" in i.rstrip():
            pepmass = i.rstrip()
        if "CHARGE" in i.rstrip():
            charge = i.rstrip()
        if "RTINSECONDS" in i.rstrip():
            rt = i.rstrip()
        if "SCANS" in i.rstrip():
            scans = i.rstrip()
        if len(i.rstrip()) > 2 and i.rstrip()[0].isdigit():
            lst.append(i.rstrip())
        if "END IONS" in i.rstrip():
            if file_name not in dicts_mz:
                dicts_mz[file_name] = [lst]
                dicts_mz_info[file_name] = [title + "@" + pepmass + "@" + rt.rstrip() + "@" + charge + "@" + scans]
            else:
                dicts_mz[file_name].append(lst)
                dicts_mz_info[file_name].append(title + "@" + pepmass + "@" + rt + "@" + charge + "@" + scans)

def split_raw_file_spectra(mgf):
    read_mgf(mgf)
    try:
        folder = os.makedirs(mgf.rstrip('.mgf'))
    except:
        print ('Folder ' + mgf.rstrip('.mgf') + ' already present')
    for k, v in dicts_mz.items():
        if k.split('.')[-1] == 'raw':
            outfile = os.path.join(mgf.rstrip('.mgf'),k.rstrip('.raw') + '.mgf') 
            write_file = open(outfile, 'w')
            for iters in range(len(v)):
                dicts_mz_info_1 = dicts_mz_info[k][iters].split('@')
                write_file.write("BEGIN IONS" + '\n')
                write_file.write(dicts_mz_info_1[0]  + '\n')
                write_file.write(dicts_mz_info_1[1]  + '\n')
                write_file.write(dicts_mz_info_1[2]  + '\n')
                write_file.write(dicts_mz_info_1[3]  + '\n')
                write_file.write(dicts_mz_info_1[4]  + '\n')
                for iter_mz in dicts_mz[k][iters]:
                    write_file.write(iter_mz  + '\n')
                write_file.write("END IONS" + "\n")
            write_file.close()
            
        elif k.split('.')[-1] == 'mgf':
            outfile = os.path.join(mgf.rstrip('.mgf'),k) 
            write_file = open(outfile, 'w')
            for iters in range(len(v)):
                dicts_mz_info_1 = dicts_mz_info[k][iters].split('@')
                write_file.write("BEGIN IONS" + '\n')
                write_file.write(dicts_mz_info_1[0]  + '\n')
                write_file.write(dicts_mz_info_1[1]  + '\n')
                write_file.write(dicts_mz_info_1[2]  + '\n')
                write_file.write(dicts_mz_info_1[3]  + '\n')
                write_file.write(dicts_mz_info_1[4]  + '\n')
                for iter_mz in dicts_mz[k][iters]:
                    write_file.write(iter_mz  + '\n')
                write_file.write("END IONS" + "\n")
            write_file.close()
    
split_raw_file_spectra(args.infile[0])                     
    
