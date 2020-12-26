
if [ "$1" == 'help' ]
then
    echo -e "\e[32mThe script used the following positioning arguments.
    1) Python executable path, if you are using conda environment on Ubuntu, then it should be like /home/<user_name>/anaconda3/envs/<environment name>/bin/python. Replace the <user_name> and <environment_name> with the corresponding values.
    2) Path to the video file
    3) Path to the calibration.pkl file (if not provided, the system will ask you to perform calibration first)

    Example (no calibration file path is provided): ./runme.sh /home/maaz/anaconda3/bin/python /home/maaz/video.mp4
    Example (calibration file path is provided): ./runme.sh /home/maaz/anaconda3/bin/python /home/maaz/video.mp4 /home/maaz/calibration.pkl\e[0m"
    exit
fi

PYTHON_PATH=$1
VIDEO_PATH=$2
CALIBRATION_FILE_PATH=$3

# Change the working directory to the directory containing the bash script (runme.sh)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR" || exit

#!/bin/sh
# Check if PYTHON path is provided
if [ -z "$PYTHON_PATH" ]
then
  echo -e "\e[31mPYTHON_PATH is not provided.
Please provide the python executable path as the first argument to the script.
Run './runme.sh help' for more details. Exiting.\e[0m"
  exit
fi


# Check if the user provided the calibration
if [ -z "$CALIBRATION_FILE_PATH" ]
then
  echo -e "\e[31mYou have not provided calibration file path. You will now be asked to perform the calibration.\e[0m"
  echo -e "\e[32mENTER number of calibration points for camera view to top view transformation.\e[0m"
  read -r num_points
  echo -e "\e[32mENTER number of iterations for pixel to feet scale factor estimation\e[0m.
Note that this the number of times you will mark the approx. 6 feet distance on the camera view image.
It is prefer to mark the points on the head and foot of the persons in the frame assuming that on average a person will be of around 6 feet tall"
  read -r iterations
  echo -e "Perfoming calibration..."
  $PYTHON_PATH calibrate.py -v "$VIDEO_PATH" -n "$num_points" -iter "$iterations"
  # Run the social distancing violation detection script
  echo -e "Running social distancing violation detection logic on the video $VIDEO_PATH..."
  $PYTHON_PATH violation_detector.py -v "$VIDEO_PATH"
else
  echo -e "\e[32mThe provided calibration pkl file path is $CALIBRATION_FILE_PATH. The calibration step will be skipped.\e[0m"
  echo -e "\e[31mIf you want to perform the calibration again, please don't provide the third argument to the script.\e[0m"
  echo -e "Running social distancing violation detection logic on the video $VIDEO_PATH..."
  $PYTHON_PATH violation_detector.py -v "$VIDEO_PATH" -c "$CALIBRATION_FILE_PATH"
fi

echo -e "\e[32mThe output video is saved in the same directory containing the video file. Thank you!\e[0m"