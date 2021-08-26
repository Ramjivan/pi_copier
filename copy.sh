#!/bin/bash


#get all flesh drives in an array
media="/media/pi"
echo $(ls $media > drives.txt)

a=0
drives="/home/pi/drives.txt"
  while IFS= read -r line
    do  if [ "$line" == "SETTINGS" ]; then
        echo "x has the value 'valid'"
         continue
        fi
	temp="$media"
	temp+="/"
	temp+="$line"
	usb[$a]=$temp
        echo ${usb[$a]}
        let a+=1    
    done <"$drives"

#Getting all the sub dirctories
cd "src"
echo | ls > /home/pi/dir.txt
cd ..

i=0

for d in ${usb[@]} 
do
bash /home/pi/cpo.sh $d &
pIdArray[i]=$!
let i+=1
done

for i in ${pIdArray[@]}
do
	wait $i
done

exit 0
