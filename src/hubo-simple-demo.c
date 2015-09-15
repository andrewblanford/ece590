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

	// move arms out of the way
	H_ref.ref[RSR] = -.1;
	H_ref.ref[LSR] = .1;

    /* Sway to be over 1 foot = 8.5 degrees? */
	double baseAngle = .14 / 10.0;
	for (int i = 0; i < 11; ++i) {
	    H_ref.ref[RHR] = baseAngle * i;
	    H_ref.ref[RAR] = -baseAngle * i;
	    H_ref.ref[LHR] = baseAngle * i;
	    H_ref.ref[LAR] = -baseAngle * i;
	    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		usleep(500000);
	}
	sleep(1);
	printf("RHR: %f\n", H_ref.ref[RHR]);

	/* bend knee slowly to raise the leg */
	baseAngle = .05;
	for (int i = 0; i < 20; ++i) {
	    H_ref.ref[LHP] = -baseAngle * i;
	    H_ref.ref[LKN] = 2 * baseAngle * i;
	    H_ref.ref[LAP] = -baseAngle * i;
	    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		usleep(500000);
	}
	sleep(2);

	// begin knee bends
	const int INTERVAL_USEC = 125000;
	int direction = 1; // start going down
	const int NUM_INTERVALS = 16;
	// need 49 degree deflection in hip to create .2m amplitude
	baseAngle = .87 / NUM_INTERVALS;
	double baseHipAngle = (.22 - .14) / NUM_INTERVALS;
	for (int reps = 0; reps < 10; ++reps) {
		printf("Bend %d\n", reps);
		// bend knee - 2 seconds
		for (int i = 0; i < NUM_INTERVALS; ++i) {
			ach_get( &chan_hubo_state, &H_state, sizeof(H_state), &fs, NULL, ACH_O_LAST );
			double begin = H_state.time;
			// bend the knee
			H_ref.ref[RHP] += -baseAngle * direction;
		    H_ref.ref[RKN] += 2 * baseAngle * direction;
		    H_ref.ref[RAP] += -baseAngle * direction;
			// move the hip / ankle so CoM stays over foot
/*
			H_ref.ref[RHR] += baseHipAngle * direction;
			H_ref.ref[RAR] += -baseHipAngle * direction;
			H_ref.ref[LHR] += baseHipAngle * direction;
			H_ref.ref[LAR] += -baseHipAngle * direction;
*/
			printf("RHP: %f \t RHR: %f\n", H_ref.ref[RHP], H_ref.ref[RHR]);
		    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
			ach_get( &chan_hubo_state, &H_state, sizeof(H_state), &fs, NULL, ACH_O_LAST );
			double end = H_state.time;
			usleep(INTERVAL_USEC - (end - begin));
		}
		direction = direction * -1;
	}


	sleep(5);

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
    H_ref.ref[LSR] = 0.0;
	ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
}

