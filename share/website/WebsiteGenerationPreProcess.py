import zipfile
import glob, os
import shutil

"""
Author: Lucas Marin
Date: 4/24/2019
So we're currently phasing out and replacing a lot of Java code that helped run biogears, however for website
generation we still rely on a big chunk of java code that calls C++ hooks, if you want to see precisely which
Java functions are called, take a look at biogears/core/projects/java/biogears/CMakeLists.txt, ctrl+f 'gen-website-docs'.

The point of this file is to facilitate generating our website by zipping/moving files to the place
where doxygen expects to find them.

This file lives in core/share/website, if you want to modify it you should modify it there, not in runtime, then 
configure/generate with CMake and build. 
"""

# This is a list of directories that cmd_bio writes out to when we run scenarios
# These paths are relative to runtime_dir
directories = ['/Scenarios/Patient',
               '/Scenarios/Validation',
               '/Scenarios/Showcase',
               '/Scenarios/EnergyEnvironment',
               '/Scenarios/Compartments',
               '/Scenarios/Miscellaneous',
               '/Scenarios/Combined',
               '/Scenarios/ConsumeMeal',
               '/Scenarios/Drug',
               '/Scenarios/AnesthesiaMachine']

#runtime_dir is something like d:/biogears/core/build/runtime
runtime_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(runtime_dir)
print(runtime_dir)

# doxygen expects the files generated by cmd_bio to be zipped, this for loop does that
for dir in directories:
     os.chdir(runtime_dir + dir)
     dir_path = os.path.dirname(os.path.realpath(__file__))
     print(dir_path)
     if not os.path.exists('baselines'):
          os.mkdir('baselines')
     for file in glob.glob('*.csv'):
          print("  "+file)
          zip_name = 'baselines/' + file.split('.')[0] + '.zip'
          file_name = file
          zipfile.ZipFile(zip_name,mode='w').write(file)

# doxygen looks for the files in Drug/baselines in Validation/baselines, this block of
# code moves the files so that doxygen can find them
print("")
os.chdir(runtime_dir + "/Scenarios")
print(os.path.dirname(os.path.realpath(__file__)))
for file in glob.glob(os.path.join(runtime_dir,'/Scenarios/Drug/baselines/','*.*')):
     print(file)
     shutil.copy(file,runtime_dir+'/Scenarios/Validation/baselines')

# There's a bunch of files that we don't seem to regenerate, they're in core/share/website,
# and get copied into runtime, the following code then moves them all to the directory doxygen looks in
print("")
os.chdir(runtime_dir)
for file in glob.glob(os.path.join(runtime_dir,'*PatientValidationTable.md')):
     print(file)
     shutil.copy(file,runtime_dir+'/validation')
     print("")

os.chdir(runtime_dir)
for file in glob.glob(os.path.join(runtime_dir,'*ValidationResults.zip')):
     print(file)
     shutil.copy(file,runtime_dir+'/Scenarios/Validation/baselines')
     print("")

if not os.path.exists('UnitTests'):
     os.mkdir('UnitTests')

os.chdir(runtime_dir+'/UnitTests')     
if not os.path.exists('BioGearsTests'):
     os.mkdir('BioGearsTests')

os.chdir(runtime_dir+'/UnitTests/BioGearsTests')
if not os.path.exists('baselines'):
     os.mkdir('baselines')

os.chdir(runtime_dir)
shutil.copy('RenalTGFFeedbackOutput.zip',runtime_dir+'/UnitTests/BioGearsTests/baselines')
shutil.copy('SimpleDiffusionFourCompartmentTest.zip',runtime_dir+'/UnitTests/BioGearsTests/baselines')
shutil.copy('RespiratoryValidationPFT@120.02s.xml',runtime_dir+'/Scenarios/Validation')

print("Preprocess successful")