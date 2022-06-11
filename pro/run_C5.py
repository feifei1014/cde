#!/usr/bin/env python3

import os
import glob
import re
import logtools
import pipe_commandline

class args_wrap:
    '''
    python pipe_commandline.py -i /data/wangxia/C5/FLT/MSC_0000000/CSST_MSC_MS_SCI_20240617065639_20240617065909_100000000_01_L0_1_flt.fits -o /data/yhsong/20220526/output/MSC_0000000 -m 2 -c /data/zhangx/ImgSimData/C5data/NGP_AstrometryON_shearOFF_Spec_diretImg/MSC_0000000/MSC_100000000_chip_01_filt_i.cat -f ../config -s 3685 -a 5 -w same
    '''
    image=''
    output=''
    mode=2
    catalog=''
    confpath='../config'
    watershed=3685
    aperture=5
    webpath='same'
    expression='True'
    display=False
    no_web=False
    startover=False
    def __init__(self):
        pass
    def set(self, key_value):
        for key in key_value:
            setattr(self, key, key_value[key])

def main(image_root, catalog_root, output_root, key_value={}):
    '''
    '''

    conf_path = '../config'
    image_dirs = glob.glob(os.path.join(image_root,'MSC_0000*'))
    
    args = args_wrap()
    args.set(key_value)

    logtools.log_init(is_display=args.display)

    CC = 'python'
    CMD = f'{CC} pipe_commandline.py -i IMAGE -o OUTPUT -m 2 -c CATALOG -f {conf_path} -s 3685 -a 5 -w same '
    
    chip_pattern = re.compile(".*_(.*)_L0.*")
    image_dirs.sort()

    for image_dir in image_dirs:
        sub_path,sub_name = os.path.split(image_dir)
        catalog_path = os.path.join(catalog_root, sub_name)
        outpath = os.path.join(output_root,sub_name)
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        ffs = glob.glob(os.path.join(image_dir,'*.fits'))
        ffs.sort()
        for ff in ffs:
            chip_id = chip_pattern.findall(ff)[0]
            catalog = glob.glob(os.path.join(catalog_path,f'*chip_{chip_id}*.cat'))[0]
            cmd = CMD.replace('IMAGE',ff)
            cmd = cmd.replace('OUTPUT',outpath)
            cmd = cmd.replace('CATALOG',catalog)

            args.image=ff
            args.output = outpath
            args.catalog = catalog
            #print (cmd)
            #pipe_commandline.main(args)
            #continue
            try:
                pipe_commandline.main(args)
            except:
                pass
if __name__ == '__main__':
    image_root = '/data/wangxia/C5/FLT'
    catalog_root = '/data/zhangx/ImgSimData/C5data/NGP_AstrometryON_shearOFF_Spec_diretImg'
    output_root = '/data/yhsong/20220526/output'
    main(image_root, catalog_root, output_root)
