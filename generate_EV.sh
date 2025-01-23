#!/bin/sh
# Matt Probert 01/12/2016

run=Si
ref_value=3.78
echo 'Generating energy-volume data for '$run

#check correct input files exist
if [ ! -e ${run}.cell ] ; then
   echo '   missing '${run}.cell
   exit 1
fi
if [ ! -e ${run}.param ] ; then
   echo '   missing '${run}.param
   exit 2
fi
check_ref=`grep -c $ref_value ${run}.cell` 
if [ $check_ref -lt 1 ]; then
   echo '   missing ref_value in '${run}.cell
   exit 3
fi

#clean up before starting the work
rm -f ${run}_EV.castep

#set up the range of lattice parameters to test
for a in 3.60 3.65 3.70 3.75 3.80 3.85 3.90 3.95 4.00 ; do
    echo '   doing a= '$a
    #replace every occurrence of the 'reference value' by 'a'
    sed -e 's/'$ref_value'/'$a'/g' ${run}.cell > ${run}_EV.cell
    #do the work
    
    mpirun -np 4 castep.mpi ${run}_EV
done

#analyse the runs and extract the values we need into a single results file
grep 'cell volume' ${run}_EV.castep | awk '{print $5}' > V
grep 'Final energy' ${run}_EV.castep | awk '{print $5}' > E
paste V E > ${run}_EV.dat
rm V E
echo 'finished with results in '${run}_EV.dat

num_atoms=`grep "Total number of ions" ${run}_EV.castep | head -1 | awk '{print $8}'`
echo 'NB each run contains '${num_atoms}' atoms'
