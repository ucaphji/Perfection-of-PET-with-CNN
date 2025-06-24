#$ -S /bin/bash
#$ -l h_vmem=2G
#$ -l tmem=2G
#$ -l h_rt=03:00:00
#$ -cwd
#$ -j y
#$ -t 1-500:1
#$ -tc 500
#$ -N VoxLung

if [ "$#" -ne 1 ]; then
    echo "Required argument: Radionuclide"
else

radionuclide=$1
TASK_ID=$SGE_TASK_ID


# Sleep for up to 5 minutes to stagger executable loading

SLEEPTIME=$((1 + RANDOM % 300))

echo "Sleeping ${SLEEPTIME} seconds"

sleep ${SLEEPTIME}



echo "Script initialised:" `date +%d.%m.%y-%H:%M:%S`

Gate main.mac -a [SimuId,$TASK_ID] | grep "annihil" >> annihil_${radionuclide}_${SGE_TASK_ID}.txt

tail -n +2 annihil_${radionuclide}_${SGE_TASK_ID}.txt | awk '/annihil/{print $2, $3, $4}' > anni_${SGE_TASK_ID}.txt

fi

echo "Script finished: " `date +%d.%m.%y-%H:%M:%S`
