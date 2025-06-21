def createH33Header(size,width,inputfilename,outputfilename):
    fid = open(outputfilename,'w');

    sizex=size[0]
    sizey=size[1]
    sizez=size[2]

    widthx=width[0]
    widthy=width[1]
    widthz=width[2]

    # Base

    base = '!INTERFILE  :=\n' + \
            'name of data file := %s\n'+\
            '!GENERAL DATA :=\n'+\
            '!GENERAL IMAGE DATA :=\n'+\
            '!type of data := PET\n'+\
            'imagedata byte order := LITTLEENDIAN\n'+\
            '!PET STUDY (General) :=\n'+\
            '!PET data type := Image\n'+\
            'process status := Reconstructed\n'+\
            '!number format := float\n'+\
            '!number of bytes per pixel := 4\n'+\
            'number of dimensions := 3\n'+\
            'matrix axis label [1] := x\n'+\
            '!matrix size [1] := %d\n'+\
            'scaling factor (mm/pixel) [1] := %g\n'+\
            'matrix axis label [2] := y\n'+\
            '!matrix size [2] := %d\n'+\
            'scaling factor (mm/pixel) [2] := %g\n'+\
            'matrix axis label [3] := z\n'+\
            '!matrix size [3] := %d\n'+\
            'scaling factor (mm/pixel) [3] := %g\n'+\
            '!number of slices := %d\n'+\
            'slice thickness (pixels) := %g\n'+\
            'number of time frames := 1\n'+\
            '!END OF INTERFILE :=\n'

    fid.write(base % (inputfilename,sizex,widthx,sizey,widthy,sizez,widthz,sizez,widthz));

    fid.close();
    return