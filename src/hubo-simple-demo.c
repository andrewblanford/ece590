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

    /* Move elbow and shoulder into wave position */
    H_ref.ref[LEB] = -2.0;
    H_ref.ref[LSP] = -0.5;
    H_ref.ref[LWR] = 1.5;
    H_ref.ref[LWP] = -0.5;
    H_ref.ref[LSY] = 0.0;


    /* Print out the actual position of the LEB */
    double posLEB = H_state.joint[LEB].pos;
    printf("Joint = %f\r\n",posLEB);

    /* Print out the Left foot torque in X */
    double mxLeftFT = H_state.ft[HUBO_FT_L_FOOT].m_x;
    printf("Mx = %f\r\n", mxLeftFT);

    /* Write to the feed-forward channel */
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));

	sleep(2);

#define TIME_STEP (250000)

	int i = 0;
	while (i < 30) {
	    H_ref.ref[LSY] = 0.0;
	    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		usleep(TIME_STEP);
	    H_ref.ref[LSY] = 0.4;
	    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		usleep(TIME_STEP);
	    H_ref.ref[LSY] = 0.0;
	    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		usleep(TIME_STEP);
	    H_ref.ref[LSY] = -0.4;
	    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		usleep(TIME_STEP);
		i++;
		printf("Wave %d\n", i);
	}

	// return to base position
    H_ref.ref[LEB] = 0.0;
    H_ref.ref[LSP] = 0.0;
    H_ref.ref[LWR] = 0.0;
    H_ref.ref[LWP] = 0.0;
    H_ref.ref[LSY] = 0.0;
	ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
}

