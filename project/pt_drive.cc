#include <boost/bind.hpp>
#include <gazebo/gazebo.hh>
#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>
#include <iostream>
#include <gazebo/transport/TransportTypes.hh>
#include <gazebo/msgs/MessageTypes.hh>
#include <gazebo/common/Time.hh>

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
#include <string.h>

// ach channels
ach_channel_t chan_pt_drive_ref;     
ach_channel_t chan_time;
ach_channel_t user_config_chan;
ach_channel_t state_chan;

int debug = 0;
double H_ref[2] = {};
double H_state[2] = {};
double ttime = 0.0;
struct USER_CONFIG {
double pid[3];
double des[2];
char tgt[6];
char flag[1];
};

struct USER_CONFIG user_config; 


namespace gazebo
{   
  class ModelPanTiltDrive : public ModelPlugin
  {

    // Function is called everytime a message is received.
    //void cb(gazebo::msgs::Image &_msg)
    //void cb(const std::string& _msg)
    //void cb(gazebo::msgs::ImageStamped &_msg)
    //void cb(ConstWorldStatisticsPtr &_msg)
    //void cb(const std::string& _msg)
    public: void cb(ConstWorldStatisticsPtr &_msg)
    {
       gazebo::common::Time simTime  = gazebo::msgs::Convert(_msg->sim_time());
       //size_t size;
       double ttime = simTime.Double();
       //ach_put(&chan_time, _msg->image().data().c_str() , _msg->image().data().size());
    }


    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf) 
    {
        // Open Ach channel
        /* open ach channel */
        memset( &H_ref,   0, sizeof(H_ref));
        memset( &H_state,   0, sizeof(H_state));
        int r = ach_open(&chan_pt_drive_ref, "robot-pt-drive" , NULL);
        assert( ACH_OK == r );
        ach_put(&chan_pt_drive_ref, &H_ref , sizeof(H_ref));      
    
        memset( &ttime,   0, sizeof(ttime));
        r = ach_open(&chan_time, "robot-time" , NULL);
        assert( ACH_OK == r );
        ach_put(&chan_time, &ttime , sizeof(ttime));

        r = ach_open(&user_config_chan, "user-config-chan" , NULL);
        assert( ACH_OK == r );

        r = ach_open(&state_chan, "robot-state", NULL);
        assert( ACH_OK == r);
        ach_put(&state_chan, &H_state, sizeof(H_state));

        // Store the pointer to the model
        this->model = _parent;

        // Get then name of the parent model
        // std::string modelName = _sdf->GetParent()->Get<std::string>("name");

        // Get the world name.
//      std::string worldName = _sdf->GetName();
        this->world = physics::get_world("default");


        // Load parameters for this plugin
        if (this->LoadParams(_sdf))
        {
           // Listen to the update event. This event is broadcast every
           // simulation iteration.
           this->updateConnection = event::Events::ConnectWorldUpdateBegin(
              boost::bind(&ModelPanTiltDrive::OnUpdate, this));
        }

        // subscribe to thread
//      gazebo::transport::NodePtr node(new gazebo::transport::Node());
//      node->Init();
//      gazebo::transport::SubscriberPtr sub = node->Subscribe("/gazebo/default/world_stats", cb);
    }

    public: bool LoadParams(sdf::ElementPtr _sdf) 
    {
      if (this->FindJointByParam(_sdf, this->pan_joint_,
                             "pan") &&
          this->FindJointByParam(_sdf, this->tilt_joint_,
                             "tilt"))
        return true;
      else
        return false;
    }

    public: bool FindJointByParam(sdf::ElementPtr _sdf,
                                  physics::JointPtr &_joint,
                                  std::string _param)
    {
      if (!_sdf->HasElement(_param))
      {
        gzerr << "param [" << _param << "] not found\n";
        return false;
      }
      else
      {
        _joint = this->model->GetJoint(
          _sdf->GetElement(_param)->GetValueString());

        if (!_joint)
        {
          gzerr << "joint by name ["
                << _sdf->GetElement(_param)->GetValueString()
                << "] not found in model\n";
          return false;
        }
      }
      return true;
    }

    // Called by the world update start event
    public: void OnUpdate()
    {
      // Get Ach chan data
      size_t fs;
      int r = ach_get( &chan_pt_drive_ref, &H_ref, sizeof(H_ref), &fs, NULL, ACH_O_LAST );

      if(ACH_OK != r | ACH_STALE_FRAMES != r | ACH_MISSED_FRAME != r) {
        if(debug) {
          printf("ref int r = %i \n\r",r);
	}
      }
      else{   assert( sizeof(H_ref) == fs ); }

      ach_get( &user_config_chan, &user_config, sizeof(user_config), &fs, NULL, ACH_O_LAST );

      // check if we are in simulate or real mode
      if (user_config.flag[0] == 0) {
         // update the robot
         this->pan_joint_->SetMaxForce(0, 100);
         this->tilt_joint_->SetMaxForce(0, 100);
         this->pan_joint_->SetAngle(0, H_ref[0]);
         this->tilt_joint_->SetAngle(0, H_ref[1]);

         // send out the sim time
         ttime = this->world->GetSimTime().Double();
         ach_put(&chan_time, &ttime, sizeof(ttime));
 
         // update the state
         H_state[0] = this->pan_joint_->GetAngle(0).Radian();
         H_state[1] = this->tilt_joint_->GetAngle(0).Radian();
         ach_put(&state_chan, &H_state, sizeof(H_state));
      } else {
         // send out the wall time
         ttime = common::Time::GetWallTime().Double();
         ach_put(&chan_time, &ttime, sizeof(ttime));
      }
    }

    // Pointer to the model
    private: physics::ModelPtr model;
    private: physics::WorldPtr world;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;

    private: physics::JointPtr pan_joint_;
    private: physics::JointPtr tilt_joint_;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(ModelPanTiltDrive)
}
