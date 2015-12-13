/*
 * Copyright 2012 Open Source Robotics Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
*/

#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/common/UpdateInfo.hh>
#include <gazebo/common/SingletonT.hh>
#include <gazebo/common/Timer.hh>
#include <gazebo/util/UtilTypes.hh>
#include <gazebo/common/common.hh>
#include <iostream>


// For Ach
#include <errno.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <inttypes.h>
#include <ach.h>

// ach channels
ach_channel_t chan_vid_chan;
ach_channel_t user_config_chan;

struct USER_CONFIG {
double pid[3];
double des[2];
char tgt[6];
char flag[1];
};

struct USER_CONFIG user_config; 

void cbVid(ConstImageStampedPtr &_msg)
{
  size_t size;
  // check the robot flag before sending video
  if (user_config.flag[0] == 0) {
     ach_put(&chan_vid_chan, _msg->image().data().c_str() , _msg->image().data().size());
  }
}

/////////////////////////////////////////////////
int main(int _argc, char **_argv)
{
  /* open ach channel */
  int r = ach_open(&chan_vid_chan, "robot-vid-chan" , NULL);
  assert( ACH_OK == r );
  r = ach_open(&user_config_chan, "user-config-chan", NULL);
  assert( ACH_OK == r );

  // Load gazebo
  printf("%i\n\r",-1);
  gazebo::load(_argc, _argv);

  printf("%i\n\r",0);
  gazebo::run();

  printf("%i\n\r",1);
  // Create our node for communication
  gazebo::transport::NodePtr node(new gazebo::transport::Node());
  node->Init();

  printf("%i\n\r",2);
  // Listen to Gazebo world_stats topic
  gazebo::transport::SubscriberPtr subL = node->Subscribe("/gazebo/default/PanTiltCam/camLink/cam_sensor1/image", cbVid);

  printf("%i\n\r",3);
  // Busy wait loop...replace with your own code as needed.
  size_t fs;
  while (true) {
    gazebo::common::Time::MSleep(100);
    ach_get( &user_config_chan, &user_config, sizeof(user_config), &fs, NULL, ACH_O_LAST );
  }

  // Make sure to shut everything down.
  gazebo::transport::fini();
}
