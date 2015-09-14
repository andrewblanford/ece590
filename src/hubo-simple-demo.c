/* Standard Stuff */
#include <string.h>
#include <stdio.h>

/* Required Hubo Headers */
#include <hubo.h>

/* For Ach IPC */
#include <errno.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <inttypes.h>
#include "ach.h"


/* Ach Channel IDs */
ach_channel_t chan_hubo_ref;      // Feed-Forward (Reference)
ach_channel_t chan_hubo_state;    // Feed-Back (State)

int main(int argc, char **argv) {

    /* Open Ach Channel */
    int r = ach_open(&chan_hubo_ref, HUBO_CHAN_REF_NAME , NULL);
    assert( ACH_OK == r );

    r = ach_open(&chan_hubo_state, HUBO_CHAN_STATE_NAME , NULL);
    assert( ACH_OK == r );



    /* Create initial structures to read and write from */
    struct hubo_ref H_ref;
    struct hubo_state H_state;
    memset( &H_ref,   0, sizeof(H_ref));
    memset( &H_state, 0, sizeof(H_state));

    /* for size check */
    size_t fs;

    /* Get the current feed-forward (state) */
    r = ach_get( &chan_hubo_state, &H_state, sizeof(H_state), &fs, NULL, ACH_O_LAST );
    if(ACH_OK != r) {
        assert( sizeof(H_state) == fs );
    }

    /* Sway to be over 1 foot = 8.5 degrees? */
    H_ref.ref[RHR] = .07;
    H_ref.ref[RAR] = -.07;
    H_ref.ref[LHR] = .07;
    H_ref.ref[LAR] = -.07;
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
	sleep(1);
    H_ref.ref[RHR] = .14;
    H_ref.ref[RAR] = -.14;
    H_ref.ref[LHR] = .14;
    H_ref.ref[LAR] = -.14;
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
	sleep(2);
	/* bend knee slightly */
    //H_ref.ref[RHP] = -.28;
    //H_ref.ref[RKN] = .56;
    //H_ref.ref[RAP] = -.28;
    H_ref.ref[LHP] = -.28;
    H_ref.ref[LKN] = .56;
    H_ref.ref[LAP] = -.28;
	// raise right arm for balance? 
    H_ref.ref[RSR] = -.25;
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
	

    /* Print out the actual position of the LEB */
    double posLEB = H_state.joint[LEB].pos;
    printf("Joint = %f\r\n",posLEB);

    /* Print out the Left foot torque in X */
    double mxLeftFT = H_state.ft[HUBO_FT_L_FOOT].m_x;
    printf("Mx = %f\r\n", mxLeftFT);

    /* Write to the feed-forward channel */
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));

	sleep(2);

	/* Lift left leg */
	H_ref.ref[LHP] = -.7;
	H_ref.ref[LKN] = 1.4;

    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));

	sleep(10);

	// return to base position
    H_ref.ref[RHP] = 0;
    H_ref.ref[RKN] = 0;
    H_ref.ref[RAP] = 0;
    H_ref.ref[LHP] = 0;
    H_ref.ref[LKN] = 0;
    H_ref.ref[LAP] = 0;
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));

	sleep(2);
	
    H_ref.ref[RHR] = 0.0;
    H_ref.ref[RAR] = 0.0;
    H_ref.ref[LHR] = 0.0;
    H_ref.ref[LAR] = 0.0;
    H_ref.ref[RSR] = 0.0;
	ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
}

