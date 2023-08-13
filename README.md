# TransClone: A Language Agnostic Code Clone Detector

### Requirements
- Make sure that you have both client and dev version of [srcML](https://www.srcml.org/#download)
- Transcoder is already provided in this repository.
- The tool was developed and tested on machines with GPU, Nvidia RTX3080 and RTX3080ti.
- It works on CPU only machines too, however, GPU is preffered.
- It currently supports Java and Python.

### Run the following to set up the dependencies

```
setup.sh 
srcml_dep.sh

cd /usr/lib/x86_64-linux-gnu/
sudo ln -s libclang-10.so.1 libclang-14.so
```

### To run the tool

- Through the shell script, [transclone.sh](transclone.sh) [Preferred]
- Or the python script, [gmn_pipeline.py](gmn_pipeline.py)



#### Contact

Subroto Nag Pinku, 
E-mail: [subroto.npi@usask.ca](mailto:subroto.npi@usask.ca) 
