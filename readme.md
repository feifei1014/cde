
## run a single image
pro/pipe_commandline.py
the arguments of this program will be shown if you type:
python pipe_commandline.py --help


## run a batch images
pro/run_C5_args.py

a example of this file:
pro/run_C5.sh

```
python run_C5_args.py -o /data/yhsong/C5_output -i /data/wangxia/C5/FLT -c /data/zhangx/ImgSimData/C5data/NGP_AstrometryON_shearOFF_Spec_diretImg --no_web --startover
```

--no_web means this program will not plot any figure.
It will be much faster than generating web page version.

--startover means all image will be extracted. If there is
no this keywords, the worked images will be passed. 
