
import argparse
import find_config
import agent_config
import logtools
import numpy as np
from logtools import LogDecorator, logger
import os
import one_image 
import make_html 

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--image",type=str,default='',help='the image file')
    parser.add_argument("-o","--output",type=str,default='',help="output path or address")
    parser.add_argument("-m","--mode", type=int,default=2,help="1 for one direction or 2 for bidirection")
    parser.add_argument("-c","--catalog", type=str,default='',help="catalog file")
    parser.add_argument("-f","--confpath",type=str, default='../config',help="config path")
    parser.add_argument("-s","--watershed",type=int,default=3685,help="watershed of the ccd")
    parser.add_argument("-a","--aperture",type=int,default=5,help="aperture size")
    parser.add_argument("-w","--webpath",type=str, default='same',help="the path of web page")
    parser.add_argument("-e","--expression",type=str, default="True",help='expression is a filter. example:  "identify>18000 and identify <19000" keywords: identify, mag, x0, y0. Default run all identifies.')
    parser.add_argument('--display', action='store_true', help='Display logs')
    parser.add_argument('--no_web', action='store_true', help='Do not generate web page and plots.')
    parser.add_argument('--startover', action='store_true', help='Force to run all program, ignoring any existing temporary files.')
    args = parser.parse_args()
    return args
        
def main(args):

    
    ff_image = args.image
    ff_catalog = args.catalog
    aperture = int(args.aperture)
    config = agent_config.agent_config(args.confpath, args.mode, args.watershed)
    webpath = args.webpath
    expression = args.expression
    

    if os.path.isdir(args.output):
        f_raw = os.path.split(args.image)[1]
        ff_output = os.path.join(args.output, f_raw)
        ff_output = ff_output.replace('.fits','_cde.fits')
    else:
        ff_output = args.output
    
    t_image = os.path.getmtime(ff_image)
    t_catalog = os.path.getmtime(ff_catalog)
    #t_config = config.getmtime()

    #logger(f'extracting spectra {f_raw}',color='b')
    logger(f'output name: {ff_output}')
    if os.path.exists(ff_output):
        t_output = os.path.getmtime(ff_output)
    else:
        t_output = -1
    if t_output <  np.max([t_image, t_catalog]) or args.startover:
        one_image.one_image(ff_image = ff_image, 
                            ff_catalog = ff_catalog, 
                            config = config, 
                            aperture = aperture, 
                            ff_output = ff_output, 
                            expression = expression
                            )
    else:
        logger('The extracting spectra exists.')

    logger(f'Going to generate web page')
    #return
    if not args.no_web:# 
        if webpath.lower() == 'same': # path is the same with ff_output 
            #webpath = os.path.join(os.path.split(ff_output)[0],'html')
            webpath = ff_output.replace('.fits','.webpage')
        if not os.path.exists(webpath):
            os.mkdir(webpath)
        logger('plot and make html web page',color='g')
        #web_path,ff_image, aperture, ff_output, ff_info
        ff_info = ff_output.replace('.fits','.info')
        make_html.make_html(web_path = webpath,
                            ff_image = ff_image, 
                            aperture = aperture, 
                            ff_output = ff_output,
                            ff_info = ff_info,
                            startover=args.startover)

        index_path = ff_output.replace('.fits','.html')
        redirection = os.path.join(os.path.split(webpath)[1],'index_0001.html')
        with open(index_path,'w') as outff:
            for line in open('index.html'):
                outff.write(line.replace('WEBPAGE',redirection))
        
    
if __name__ == '__main__':
    args = init()
    #logtools.log_init(level=logging.DEBUG, is_display=args.display)
    logtools.log_init(is_display=args.display)
    main(args)
    logtools.function_stat()


