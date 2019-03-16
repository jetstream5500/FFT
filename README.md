# FFT
Building an FFT Algorithm

## General Usage
`fft.c` = Contains the code for the fft (Cooley-Tukey) and dft algorithm  
`fft_test.c` = Testing file (must be compiled with `fft.c`)  
`fft.so` = shared object file used for importing in `python`  
`r2fft.py` = `python` wrapper around the `fft` function in `fft.c`  
`plot.py` = Testing of artificial signal data, and plotting in Matplotlib  
    (`python plot.py <i_data_file> <i_plot_filename> <o_data_file> <o_plot_filename>`,  
      ex: `python plot.py data.csv graph.png transform.csv graph2.png`)  
`sd_test.py` = Generates spectogram (to run simply type `python sd_test.py`)  
`animation.py` = A testing python file for updating an `imshow` in Matplotlib using `blit`  
