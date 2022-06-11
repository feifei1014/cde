#!/usr/bin/env python
import argparse
import run_C5

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--image_path",type=str,default='',help='the image root path')
    parser.add_argument("-c","--catalog_path",type=str,default='',help="catalog root path")
    parser.add_argument("-o","--output_path",type=str,default='',help="output path")
    parser.add_argument("-a","--aperture",type=int,default=5,help="aperture size")
    parser.add_argument('--no_web', action='store_true', help='Do not generate web page and plots.')
    parser.add_argument('--startover', action='store_true', help='Force to run all program, ignoring any existing temporary files.')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    image_root = '/data/wangxia/C5/FLT'
    catalog_root = '/data/zhangx/ImgSimData/C5data/NGP_AstrometryON_shearOFF_Spec_diretImg'
    output_root = '/data/yhsong/20220526/output'
    args = init()
    image_root = args.image_path
    catalog_root = args.catalog_path
    output_root = args.output_path
    d = {}
    d['no_web'] = args.no_web
    d['startover'] = args.startover
    d['aperture'] = args.aperture
    run_C5.main(image_root, catalog_root, output_root,d)
